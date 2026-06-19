"""Modelos Pydantic do esquema camadas.json v1.

Reflete ESQUEMA_CAMADAS.md. Editor valida toda entrada contra estes modelos.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


TipoCamada = Literal["texto", "caixa", "icone", "cena", "linha_divisoria"]


class BBox(BaseModel):
    x: int
    y: int
    w: int
    h: int


class EstiloTexto(BaseModel):
    cor: str = "#000000"
    cor_fundo_local: Optional[str] = None
    tamanho_px: int = 16
    fonte_classe: Literal["serif", "sans_serif", "display"] = "serif"
    fonte_id: Optional[str] = None
    peso: Literal["normal", "bold", "light"] = "normal"
    alinhamento: Literal["left", "center", "right"] = "left"


class Camada(BaseModel):
    id: str
    tipo: TipoCamada
    bbox: BBox
    z: Optional[int] = None
    mascara: Optional[str] = None

    # Comuns opcionais por tipo
    conteudo: Optional[str] = None
    estilo: Optional[EstiloTexto] = None
    cor_fundo: Optional[str] = None
    cor_borda: Optional[str] = None
    espessura_borda: Optional[int] = 0
    raio_canto: Optional[int] = 0
    filhos: Optional[list[str]] = None
    arquivo_recorte: Optional[str] = None
    descricao: Optional[str] = None
    cor: Optional[str] = None
    espessura: Optional[int] = None
    estilo_linha: Optional[Literal["solida", "tracejada"]] = None


class Dimensoes(BaseModel):
    largura: int
    altura: int


class Documento(BaseModel):
    schema_version: int = 1
    imagem_origem: str
    dimensoes: Dimensoes
    fundo_limpo: str
    camadas: list[Camada]


class PatchCamada(BaseModel):
    """Aplicado via PATCH /sessao/{sid}/camada/{cid}."""

    conteudo: Optional[str] = None
    bbox: Optional[BBox] = None
    estilo: Optional[EstiloTexto] = None
    cor_fundo: Optional[str] = None
    cor_borda: Optional[str] = None
    espessura_borda: Optional[int] = None
    raio_canto: Optional[int] = None
    cor: Optional[str] = None
    espessura: Optional[int] = None


class RespostaUpload(BaseModel):
    sessao_id: str
    documento: Documento


class RespostaSessao(BaseModel):
    sessao_id: str
    documento: Documento
