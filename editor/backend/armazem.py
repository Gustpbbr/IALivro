"""Armazem em memoria de sessoes (POC). Producao usa R2 + persistencia."""

import io
from typing import Optional
from uuid import uuid4

from PIL import Image

from modelos import Documento, Camada, PatchCamada


_sessoes: dict[str, Documento] = {}
_fundos: dict[str, Image.Image] = {}
_originais: dict[str, dict[str, dict]] = {}  # sid -> {camada_id: snapshot_dict}


def criar(documento: Documento) -> str:
    sid = uuid4().hex[:12]
    _sessoes[sid] = documento
    # snapshot por id pra comparar depois
    _originais[sid] = {c.id: c.model_dump() for c in documento.camadas}
    return sid


def obter(sid: str) -> Optional[Documento]:
    return _sessoes.get(sid)


def obter_original(sid: str, cid: str) -> Optional[dict]:
    return _originais.get(sid, {}).get(cid)


def camadas_alteradas(sid: str) -> list[str]:
    doc = _sessoes.get(sid)
    snaps = _originais.get(sid)
    if not doc or not snaps:
        return []
    mudados = []
    ids_atuais = set()
    for c in doc.camadas:
        ids_atuais.add(c.id)
        original = snaps.get(c.id)
        if original is None:
            mudados.append(c.id)  # nova
            continue
        if c.model_dump() != original:
            mudados.append(c.id)
    # tambem retorna ids que foram removidos
    for cid_orig in snaps:
        if cid_orig not in ids_atuais:
            mudados.append(cid_orig)
    return mudados


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
