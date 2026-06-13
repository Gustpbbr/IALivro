"""Passo 5 — Estimativa de estilo do texto.

Pra cada camada de tipo "texto", refina o que o Claude estimou:
- cor: amostragem real dos pixels do texto (mediana RGB, separando texto/fundo via Otsu)
- tamanho_px: altura do bbox / numero de linhas
- fonte_classe: mantem o que o Claude apontou; sem matching real ainda

Cor de fundo de caixas e cor de borda tambem podem ser refinadas aqui.
"""

from copy import deepcopy
from pathlib import Path
from typing import Any
import json

import numpy as np
from PIL import Image


def aplicar(layout: dict[str, Any], img: Image.Image) -> dict[str, Any]:
    resultado = deepcopy(layout)
    arr = np.array(img.convert("RGB"))

    for camada in resultado.get("camadas", []):
        tipo = camada.get("tipo")
        if tipo == "texto":
            _refinar_texto(camada, arr)
        elif tipo == "caixa":
            _refinar_caixa(camada, arr)

    return resultado


def _refinar_texto(camada: dict[str, Any], arr: np.ndarray) -> None:
    bbox = camada.get("bbox")
    if not bbox:
        return
    recorte = _recortar(arr, bbox)
    if recorte.size == 0:
        return

    cor_texto, cor_fundo = _amostrar_cor_texto_e_fundo(recorte)
    if cor_texto is not None:
        camada.setdefault("estilo", {})["cor"] = _rgb_para_hex(cor_texto)
        camada["estilo"]["cor_fundo_local"] = (
            _rgb_para_hex(cor_fundo) if cor_fundo is not None else None
        )

    conteudo = camada.get("conteudo") or ""
    n_linhas = conteudo.count("\n") + 1 if conteudo else 1
    altura = bbox["h"]
    tamanho_px = int(altura / n_linhas) if n_linhas > 0 else altura
    camada.setdefault("estilo", {})["tamanho_px"] = tamanho_px
    camada["estilo"]["fonte_classe"] = camada.get("fonte_classe")


def _refinar_caixa(camada: dict[str, Any], arr: np.ndarray) -> None:
    bbox = camada.get("bbox")
    if not bbox:
        return
    recorte = _recortar(arr, bbox)
    if recorte.size == 0:
        return

    pixels = recorte.reshape(-1, 3)
    cor_mediana = np.median(pixels, axis=0).astype(int)
    camada["cor_fundo"] = _rgb_para_hex(tuple(cor_mediana))


def _amostrar_cor_texto_e_fundo(
    recorte: np.ndarray,
) -> tuple[tuple[int, int, int] | None, tuple[int, int, int] | None]:
    """Otsu binariza, pega classe minoritaria como texto."""
    if recorte.shape[0] < 4 or recorte.shape[1] < 4:
        return None, None

    cinza = np.mean(recorte, axis=2).astype(np.uint8)
    limiar = _otsu(cinza)
    mascara_escuro = cinza < limiar

    n_escuros = int(mascara_escuro.sum())
    n_claros = int(mascara_escuro.size - n_escuros)
    if n_escuros == 0 or n_claros == 0:
        return None, None

    pixels = recorte.reshape(-1, 3)
    mask_flat = mascara_escuro.reshape(-1)

    cor_escuro = tuple(np.median(pixels[mask_flat], axis=0).astype(int))
    cor_claro = tuple(np.median(pixels[~mask_flat], axis=0).astype(int))

    if n_escuros < n_claros:
        return cor_escuro, cor_claro
    return cor_claro, cor_escuro


def _otsu(cinza: np.ndarray) -> int:
    """Otsu manual, evita dependencia do opencv."""
    hist, _ = np.histogram(cinza, bins=256, range=(0, 256))
    total = cinza.size
    soma_total = float(np.dot(np.arange(256), hist))

    soma_bg = 0.0
    peso_bg = 0
    var_max = 0.0
    limiar = 127

    for t in range(256):
        peso_bg += int(hist[t])
        if peso_bg == 0:
            continue
        peso_fg = total - peso_bg
        if peso_fg == 0:
            break
        soma_bg += t * float(hist[t])
        media_bg = soma_bg / peso_bg
        media_fg = (soma_total - soma_bg) / peso_fg
        var_entre = peso_bg * peso_fg * (media_bg - media_fg) ** 2
        if var_entre > var_max:
            var_max = var_entre
            limiar = t
    return limiar


def _recortar(arr: np.ndarray, bbox: dict[str, int]) -> np.ndarray:
    x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]
    H, W = arr.shape[:2]
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(W, x + w), min(H, y + h)
    return arr[y1:y2, x1:x2]


def _rgb_para_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = (int(c) for c in rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


def salvar(dados: dict[str, Any], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
