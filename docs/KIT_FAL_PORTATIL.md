# KIT PORTÁTIL — fal.ai em qualquer repositório (via GitHub Actions)

> Auto-contido: contém instruções + os 2 arquivos completos. Validado em
> 12/06/2026 no repo IALivro (smoke test aprovado). Cole este documento em
> qualquer sessão do Claude Code e peça: "instale o kit fal.ai deste documento".

## Pré-requisitos (1x por repositório, ~3 min, dá pra fazer pelo celular)

1. Criar uma chave para o projeto em **fal.ai/dashboard/keys** (1 chave por
   projeto — revogável individualmente).
2. No GitHub do repositório: **Settings → Secrets and variables → Actions →
   New repository secret** → Name: `FAL_KEY` → colar a chave → Add secret.
3. Criar os 2 arquivos abaixo (ajustar o nome da branch no workflow).

## Como usar depois de instalado

Commitar um JSON em `training/requests/` → o workflow roda → resultado em
`outputs/` → o pedido vira `.done.json` (ou `.erro.json` com o diagnóstico).

```json
{
  "tipo": "smoke_test",
  "prompt": "descrição da imagem em inglês",
  "image_size": {"width": 1216, "height": 832}
}
```

Custo: FLUX schnell ≈ US$ 0,003/imagem. Novos tipos (treino de LoRA, geração
com LoRA) são funções novas no dicionário `TIPOS` do script.

---

## Arquivo 1 — `.github/workflows/fal-pipeline.yml`

> ⚠️ Trocar `SUA_BRANCH_AQUI` pela branch de trabalho do repositório.

```yaml
name: Pipeline fal.ai

on:
  push:
    branches: ["SUA_BRANCH_AQUI"]
    paths:
      - "training/requests/*.json"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  executar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install --quiet requests

      - name: Processar pedidos
        env:
          FAL_KEY: ${{ secrets.FAL_KEY }}
        run: python training/processar_pedidos.py

      - name: Commit e push dos resultados
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add outputs/ training/requests/
          if git diff --cached --quiet; then
            echo "Nada novo."
            exit 0
          fi
          git commit -m "Resultados do pipeline fal.ai (workflow)"
          git pull --rebase origin SUA_BRANCH_AQUI
          git push origin HEAD:SUA_BRANCH_AQUI
```

## Arquivo 2 — `training/processar_pedidos.py`

```python
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
```
