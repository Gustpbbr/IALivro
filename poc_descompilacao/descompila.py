"""CLI principal da POC de descompilacao.

Uso:
    python descompila.py <caminho_da_imagem>

Saida vai para ./output/
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from etapas.carregar import carregar, salvar_copia_debug
from etapas import analise_layout, ocr, reconciliar


RAIZ = Path(__file__).parent
OUTPUT = RAIZ / "output"
DEBUG = OUTPUT / "debug"
PROMPTS = RAIZ / "prompts"


def main() -> int:
    load_dotenv(RAIZ / ".env")

    if len(sys.argv) != 2:
        print("Uso: python descompila.py <caminho_da_imagem>")
        return 1

    caminho = Path(sys.argv[1]).expanduser().resolve()

    print("\n=== POC Descompilacao ===")
    print(f"Imagem: {caminho}")

    # Passo 1 — Carregar
    img = carregar(caminho)
    print(f"\n[Passo 1] Carregada: {img.width} x {img.height}, modo {img.mode}")
    salvar_copia_debug(img, DEBUG / "00_imagem_original.png")

    # Passo 2 — Analise semantica com Claude vision
    print("\n[Passo 2] Chamando Claude vision...")
    layout = analise_layout.analisar_layout(
        img, PROMPTS / "claude_layout.txt"
    )
    analise_layout.salvar(layout, DEBUG / "01_claude_layout.json")
    n_camadas = len(layout.get("camadas", []))
    meta = layout.get("_meta", {})
    print(f"           {n_camadas} camadas identificadas")
    print(f"           tokens in/out: {meta.get('tokens_input')}/{meta.get('tokens_output')}")

    # Passo 3 — OCR
    print("\n[Passo 3] Rodando PaddleOCR...")
    blocos_ocr = ocr.rodar_ocr(img)
    ocr.salvar(blocos_ocr, DEBUG / "02_ocr.json")
    ocr.visualizar(img, blocos_ocr, DEBUG / "02_ocr_visual.png")
    confiantes = sum(1 for b in blocos_ocr if b["confianca"] >= 0.8)
    print(f"           {len(blocos_ocr)} blocos de texto ({confiantes} com confianca >= 0.8)")

    # Passo 4 — Reconciliacao
    print("\n[Passo 4] Reconciliando Claude + OCR...")
    reconciliado = reconciliar.reconciliar(layout, blocos_ocr)
    reconciliar.salvar(reconciliado, DEBUG / "03_reconciliado.json")
    meta_r = reconciliado.get("_meta_reconciliacao", {})
    print(f"           OCR casados: {meta_r.get('ocr_casados')}/{meta_r.get('ocr_total')}")
    print(f"           OCR orfaos:  {meta_r.get('ocr_orfaos')}")
    print(f"           Claude suspeitos (sem match OCR): {meta_r.get('claude_suspeitos')}")

    # Passos 5-8 — pendentes
    print("\n[Passos 5-8] Pendentes. Ver ../ETAPA_B_PASSO_A_PASSO.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
