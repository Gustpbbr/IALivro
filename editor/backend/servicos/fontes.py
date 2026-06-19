"""Catalogo de fontes do editor + carga sob demanda.

Reflete ETAPA_C_DESIGN.md §4. Cada fonte:
- id (usado pelo frontend)
- arquivo .ttf/.otf esperado em backend/dados/fontes/
- url do Google Fonts pra download (fallback se nao tiver localmente)
"""

from pathlib import Path
from typing import Optional

import requests
from PIL import ImageFont


PASTA_FONTES = Path(__file__).parent.parent / "dados" / "fontes"
PASTA_FONTES.mkdir(parents=True, exist_ok=True)

CATALOGO = {
    "cormorant": {
        "nome": "Cormorant Garamond",
        "classe": "serif",
        "arquivo": "CormorantGaramond-Regular.ttf",
        "url": "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond-Regular.ttf",
    },
    "source-serif": {
        "nome": "Source Serif Pro",
        "classe": "serif",
        "arquivo": "SourceSerif4-Regular.ttf",
        "url": "https://github.com/google/fonts/raw/main/ofl/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf",
    },
    "inter": {
        "nome": "Inter",
        "classe": "sans_serif",
        "arquivo": "Inter-Regular.ttf",
        "url": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
    },
    "work-sans": {
        "nome": "Work Sans",
        "classe": "sans_serif",
        "arquivo": "WorkSans-Regular.ttf",
        "url": "https://github.com/google/fonts/raw/main/ofl/worksans/WorkSans%5Bwght%5D.ttf",
    },
    "cinzel": {
        "nome": "Cinzel",
        "classe": "display",
        "arquivo": "Cinzel-Regular.ttf",
        "url": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel%5Bwght%5D.ttf",
    },
    "playfair": {
        "nome": "Playfair Display",
        "classe": "display",
        "arquivo": "PlayfairDisplay-Regular.ttf",
        "url": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    },
}

FALLBACK_SISTEMA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def caminho(fonte_id: str) -> Path:
    info = CATALOGO.get(fonte_id) or CATALOGO["inter"]
    return PASTA_FONTES / info["arquivo"]


def garantir_local(fonte_id: str) -> Optional[Path]:
    """Baixa do Google Fonts se ainda nao tiver localmente."""
    info = CATALOGO.get(fonte_id)
    if not info:
        return None

    arquivo = PASTA_FONTES / info["arquivo"]
    if arquivo.exists() and arquivo.stat().st_size > 1000:
        return arquivo

    try:
        resp = requests.get(info["url"], timeout=20)
        resp.raise_for_status()
        arquivo.write_bytes(resp.content)
        return arquivo
    except Exception as exc:
        print(f"[fontes] falha ao baixar {fonte_id}: {exc}")
        return None


def carregar(
    fonte_id: str, tamanho_px: int, peso: str = "normal"
) -> ImageFont.FreeTypeFont:
    """Carrega fonte pra render. Fallback: DejaVuSans do sistema."""
    arquivo = garantir_local(fonte_id) if fonte_id else None
    if arquivo and arquivo.exists():
        try:
            return ImageFont.truetype(str(arquivo), size=tamanho_px)
        except Exception:
            pass
    # Fallback
    if Path(FALLBACK_SISTEMA).exists():
        return ImageFont.truetype(FALLBACK_SISTEMA, size=tamanho_px)
    return ImageFont.load_default()
