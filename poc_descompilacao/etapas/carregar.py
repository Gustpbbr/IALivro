"""Passo 1 — Carregar imagem e validar."""

from pathlib import Path
from PIL import Image, ImageOps


def carregar(caminho: Path) -> Image.Image:
    if not caminho.exists():
        raise FileNotFoundError(f"Imagem nao encontrada: {caminho}")

    img = Image.open(caminho)
    img = ImageOps.exif_transpose(img)

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    return img


def salvar_copia_debug(img: Image.Image, destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino)
