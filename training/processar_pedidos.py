"""Processa pedidos em training/requests/*.json contra a API da fal.ai.

Tipos suportados:
  smoke_test  — gera 1 imagem no FLUX schnell (~US$ 0,003) para validar a FAL_KEY.

Cada pedido processado é renomeado para .done.json (não roda duas vezes).
Falhas viram .erro.json com a mensagem dentro.
"""

import json
import os
import sys
from pathlib import Path

import requests

FAL_KEY = os.environ.get("FAL_KEY", "")
REQUESTS_DIR = Path("training/requests")
OUTPUTS_DIR = Path("outputs")


def smoke_test(pedido: dict, nome: str) -> None:
    """Gera 1 imagem barata (schnell) e salva em outputs/."""
    resp = requests.post(
        "https://fal.run/fal-ai/flux/schnell",
        headers={
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": pedido["prompt"],
            "image_size": pedido.get("image_size", {"width": 1024, "height": 1024}),
            "num_images": 1,
        },
        timeout=120,
    )
    resp.raise_for_status()
    dados = resp.json()
    url_imagem = dados["images"][0]["url"]

    img = requests.get(url_imagem, timeout=120)
    img.raise_for_status()
    destino = OUTPUTS_DIR / f"{nome}.png"
    destino.write_bytes(img.content)
    print(f"OK: {destino} ({len(img.content)} bytes)")


TIPOS = {"smoke_test": smoke_test}


def main() -> int:
    if not FAL_KEY:
        print("::error::FAL_KEY ausente — configurar o secret no GitHub")
        return 1

    OUTPUTS_DIR.mkdir(exist_ok=True)
    pendentes = [
        p for p in sorted(REQUESTS_DIR.glob("*.json"))
        if not p.name.endswith((".done.json", ".erro.json"))
    ]
    if not pendentes:
        print("Nenhum pedido pendente.")
        return 0

    falhas = 0
    for caminho in pendentes:
        pedido = json.loads(caminho.read_text())
        tipo = pedido.get("tipo")
        nome = caminho.stem
        print(f"--- Pedido {nome} (tipo={tipo}) ---")
        try:
            TIPOS[tipo](pedido, nome)
            caminho.rename(caminho.with_name(f"{nome}.done.json"))
        except Exception as exc:  # noqa: BLE001 — registrar qualquer falha no .erro.json
            falhas += 1
            erro = {"pedido": pedido, "erro": str(exc)}
            caminho.with_name(f"{nome}.erro.json").write_text(
                json.dumps(erro, ensure_ascii=False, indent=2)
            )
            caminho.unlink()
            print(f"::warning::Pedido {nome} falhou: {exc}")

    print(f"Concluído. Falhas: {falhas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
