"""Passo 3 — OCR fino com PaddleOCR.

PaddleOCR e mais preciso que o Claude pra texto pequeno e pra bbox pixel-exata.
Aqui pegamos o texto literal e a bbox; estilo (cor/tamanho) vem no Passo 5.
"""

import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

# Import preguicoso: paddleocr e pesado e nao queremos pagar custo de import
# se este modulo nao for usado.
_OCR = None


def _get_ocr():
    global _OCR
    if _OCR is None:
        from paddleocr import PaddleOCR

        _OCR = PaddleOCR(use_angle_cls=True, lang="pt", show_log=False)
    return _OCR


def rodar_ocr(img: Image.Image) -> list[dict[str, Any]]:
    """Roda PaddleOCR e devolve lista de blocos: {texto, bbox, confianca}."""
    ocr = _get_ocr()
    arr = np.array(img.convert("RGB"))

    resultado = ocr.ocr(arr, cls=True)
    if not resultado or not resultado[0]:
        return []

    blocos = []
    for linha in resultado[0]:
        poligono, (texto, confianca) = linha
        # poligono = [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] (4 cantos)
        xs = [p[0] for p in poligono]
        ys = [p[1] for p in poligono]
        bbox = {
            "x": int(min(xs)),
            "y": int(min(ys)),
            "w": int(max(xs) - min(xs)),
            "h": int(max(ys) - min(ys)),
        }
        blocos.append(
            {
                "texto": texto,
                "bbox": bbox,
                "confianca": round(float(confianca), 3),
            }
        )

    return blocos


def visualizar(
    img: Image.Image, blocos: list[dict[str, Any]], destino: Path
) -> None:
    """Desenha bbox e texto por cima da imagem original (debug visual)."""
    debug = img.convert("RGB").copy()
    draw = ImageDraw.Draw(debug)
    for b in blocos:
        x, y, w, h = b["bbox"]["x"], b["bbox"]["y"], b["bbox"]["w"], b["bbox"]["h"]
        cor = "red" if b["confianca"] < 0.8 else "lime"
        draw.rectangle([x, y, x + w, y + h], outline=cor, width=2)

    destino.parent.mkdir(parents=True, exist_ok=True)
    debug.save(destino)


def salvar(blocos: list[dict[str, Any]], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(blocos, ensure_ascii=False, indent=2), encoding="utf-8"
    )
