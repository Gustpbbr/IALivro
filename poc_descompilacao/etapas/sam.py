"""Passo 6 — Segmentacao fina com SAM 2 via fal.ai.

Pra cada camada tipo 'icone' ou 'cena', chama SAM 2 com prompt de ponto
(centro do bbox). Recebe a mascara, recorta o PNG transparente.
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
from PIL import Image


FAL_ENDPOINT = "fal-ai/sam2/image"
TIMEOUT = 120


def aplicar(
    layout: dict[str, Any],
    img: Image.Image,
    pasta_icones: Path,
    tipos_alvo: tuple[str, ...] = ("icone", "cena"),
) -> dict[str, Any]:
    fal_key = os.environ.get("FAL_KEY", "")
    if not fal_key:
        raise RuntimeError(
            "FAL_KEY nao encontrada. Configure no .env ou no environment."
        )

    resultado = deepcopy(layout)
    pasta_icones.mkdir(parents=True, exist_ok=True)

    image_url = _imagem_para_data_url(img)

    for camada in resultado.get("camadas", []):
        if camada.get("tipo") not in tipos_alvo:
            continue
        bbox = camada.get("bbox")
        if not bbox:
            continue

        cx = bbox["x"] + bbox["w"] // 2
        cy = bbox["y"] + bbox["h"] // 2

        try:
            mascara_img = _chamar_sam(image_url, cx, cy, fal_key)
        except Exception as exc:
            camada["_sam_erro"] = str(exc)
            continue

        # Recorte transparente pela mascara
        recorte = _recortar_com_mascara(img, mascara_img, bbox)
        arquivo = pasta_icones / f"{camada['id']}.png"
        recorte.save(arquivo)
        camada["arquivo_recorte"] = f"icones/{camada['id']}.png"

    return resultado


def _chamar_sam(image_url: str, x: int, y: int, fal_key: str) -> Image.Image:
    resp = requests.post(
        f"https://fal.run/{FAL_ENDPOINT}",
        headers={
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json",
        },
        json={
            "image_url": image_url,
            "prompts": [{"x": x, "y": y, "label": "positive"}],
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    dados = resp.json()
    # Resposta tipica: {"image": {"url": "..."}, "masks": [...]}
    mascara_url = (
        dados.get("image", {}).get("url")
        if isinstance(dados.get("image"), dict)
        else dados.get("masks", [{}])[0].get("url")
    )
    if not mascara_url:
        raise RuntimeError(f"SAM retornou sem mascara: {list(dados)}")
    bin_mascara = requests.get(mascara_url, timeout=60).content
    return Image.open(io.BytesIO(bin_mascara)).convert("L")


def _recortar_com_mascara(
    img: Image.Image, mascara: Image.Image, bbox: dict[str, int]
) -> Image.Image:
    if mascara.size != img.size:
        mascara = mascara.resize(img.size, Image.BILINEAR)

    rgba = img.convert("RGBA")
    arr_rgba = np.array(rgba)
    arr_mask = np.array(mascara)
    arr_rgba[..., 3] = arr_mask

    completo = Image.fromarray(arr_rgba)
    x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]
    return completo.crop((x, y, x + w, y + h))


def _imagem_para_data_url(img: Image.Image) -> str:
    buf = io.BytesIO()
    (img if img.mode == "RGB" else img.convert("RGB")).save(buf, format="PNG")
    b64 = base64.standard_b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def salvar(dados: dict[str, Any], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
