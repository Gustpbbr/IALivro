"""CLI principal da POC de descompilacao.

Uso:
    python descompila.py <caminho_da_imagem>

Saida vai para ./output/
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from etapas.carregar import carregar, salvar_copia_debug


RAIZ = Path(__file__).parent
OUTPUT = RAIZ / "output"
DEBUG = OUTPUT / "debug"


def main() -> int:
    load_dotenv(RAIZ / ".env")

    if len(sys.argv) != 2:
        print("Uso: python descompila.py <caminho_da_imagem>")
        return 1

    caminho = Path(sys.argv[1]).expanduser().resolve()

    print(f"\n=== POC Descompilacao ===")
    print(f"Imagem: {caminho}")

    # Passo 1 — Carregar
    img = carregar(caminho)
    print(f"\n[Passo 1] Carregada: {img.width} x {img.height}, modo {img.mode}")

    salvar_copia_debug(img, DEBUG / "00_imagem_original.png")
    print(f"           Salva em {DEBUG / '00_imagem_original.png'}")

    # Passos 2-8 — ainda nao implementados
    print("\n[Passos 2-8] Pendentes. Ver ../ETAPA_B_PASSO_A_PASSO.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
