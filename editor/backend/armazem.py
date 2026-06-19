"""Armazem em memoria de sessoes (POC). Producao usa R2 + persistencia."""

import io
from typing import Optional
from uuid import uuid4

from PIL import Image

from modelos import Documento, Camada, PatchCamada


_sessoes: dict[str, Documento] = {}
_fundos: dict[str, Image.Image] = {}


def criar(documento: Documento) -> str:
    sid = uuid4().hex[:12]
    _sessoes[sid] = documento
    return sid


def obter(sid: str) -> Optional[Documento]:
    return _sessoes.get(sid)


def salvar_fundo(sid: str, bytes_imagem: bytes) -> bool:
    if sid not in _sessoes:
        return False
    _fundos[sid] = Image.open(io.BytesIO(bytes_imagem))
    return True


def obter_fundo(sid: str) -> Optional[Image.Image]:
    return _fundos.get(sid)


def atualizar_camada(sid: str, cid: str, patch: PatchCamada) -> Optional[Camada]:
    doc = _sessoes.get(sid)
    if not doc:
        return None
    for i, camada in enumerate(doc.camadas):
        if camada.id != cid:
            continue
        dados = camada.model_dump()
        atualizacao = patch.model_dump(exclude_unset=True)
        # Estilo é dict aninhado — mergeia ao invés de sobrescrever
        if "estilo" in atualizacao and atualizacao["estilo"] is not None:
            base = dados.get("estilo") or {}
            base.update(atualizacao["estilo"])
            atualizacao["estilo"] = base
        dados.update(atualizacao)
        nova = Camada(**dados)
        doc.camadas[i] = nova
        return nova
    return None


def remover_camada(sid: str, cid: str) -> bool:
    doc = _sessoes.get(sid)
    if not doc:
        return False
    antes = len(doc.camadas)
    doc.camadas = [c for c in doc.camadas if c.id != cid]
    return len(doc.camadas) < antes
