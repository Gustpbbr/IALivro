"""Rotas de sessao: upload, obter, atualizar camada, apagar camada."""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File

import armazem
from modelos import (
    Camada,
    Documento,
    PatchCamada,
    RespostaSessao,
    RespostaUpload,
)


router = APIRouter(prefix="/sessao", tags=["sessao"])


@router.post("/upload", response_model=RespostaUpload)
async def upload(arquivo: UploadFile = File(...)) -> RespostaUpload:
    """Recebe um camadas.json (multipart) e cria sessao."""
    if not arquivo.filename.endswith(".json"):
        raise HTTPException(400, "Arquivo precisa ser .json")

    conteudo = (await arquivo.read()).decode("utf-8")
    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as exc:
        raise HTTPException(400, f"JSON invalido: {exc}")

    try:
        documento = Documento(**dados)
    except Exception as exc:
        raise HTTPException(422, f"Esquema invalido: {exc}")

    sid = armazem.criar(documento)
    return RespostaUpload(sessao_id=sid, documento=documento)


@router.get("/{sid}", response_model=RespostaSessao)
def obter(sid: str) -> RespostaSessao:
    documento = armazem.obter(sid)
    if not documento:
        raise HTTPException(404, "Sessao nao encontrada")
    return RespostaSessao(sessao_id=sid, documento=documento)


@router.patch("/{sid}/camada/{cid}", response_model=Camada)
def atualizar_camada(sid: str, cid: str, patch: PatchCamada) -> Camada:
    if not armazem.obter(sid):
        raise HTTPException(404, "Sessao nao encontrada")
    camada = armazem.atualizar_camada(sid, cid, patch)
    if not camada:
        raise HTTPException(404, "Camada nao encontrada")
    return camada


@router.delete("/{sid}/camada/{cid}")
def apagar_camada(sid: str, cid: str, modo: str = "simples") -> dict:
    """Modos: simples (gratis), refazer (inpainting), estender (outpainting).

    POC: simples remove a camada (frontend revela o fundo_limpo).
    Refazer/estender retornam 501 ate Etapa D estar pronta.
    """
    if modo not in ("simples", "refazer", "estender"):
        raise HTTPException(400, "modo deve ser simples|refazer|estender")

    if not armazem.obter(sid):
        raise HTTPException(404, "Sessao nao encontrada")

    if modo == "simples":
        ok = armazem.remover_camada(sid, cid)
        if not ok:
            raise HTTPException(404, "Camada nao encontrada")
        return {"ok": True, "modo": "simples"}

    raise HTTPException(
        501,
        f"Modo {modo} ainda nao implementado (Etapa D em construcao)",
    )
