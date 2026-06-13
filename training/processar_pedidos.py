"""Processa pedidos em training/requests/*.json contra a API da fal.ai.

Tipos suportados:
  smoke_test  — 1 imagem no FLUX schnell (~US$ 0,003). Valida a FAL_KEY. Sem trava.
  treino_lora — treina um LoRA FLUX a partir de uma pasta de dataset (~US$ 2–3).
  geracao     — gera imagens com 1+ LoRAs aplicados (~US$ 0,02–0,035/imagem).

⚠️ TRAVA DE CUSTO: treino_lora e geracao só rodam com "confirmo_custo": true no
JSON — evita gasto acidental. smoke_test é barato e não tem trava.

Cada pedido processado vira .done.json; falhas viram .erro.json com a mensagem.
Schema do treino confirmado em fal.ai/models/fal-ai/flux-lora-fast-training (13/06/2026).
"""

import json
import os
import shutil
import sys
from pathlib import Path

import requests

FAL_KEY = os.environ.get("FAL_KEY", "")
REQUESTS_DIR = Path("training/requests")
OUTPUTS_DIR = Path("outputs")
LORAS_DIR = Path("training/loras")


def _baixar(url: str, destino: Path) -> None:
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(r.content)


def smoke_test(pedido: dict, nome: str) -> None:
    """Gera 1 imagem barata (schnell) e salva em outputs/."""
    resp = requests.post(
        "https://fal.run/fal-ai/flux/schnell",
        headers={"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"},
        json={
            "prompt": pedido["prompt"],
            "image_size": pedido.get("image_size", {"width": 1024, "height": 1024}),
            "num_images": 1,
        },
        timeout=120,
    )
    resp.raise_for_status()
    url = resp.json()["images"][0]["url"]
    _baixar(url, OUTPUTS_DIR / f"{nome}.png")
    print(f"OK: outputs/{nome}.png")


def treino_lora(pedido: dict, nome: str) -> None:
    """Treina um LoRA FLUX a partir de uma pasta de imagens.

    Campos do pedido:
      dataset      (str)  pasta com as imagens de treino (ex.: dataset/201_leonidas_stf)
      trigger_word (str)  palavra-gatilho (ex.: "leonidas_stf_xyz")
      is_style     (bool) true para LoRA de estilo, false para personagem
      steps        (int)  padrão 1000
      confirmo_custo (bool) OBRIGATÓRIO true
    """
    import fal_client  # só aqui: dependência pesada usada apenas no treino

    dataset = Path(pedido["dataset"])
    imgs = [p for p in dataset.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg")]
    if not imgs:
        raise RuntimeError(f"Nenhuma imagem em {dataset}")

    # zipar o dataset e subir para o storage da fal
    zip_base = Path("training") / f"_zip_{nome}"
    zip_path = Path(shutil.make_archive(str(zip_base), "zip", dataset))
    print(f"  {len(imgs)} imagens zipadas → {zip_path.name}")
    images_data_url = fal_client.upload_file(str(zip_path))
    zip_path.unlink(missing_ok=True)

    resultado = fal_client.subscribe(
        "fal-ai/flux-lora-fast-training",
        arguments={
            "images_data_url": images_data_url,
            "trigger_word": pedido["trigger_word"],
            "is_style": bool(pedido.get("is_style", False)),
            "steps": int(pedido.get("steps", 1000)),
        },
        with_logs=True,
    )

    # extrair a URL do .safetensors (chave varia; tentar as conhecidas)
    lora_url = None
    for chave in ("diffusers_lora_file", "lora_file", "safetensors_file"):
        if isinstance(resultado.get(chave), dict) and resultado[chave].get("url"):
            lora_url = resultado[chave]["url"]
            break
    if not lora_url:
        raise RuntimeError(f"LoRA treinado mas URL não encontrada no retorno: {list(resultado)}")

    LORAS_DIR.mkdir(parents=True, exist_ok=True)
    registro = {
        "trigger_word": pedido["trigger_word"],
        "is_style": bool(pedido.get("is_style", False)),
        "steps": int(pedido.get("steps", 1000)),
        "dataset": str(dataset),
        "n_imagens": len(imgs),
        "lora_url": lora_url,
    }
    (LORAS_DIR / f"{pedido['trigger_word']}.json").write_text(
        json.dumps(registro, ensure_ascii=False, indent=2)
    )
    # .safetensors NÃO entra no Git (gitignore) — fica na CDN da fal; registramos a URL
    print(f"OK: LoRA treinado → {lora_url}\n     registro em training/loras/{pedido['trigger_word']}.json")


def geracao(pedido: dict, nome: str) -> None:
    """Gera imagens com 1+ LoRAs aplicados (FLUX.1 dev + LoRA).

    Campos: prompt, loras [{path|url, scale}], image_size, num_images (padrão 2),
            confirmo_custo (bool) OBRIGATÓRIO true.
    """
    loras = [
        {"path": lo.get("url") or lo["path"], "scale": lo.get("scale", 1.0)}
        for lo in pedido.get("loras", [])
    ]
    resp = requests.post(
        "https://fal.run/fal-ai/flux-lora",
        headers={"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"},
        json={
            "prompt": pedido["prompt"],
            "loras": loras,
            "image_size": pedido.get("image_size", {"width": 1216, "height": 832}),
            "num_images": int(pedido.get("num_images", 2)),
        },
        timeout=300,
    )
    resp.raise_for_status()
    imgs = resp.json()["images"]
    for i, im in enumerate(imgs, 1):
        _baixar(im["url"], OUTPUTS_DIR / f"{nome}_v{i}.png")
    print(f"OK: {len(imgs)} variações em outputs/{nome}_v*.png")


COM_TRAVA = {"treino_lora", "geracao"}
TIPOS = {"smoke_test": smoke_test, "treino_lora": treino_lora, "geracao": geracao}


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
            if tipo not in TIPOS:
                raise RuntimeError(f"Tipo desconhecido: {tipo}")
            if tipo in COM_TRAVA and not pedido.get("confirmo_custo"):
                raise RuntimeError(
                    "TRAVA DE CUSTO: este tipo gasta créditos. "
                    'Adicione "confirmo_custo": true ao pedido para liberar.'
                )
            TIPOS[tipo](pedido, nome)
            caminho.rename(caminho.with_name(f"{nome}.done.json"))
        except Exception as exc:  # noqa: BLE001 — registrar qualquer falha no .erro.json
            falhas += 1
            (caminho.with_name(f"{nome}.erro.json")).write_text(
                json.dumps({"pedido": pedido, "erro": str(exc)}, ensure_ascii=False, indent=2)
            )
            caminho.unlink()
            print(f"::warning::Pedido {nome} falhou: {exc}")

    print(f"Concluído. Falhas: {falhas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
