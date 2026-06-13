"""Passo 2 — Analise semantica do layout via Claude vision."""

import base64
import io
import json
import re
from pathlib import Path
from typing import Any

import anthropic
from PIL import Image


MODELO_PADRAO = "claude-sonnet-4-6"
MAX_TOKENS = 8000


def analisar_layout(
    img: Image.Image,
    prompt_path: Path,
    modelo: str = MODELO_PADRAO,
) -> dict[str, Any]:
    """Manda a imagem pro Claude e devolve o JSON de camadas parseado."""
    cliente = anthropic.Anthropic()

    img_b64 = _imagem_para_base64(img)
    prompt = prompt_path.read_text(encoding="utf-8")

    resposta = cliente.messages.create(
        model=modelo,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    texto = resposta.content[0].text
    dados = _extrair_json(texto)

    dados["_meta"] = {
        "modelo": modelo,
        "tokens_input": resposta.usage.input_tokens,
        "tokens_output": resposta.usage.output_tokens,
    }
    return dados


def _imagem_para_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img_para_enviar = img if img.mode == "RGB" else img.convert("RGB")
    img_para_enviar.save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


def _extrair_json(texto: str) -> dict[str, Any]:
    """Tenta achar bloco JSON na resposta. Aceita resposta crua ou com cerca markdown."""
    texto = texto.strip()

    if texto.startswith("{"):
        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            pass

    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", texto, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    abre = texto.find("{")
    fecha = texto.rfind("}")
    if abre != -1 and fecha != -1 and fecha > abre:
        return json.loads(texto[abre : fecha + 1])

    raise ValueError(f"Nao consegui extrair JSON da resposta:\n{texto[:500]}")


def salvar(dados: dict[str, Any], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
