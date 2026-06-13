"""Passo 7 — Inpainting do fundo + mascaras individuais por elemento.

Gera:
- fundo_limpo.png: cena sem texto/boxes/icones (uma chamada Fal com mascara global)
- mascaras/<id>.png: mascara binaria por camada editavel (sem chamada Fal)

As mascaras individuais sao o que o editor (Etapa C) vai mandar pros modos
P3 amarelo (refazer fundo) e azul (estender cena).
"""

import base64
import io
import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np
import requests
from PIL import Image, ImageDraw


FAL_ENDPOINT_INPAINT = "fal-ai/lama"
TIMEOUT = 180

# Tipos que viram "elemento UI" (sao apagados do fundo)
TIPOS_UI = ("texto", "caixa", "icone", "linha_divisoria")
# Tipos que ganham mascara individual pra modos P3
TIPOS_COM_MASCARA = ("caixa", "icone", "texto")


def gerar(
    layout: dict[str, Any],
    img: Image.Image,
    pasta_output: Path,
) -> dict[str, Any]:
    fal_key = os.environ.get("FAL_KEY", "")
    if not fal_key:
        raise RuntimeError(
            "FAL_KEY nao encontrada. Configure no .env ou no environment."
        )

    pasta_output.mkdir(parents=True, exist_ok=True)
    pasta_mascaras = pasta_output / "mascaras"
    pasta_mascaras.mkdir(exist_ok=True)

    camadas = layout.get("camadas", [])

    # Mascara global (uniao de todos os elementos UI)
    mascara_global = _construir_mascara_global(img.size, camadas)
    fundo_limpo = _chamar_inpainting(img, mascara_global, fal_key)
    fundo_limpo.save(pasta_output / "fundo_limpo.png")

    # Mascaras individuais
    resultado = deepcopy(layout)
    for camada in resultado.get("camadas", []):
        if camada.get("tipo") not in TIPOS_COM_MASCARA:
            continue
        bbox = camada.get("bbox")
        if not bbox:
            continue
        mascara = _mascara_da_camada(img.size, bbox)
        arquivo = pasta_mascaras / f"{camada['id']}.png"
        mascara.save(arquivo)
        camada["mascara"] = f"mascaras/{camada['id']}.png"

    return resultado


def _construir_mascara_global(
    tamanho: tuple[int, int], camadas: list[dict[str, Any]]
) -> Image.Image:
    mascara = Image.new("L", tamanho, 0)
    draw = ImageDraw.Draw(mascara)
    for c in camadas:
        if c.get("tipo") not in TIPOS_UI:
            continue
        b = c.get("bbox")
        if not b:
            continue
        draw.rectangle([b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]], fill=255)
    return mascara


def _mascara_da_camada(tamanho: tuple[int, int], bbox: dict[str, int]) -> Image.Image:
    mascara = Image.new("L", tamanho, 0)
    draw = ImageDraw.Draw(mascara)
    draw.rectangle(
        [bbox["x"], bbox["y"], bbox["x"] + bbox["w"], bbox["y"] + bbox["h"]], fill=255
    )
    return mascara


def _chamar_inpainting(
    img: Image.Image, mascara: Image.Image, fal_key: str
) -> Image.Image:
    image_url = _imagem_para_data_url(img.convert("RGB"))
    mask_url = _imagem_para_data_url(mascara.convert("L"))

    resp = requests.post(
        f"https://fal.run/{FAL_ENDPOINT_INPAINT}",
        headers={
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json",
        },
        json={"image_url": image_url, "mask_url": mask_url},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    dados = resp.json()
    url = dados.get("image", {}).get("url") if isinstance(dados.get("image"), dict) else None
    if not url:
        raise RuntimeError(f"Inpaint sem URL no retorno: {list(dados)}")
    bin_img = requests.get(url, timeout=120).content
    return Image.open(io.BytesIO(bin_img)).convert("RGB")


def _imagem_para_data_url(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.standard_b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def salvar(dados: dict[str, Any], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
