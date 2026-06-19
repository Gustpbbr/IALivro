"""FastAPI principal do editor IALivro.

Sub-etapas C2 e C3 do ETAPA_C_ARQUITETURA.md. Sirvo:
- frontend estatico (/static/*)
- API de sessao (/api/sessao/*)
- arquivos auxiliares (fundo_limpo.png, mascaras/, icones/) por sessao

Rodar local:
    cd editor/backend
    uvicorn main:app --reload --port 8000
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from rotas import sessao


RAIZ = Path(__file__).parent
FRONTEND = RAIZ.parent / "frontend"


app = FastAPI(
    title="Editor IALivro",
    description="Editor de descompilacao em camadas. Etapa C do projeto.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessao.router, prefix="/api")


@app.get("/api/saude")
def saude() -> dict:
    return {"ok": True, "versao": app.version}


if FRONTEND.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND), html=True), name="frontend")
