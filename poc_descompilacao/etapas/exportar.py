"""Passo 8 — Exportacao final consolidada.

Junta tudo em output/camadas.json com caminhos relativos, e gera uma
visualizacao com bbox por cima da imagem original (debug visual).
"""

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


CORES_TIPO = {
    "texto": (0, 200, 0),
    "caixa": (50, 100, 255),
    "icone": (255, 150, 0),
    "cena": (255, 0, 200),
    "linha_divisoria": (200, 200, 0),
}


def consolidar(
    layout: dict[str, Any], pasta_output: Path, imagem_origem: str
) -> dict[str, Any]:
    final = {
        "imagem_origem": imagem_origem,
        "dimensoes": layout.get("dimensoes_imagem")
        or {"largura": layout.get("largura"), "altura": layout.get("altura")},
        "fundo_limpo": "fundo_limpo.png",
        "camadas": [],
        "_meta": {
            "claude": layout.get("_meta", {}),
            "reconciliacao": layout.get("_meta_reconciliacao", {}),
        },
    }

    for camada in layout.get("camadas", []):
        cam_limpa = _limpar_camada(camada)
        final["camadas"].append(cam_limpa)

    destino = pasta_output / "camadas.json"
    destino.write_text(
        json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return final


def _limpar_camada(camada: dict[str, Any]) -> dict[str, Any]:
    """Remove campos internos (_suspeita, _origem) do JSON final."""
    return {k: v for k, v in camada.items() if not k.startswith("_")}


def visualizar(
    img: Image.Image, layout: dict[str, Any], destino: Path
) -> None:
    debug = img.convert("RGB").copy()
    draw = ImageDraw.Draw(debug)
    try:
        fonte = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13
        )
    except Exception:
        fonte = ImageFont.load_default()

    for camada in layout.get("camadas", []):
        b = camada.get("bbox")
        if not b:
            continue
        cor = CORES_TIPO.get(camada.get("tipo", ""), (128, 128, 128))
        draw.rectangle([b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]], outline=cor, width=2)
        label = f"{camada.get('tipo', '?')[:3].upper()}: {camada.get('id', '')[:24]}"
        bbox_label = draw.textbbox((b["x"] + 3, b["y"] + 3), label, font=fonte)
        draw.rectangle(bbox_label, fill=(0, 0, 0))
        draw.text((b["x"] + 3, b["y"] + 3), label, fill=cor, font=fonte)

    destino.parent.mkdir(parents=True, exist_ok=True)
    debug.save(destino)
