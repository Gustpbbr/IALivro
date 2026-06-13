"""CLI principal da POC de descompilacao.

Uso:
    python descompila.py <caminho_da_imagem> [--pular-fal] [--pular-claude]

Por padrao roda todos os 8 passos. Flags pulam etapas caras se as chaves
nao estiverem disponiveis (util pra teste parcial).

Saida em ./output/
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from etapas.carregar import carregar, salvar_copia_debug
from etapas import analise_layout, ocr, reconciliar, estilo, sam, inpaint, exportar


RAIZ = Path(__file__).parent
OUTPUT = RAIZ / "output"
DEBUG = OUTPUT / "debug"
PROMPTS = RAIZ / "prompts"


def main() -> int:
    load_dotenv(RAIZ / ".env")

    argv = sys.argv[1:]
    pular_fal = "--pular-fal" in argv
    pular_claude = "--pular-claude" in argv
    posicionais = [a for a in argv if not a.startswith("--")]

    if len(posicionais) != 1:
        print("Uso: python descompila.py <caminho_da_imagem> [--pular-fal] [--pular-claude]")
        return 1

    caminho = Path(posicionais[0]).expanduser().resolve()

    print("\n=== POC Descompilacao ===")
    print(f"Imagem: {caminho}")

    # Passo 1
    img = carregar(caminho)
    print(f"\n[Passo 1] Carregada: {img.width} x {img.height}, modo {img.mode}")
    salvar_copia_debug(img, DEBUG / "00_imagem_original.png")

    # Passo 2
    layout = _passo2_claude(img, pular_claude)

    # Passo 3
    print("\n[Passo 3] Rodando PaddleOCR...")
    blocos_ocr = ocr.rodar_ocr(img)
    ocr.salvar(blocos_ocr, DEBUG / "02_ocr.json")
    ocr.visualizar(img, blocos_ocr, DEBUG / "02_ocr_visual.png")
    print(f"           {len(blocos_ocr)} blocos de texto")

    # Passo 4
    print("\n[Passo 4] Reconciliando Claude + OCR...")
    layout = reconciliar.reconciliar(layout, blocos_ocr)
    reconciliar.salvar(layout, DEBUG / "03_reconciliado.json")
    meta_r = layout.get("_meta_reconciliacao", {})
    print(f"           OCR casados: {meta_r.get('ocr_casados')}/{meta_r.get('ocr_total')}")

    # Passo 5
    print("\n[Passo 5] Estimando estilo dos textos...")
    layout = estilo.aplicar(layout, img)
    estilo.salvar(layout, DEBUG / "04_com_estilo.json")
    n_textos = sum(1 for c in layout["camadas"] if c.get("tipo") == "texto")
    print(f"           {n_textos} textos com cor/tamanho amostrados")

    # Passo 6
    if pular_fal or not os.environ.get("FAL_KEY"):
        print("\n[Passo 6] PULADO (FAL_KEY ausente ou --pular-fal)")
    else:
        print("\n[Passo 6] Segmentando icones com SAM 2 (Fal.ai)...")
        layout = sam.aplicar(layout, img, OUTPUT / "icones")
        sam.salvar(layout, DEBUG / "05_com_recortes.json")
        n_recortados = sum(1 for c in layout["camadas"] if c.get("arquivo_recorte"))
        print(f"           {n_recortados} elementos recortados em output/icones/")

    # Passo 7
    if pular_fal or not os.environ.get("FAL_KEY"):
        print("\n[Passo 7] PULADO (FAL_KEY ausente ou --pular-fal)")
    else:
        print("\n[Passo 7] Inpainting do fundo + mascaras individuais...")
        layout = inpaint.gerar(layout, img, OUTPUT)
        inpaint.salvar(layout, DEBUG / "06_com_mascaras.json")
        n_mascaras = sum(1 for c in layout["camadas"] if c.get("mascara"))
        print(f"           fundo_limpo.png + {n_mascaras} mascaras geradas")

    # Passo 8
    print("\n[Passo 8] Consolidando exportacao final...")
    final = exportar.consolidar(layout, OUTPUT, caminho.name)
    exportar.visualizar(img, final, DEBUG / "visualizacao_final.png")
    print(f"           camadas.json: {len(final['camadas'])} camadas")
    print(f"           visualizacao em {DEBUG / 'visualizacao_final.png'}")
    print(f"\nResultado em {OUTPUT}/")

    return 0


def _passo2_claude(img, pular: bool):
    """Passo 2 com fallback: se nao tem chave/pular, tenta usar layout existente."""
    cache = DEBUG / "01_claude_layout.json"
    if pular or not os.environ.get("ANTHROPIC_API_KEY"):
        if cache.exists():
            import json

            print(f"\n[Passo 2] Reutilizando {cache.name} (pulado).")
            return json.loads(cache.read_text())
        raise RuntimeError(
            "Passo 2 pulado e nao ha layout em cache. "
            "Rode com ANTHROPIC_API_KEY ou forneca 01_claude_layout.json manualmente."
        )

    print("\n[Passo 2] Chamando Claude vision...")
    layout = analise_layout.analisar_layout(img, PROMPTS / "claude_layout.txt")
    analise_layout.salvar(layout, DEBUG / "01_claude_layout.json")
    meta = layout.get("_meta", {})
    print(f"           {len(layout.get('camadas', []))} camadas")
    print(f"           tokens: {meta.get('tokens_input')}/{meta.get('tokens_output')}")
    return layout


if __name__ == "__main__":
    sys.exit(main())
