# ETAPA C — Arquitetura do Editor Web

> Primeira proposta de arquitetura. Pode ser refinada quando o autor testar o mockup.

## Objetivo

Aplicação web que carrega o `camadas.json` (saída da Etapa B) + `fundo_limpo.png` + ícones recortados, e permite ao autor editar texto, fonte, cor, posição e tamanho de cada camada, com previsão de exportação final.

Mobile-first (autor edita do celular) com suporte a desktop.

---

## Stack escolhida

| Componente | Escolha | Por quê |
|---|---|---|
| **Backend** | Python + FastAPI | Mesmo padrão do projeto Gus já em uso; integra com `descompila.py` |
| **Frontend** | HTML/CSS/JS vanilla + Konva.js | Konva é canvas 2D maduro, ótimo pra editor visual com camadas; vanilla evita peso de framework pra POC |
| **Editor de texto** | `contenteditable` em SVG foreignObject | Permite digitação nativa do celular sem mexer com canvas-text |
| **Storage** | Cloudflare R2 (já existente) | Imagens, máscaras e JSONs ficam lá; URLs pré-assinadas |
| **Hosting** | Railway (conta existente) | Dockerfile/FastAPI; deploy fácil |
| **Fontes** | Catálogo curado (Google Fonts + fontes do projeto) | Mapeamento `fonte_classe` → fonte real |

### Por que NÃO outras opções

- **React/Vue/Svelte:** overhead pra POC; podemos migrar depois se virar app sério
- **Fabric.js:** alternativa a Konva, igualmente boa; escolhi Konva por mobile melhor
- **Tldraw:** ótimo, mas é editor genérico; não controla bem fluxo de "camadas vindas de descompilação"
- **Tauri/Electron:** desktop-only, autor quer mobile

---

## Componentes principais

```
┌─────────────────────────────────────────────────┐
│  CANVAS (Konva.js)                               │
│  ┌─────────────────────────────────────────┐    │
│  │ Layer: fundo (raster, não interativo)   │    │
│  ├─────────────────────────────────────────┤    │
│  │ Layer: boxes (vetorial, clicáveis)       │    │
│  ├─────────────────────────────────────────┤    │
│  │ Layer: ícones (raster transparente)      │    │
│  ├─────────────────────────────────────────┤    │
│  │ Layer: textos (SVG foreignObject)        │    │
│  ├─────────────────────────────────────────┤    │
│  │ Layer: seleção/handles (UI)              │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  PAINEL DE PROPRIEDADES                          │
│  (mobile: aparece embaixo; desktop: à direita)   │
│                                                  │
│  Quando uma camada é selecionada:                │
│  - Texto: conteúdo, fonte, tamanho, cor          │
│  - Caixa: cor fundo, borda, raio                 │
│  - Ícone: posição, tamanho, substituir           │
│  - Todos: 🟢/🟡/🔵 apagar                          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  TOPBAR                                          │
│  [Upload .json] [Exportar PNG] [Histórico]       │
└─────────────────────────────────────────────────┘
```

---

## Fluxo de dados

```
Usuário → upload camadas.json
  ↓
Backend valida schema, retorna assets (fundo, ícones)
  ↓
Frontend renderiza Canvas + camadas
  ↓
Usuário edita (texto, cor, posição, apagar)
  ↓
Mudanças atualizam estado local (camadas.json em memória)
  ↓
Auto-save a cada N segundos no backend
  ↓
Usuário clica "Exportar"
  ↓
Backend renderiza canvas final no servidor (Pillow ou Playwright headless)
  ↓
Polish pass opcional (Etapa D) → PNG/PDF final
```

---

## Organização de pastas

```
editor/
├── backend/
│   ├── main.py                # FastAPI app
│   ├── rotas/
│   │   ├── upload.py          # POST /upload (recebe JSON)
│   │   ├── editar.py          # PATCH /sessao/{id}/camada/{cid}
│   │   ├── apagar.py          # DELETE /sessao/{id}/camada/{cid}?modo=simples|refazer|estender
│   │   └── exportar.py        # POST /sessao/{id}/exportar
│   ├── servicos/
│   │   ├── inpaint.py         # Reaproveita poc_descompilacao/etapas/inpaint.py
│   │   └── renderizar.py      # Compõe camadas em PNG final
│   ├── modelos.py             # Pydantic do esquema
│   └── storage.py             # R2 client
├── frontend/
│   ├── index.html             # SPA single-page
│   ├── style.css              # Mobile-first
│   ├── js/
│   │   ├── editor.js          # Konva setup + lógica
│   │   ├── camadas/
│   │   │   ├── texto.js
│   │   │   ├── caixa.js
│   │   │   ├── icone.js
│   │   │   └── cena.js
│   │   ├── propriedades.js    # Painel lateral
│   │   ├── api.js             # Wrapper das chamadas REST
│   │   └── estado.js          # Store em memória
│   └── fontes/                # Fontes web do catálogo
├── Dockerfile
└── README.md
```

---

## Princípios de UX

1. **Toque primeiro.** Tudo precisa funcionar com dedo grande no celular. Handles de redimensionamento maiores que o desktop manda.
2. **Apagar tem três cliques diferentes.** Botão 🟢 padrão grande. 🟡 e 🔵 escondidos em "..." (custam dinheiro/tempo).
3. **Auto-save é silencioso.** Indicador discreto. Nunca trava a UI.
4. **Histórico (undo) é local primeiro.** Backend salva versões, mas undo imediato vem do estado.
5. **Catálogo de fontes pequeno e curado.** Não enche o autor de 200 opções; 6-8 fontes bem escolhidas (2 serif, 2 sans, 2 display, 2 mono).
6. **Cores via paleta do projeto.** `SISTEMA_CORES_COMPLETO_v2.md` vira o seletor padrão; "outras cores" via picker fica como secundário.

---

## Etapas internas da Etapa C

| Sub-etapa | O quê | Prioridade |
|---|---|---|
| C1 | Mockup HTML estático interativo (sem backend, fake data) | 🔥 primeira |
| C2 | Backend FastAPI + rotas básicas | alta |
| C3 | Integração: upload `camadas.json` + render no canvas | alta |
| C4 | Edição de texto (conteúdo, fonte, cor, tamanho) | alta |
| C5 | Edição de caixas (cor, borda, raio, redimensionar) | alta |
| C6 | Apagar 🟢 (revela fundo_limpo) | alta |
| C7 | Apagar 🟡 (chama inpaint via backend) | média |
| C8 | Apagar 🔵 (outpaint) | média |
| C9 | Exportação PNG/PDF | alta |
| C10 | Histórico de edição + undo | média |
| C11 | Catálogo de fontes refinado | média |
| C12 | Color grading básico (E) | baixa |

C1 vai junto deste commit — é o mockup que o autor vai ver no celular.

---

## Decisões pendentes

1. Auto-save em segundos (sugerido: 5s)? Ou a cada mudança?
2. Onde guardar sessões: R2, banco SQLite local no Railway, ou ambos?
3. Vamos suportar múltiplas imagens por sessão (ex.: 12 páginas de um capítulo) ou uma por vez?
4. Polish pass (Etapa D) é botão explícito ou rodado automático no export?

Essas ficam pra discussão depois do autor testar o C1.
