# Editor IALivro — Etapa C

Editor web pra editar imagens descompiladas pela POC (Etapa B). Implementa as sub-etapas **C2-C5** do `ETAPA_C_ARQUITETURA.md`:

- **C2** — Backend FastAPI com rotas básicas ✅
- **C3** — Upload de `camadas.json` + render no canvas SVG ✅
- **C4** — Edição de texto (conteúdo, fonte, cor, tamanho, peso) ✅
- **C5** — Edição de caixas (cor fundo, borda, raio, posição) ✅

Modos 🟡 (refazer) e 🔵 (estender) ficam pra Etapa D quando o inpainting Fal estiver acessível via Actions.

## Pastas

```
editor/
├── mockup/                # Mockup estático (HTML+JS sem backend)
├── frontend/              # SPA real do editor
│   ├── index.html         # Upload + canvas + painel
│   ├── css/
│   │   ├── tokens.css     # Design system (variáveis CSS)
│   │   └── editor.css     # Componentes
│   ├── js/
│   │   ├── editor.js      # Entrada principal
│   │   ├── api.js         # Wrapper REST
│   │   ├── estado.js      # Store em memória
│   │   ├── painel.js      # Painel de propriedades
│   │   ├── toast.js       # Notificações
│   │   └── camadas/
│   │       ├── comum.js   # Render SVG das bboxes
│   │       └── fontes.js  # Catálogo de fontes
│   └── static/            # Assets (fundo_demo.png, etc.)
└── backend/               # FastAPI
    ├── main.py            # App + montagem do frontend
    ├── modelos.py         # Pydantic do esquema v1
    ├── armazem.py         # Sessões em memória (POC)
    ├── rotas/
    │   └── sessao.py      # Upload, get, patch, delete
    └── requirements.txt
```

## Rodar

```bash
cd editor/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Acessar: `http://localhost:8000/`

## Testar fluxo completo

1. Rode `poc_descompilacao/descompila.py` numa imagem (ou use `camadas_demo.json` do mockup adaptado)
2. Abra o editor no navegador
3. Faça upload do `camadas.json` na tela inicial
4. Clique numa camada → painel abre com propriedades
5. Edite (texto, cor, fonte, posição)
6. Toda mudança é persistida via `PATCH /api/sessao/{sid}/camada/{cid}`

## API REST

| Método | Rota | Função |
|---|---|---|
| `POST` | `/api/sessao/upload` | Recebe multipart com `arquivo` (json) + `fundo` (PNG opcional), retorna `sessao_id` |
| `POST` | `/api/sessao/{sid}/fundo` | Anexa fundo depois |
| `GET` | `/api/sessao/{sid}` | Estado atual do documento |
| `PATCH` | `/api/sessao/{sid}/camada/{cid}` | Atualiza campos da camada (merge) |
| `DELETE` | `/api/sessao/{sid}/camada/{cid}?modo=simples\|refazer\|estender` | Apaga camada |
| `POST` | `/api/sessao/{sid}/exportar?formato=png\|pdf` | Renderiza com Pillow e devolve PNG ou PDF |
| `GET` | `/api/saude` | Healthcheck |

Docs interativas: `http://localhost:8000/docs`

## Próximas sub-etapas

| Sub | Status | Depende de |
|---|---|---|
| C6 — Apagar 🟢 simples | ✅ feito | — |
| C7 — Apagar 🟡 refazer | ⬜ | Fal disponível (Actions) |
| C8 — Apagar 🔵 estender | ⬜ | Fal disponível |
| C9 — Exportação PNG/PDF | ✅ feito | — |
| C10 — Histórico/undo | ⬜ | armazem com versões |
| C11 — Catálogo fontes refinado | ⬜ | uso real |
| C12 — Color grading (E) | ⬜ | escopo Etapa E |

## Renderização (C9)

Backend renderiza com Pillow:

- Fundo: PNG opcional enviado no upload (sem fundo, usa branco)
- Camadas em ordem: cena → caixa → linha → ícone → texto
- Caixas: `ImageDraw.rounded_rectangle` com fill, outline, raio do canto
- Textos: fonte do catálogo (`servicos/fontes.py`), baixada do Google Fonts on-demand pra `editor/backend/dados/fontes/` (gitignored), fallback `DejaVuSans`
- Ícones: paste do `arquivo_recorte` da camada (Etapa B)
- Saída: PNG ou PDF via parâmetro de query
