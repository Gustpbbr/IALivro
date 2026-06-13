"""Gera captions (.txt) baseline para um dataset de personagem/estilo.

Cria um <imagem>.txt ao lado de cada imagem da pasta, com:
  <trigger_word>, <descricao_base>

Uso:
  python training/gerar_captions.py <pasta> <trigger_word> ["descricao base"]

Ex.:
  python training/gerar_captions.py dataset/201_leonidas_stf leonidas_stf_xyz \
    "a lion anthropomorphic character, STF supreme court justice, black velvet robe"

⚠️ Estas captions são um PONTO DE PARTIDA. O ideal é refiná-las por imagem com
visão (descrever pose, ângulo, fundo — o que DEVE poder variar), para o modelo
não "grudar" fundo/roupa na identidade do personagem. Ver
referencia_visual/CHECKLIST_REVISAO_61_PRANCHAS.md e BANCO_FICHAS_CANONICAS.md.
"""

import sys
from pathlib import Path

EXTS = (".png", ".jpg", ".jpeg", ".webp")


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    pasta = Path(sys.argv[1])
    trigger = sys.argv[2]
    base = sys.argv[3] if len(sys.argv) > 3 else ""

    imgs = [p for p in sorted(pasta.glob("*")) if p.suffix.lower() in EXTS]
    if not imgs:
        print(f"Nenhuma imagem em {pasta}")
        return 1

    caption = f"{trigger}, {base}".rstrip(", ").strip()
    for img in imgs:
        txt = img.with_suffix(".txt")
        txt.write_text(caption + "\n", encoding="utf-8")
        print(f"  {txt.name}")
    print(f"OK: {len(imgs)} captions baseline em {pasta} (refinar por imagem com visão)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
