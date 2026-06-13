"""Passo 4 — Reconciliar resultados do Claude (semantica) e PaddleOCR (precisao).

Estrategia:
- Pra cada camada tipo "texto" do Claude, achar bloco OCR com IoU > 0.3
- Substituir texto e bbox do Claude pelos do OCR (mais preciso)
- Marcar camadas Claude sem match como "suspeita_alucinacao"
- Blocos OCR sem match Claude viram novas camadas "texto_orfao"
"""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


IOU_MIN = 0.3


def reconciliar(
    layout_claude: dict[str, Any], blocos_ocr: list[dict[str, Any]]
) -> dict[str, Any]:
    resultado = deepcopy(layout_claude)
    camadas = resultado.get("camadas", [])

    # Marca OCRs usados pra identificar orfaos depois
    ocr_usado = [False] * len(blocos_ocr)

    for camada in camadas:
        if camada.get("tipo") != "texto":
            continue

        bbox_c = camada.get("bbox")
        if not bbox_c:
            continue

        melhor_idx = -1
        melhor_iou = 0.0
        for i, bloco in enumerate(blocos_ocr):
            if ocr_usado[i]:
                continue
            iou = _iou(bbox_c, bloco["bbox"])
            if iou > melhor_iou:
                melhor_iou = iou
                melhor_idx = i

        if melhor_iou >= IOU_MIN:
            bloco = blocos_ocr[melhor_idx]
            camada["conteudo"] = bloco["texto"]
            camada["bbox"] = bloco["bbox"]
            camada["_ocr_confianca"] = bloco["confianca"]
            ocr_usado[melhor_idx] = True
        else:
            camada["_suspeita"] = "sem_match_ocr"

    # Texto OCR sem match Claude vira camada nova
    proximo_id = 1
    for i, bloco in enumerate(blocos_ocr):
        if ocr_usado[i]:
            continue
        camadas.append(
            {
                "id": f"texto_orfao_{proximo_id:02d}",
                "tipo": "texto",
                "conteudo": bloco["texto"],
                "bbox": bloco["bbox"],
                "cor_texto": None,
                "tamanho_aproximado": None,
                "fonte_classe": None,
                "_ocr_confianca": bloco["confianca"],
                "_origem": "ocr_apenas",
            }
        )
        proximo_id += 1

    resultado["camadas"] = camadas
    resultado["_meta_reconciliacao"] = {
        "iou_min": IOU_MIN,
        "ocr_total": len(blocos_ocr),
        "ocr_casados": sum(ocr_usado),
        "ocr_orfaos": sum(1 for u in ocr_usado if not u),
        "claude_suspeitos": sum(
            1 for c in camadas if c.get("_suspeita") == "sem_match_ocr"
        ),
    }
    return resultado


def _iou(a: dict[str, int], b: dict[str, int]) -> float:
    """Intersection over Union de dois bboxes formato {x, y, w, h}."""
    ax1, ay1, ax2, ay2 = a["x"], a["y"], a["x"] + a["w"], a["y"] + a["h"]
    bx1, by1, bx2, by2 = b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]

    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)

    inter_w = max(0, ix2 - ix1)
    inter_h = max(0, iy2 - iy1)
    inter = inter_w * inter_h
    if inter == 0:
        return 0.0

    area_a = a["w"] * a["h"]
    area_b = b["w"] * b["h"]
    uniao = area_a + area_b - inter
    return inter / uniao if uniao > 0 else 0.0


def salvar(dados: dict[str, Any], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
