"""Fatiador de pranchas — recorta painéis nomeados de uma prancha em alta resolução.

Uso:
  python training/fatiar.py recortar <manifest.json>   # gera os recortes
  python training/fatiar.py grade <imagem.png>         # gera overlay 10x10 p/ achar coords

Coordenadas são FRACIONÁRIAS (0.0–1.0) → independentes da resolução: o mesmo
manifest serve para a prancha de teste (1024×1536) e para a final (2400×3600).

Formato do manifest (training/fatiamento/<personagem>.json):
{
  "imagem": "referencia_visual/pranchas_personagens/prancha_leonidas_...png",
  "saida": "dataset/201_leonidas_stf",
  "trigger": "leonidas_stf_xyz",
  "recortes": [
    {"nome": "vista_3-4", "box": [0.55, 0.10, 0.98, 0.42]},   // [x1,y1,x2,y2] fracionário
    {"nome": "close_olhos", "box": [0.05, 0.62, 0.20, 0.72]}
  ]
}
Cada recorte vira <saida>/<trigger>__<nome>.png.
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def recortar(manifest_path: str) -> None:
    cfg = json.loads(Path(manifest_path).read_text())
    img = Image.open(cfg["imagem"]).convert("RGB")
    W, H = img.size
    saida = Path(cfg["saida"])
    saida.mkdir(parents=True, exist_ok=True)
    trigger = cfg.get("trigger", "item")

    for r in cfg["recortes"]:
        x1, y1, x2, y2 = r["box"]
        caixa = (round(x1 * W), round(y1 * H), round(x2 * W), round(y2 * H))
        recorte = img.crop(caixa)
        destino = saida / f"{trigger}__{r['nome']}.png"
        recorte.save(destino)
        print(f"  {destino}  ({recorte.size[0]}x{recorte.size[1]})")
    print(f"OK: {len(cfg['recortes'])} recortes de {cfg['imagem']}")


def grade(imagem_path: str) -> None:
    """Sobrepõe uma grade 10x10 rotulada (0.0–1.0) para localizar coordenadas."""
    img = Image.open(imagem_path).convert("RGB")
    W, H = img.size
    d = ImageDraw.Draw(img)
    for i in range(1, 10):
        x = round(W * i / 10)
        y = round(H * i / 10)
        d.line([(x, 0), (x, H)], fill=(255, 0, 0), width=2)
        d.line([(0, y), (W, y)], fill=(255, 0, 0), width=2)
        d.text((x + 3, 3), f"{i/10:.1f}", fill=(255, 0, 0))
        d.text((3, y + 3), f"{i/10:.1f}", fill=(255, 0, 0))
    destino = Path(imagem_path).with_name(Path(imagem_path).stem + "__grade.png")
    img.save(destino)
    print(f"Grade salva em {destino}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("recortar", "grade"):
        print(__doc__)
        sys.exit(1)
    (recortar if sys.argv[1] == "recortar" else grade)(sys.argv[2])
