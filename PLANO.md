# PLANO v2 — Editor de Composição com Descompilação por IA

> **Mudança de rota (13/06/2026):** o foco do projeto passou de "gerar imagens via Fal.ai + LoRAs" para "**editar imagens prontas do ChatGPT em camadas, com auxílio de IA**". A geração de imagem fica no ChatGPT (qualidade superior). O esforço de engenharia vai todo para o editor.
>
> O plano anterior (Fases 1-4 com Fal.ai + LoRAs como núcleo) foi arquivado em [`historico/PLANO_v1_geracao_fal.md`](historico/PLANO_v1_geracao_fal.md). Os documentos `UNIVERSO.md`, `INFRAESTRUTURA.md`, `SISTEMA_CORES_COMPLETO_v2.md` e os dois `GUIA_*` continuam válidos.

---

## Objetivo

Construir um **editor web** que aceita uma imagem raster gerada pelo ChatGPT (infográfico, prancha, cena ilustrada com texto e elementos gráficos) e a "explode" em **camadas editáveis**: texto, boxes, ícones, cena de fundo. O autor edita texto, fonte, cor, tamanho de box, paleta — e a IA recompõe a imagem final com qualidade preservada.

A geração inicial das imagens **continua sendo feita no ChatGPT**, alimentada pelas pranchas dos 61 personagens (Etapa A).

---

## Por que mudou

| Antes | Agora |
|---|---|
| Fal.ai + LoRAs treinados gerariam as imagens | ChatGPT gera; qualidade visual é superior |
| Consistência via LoRAs treinados em personagens | Consistência via pranchas no prompt do ChatGPT (já funciona) |
| Editor era a Fase 4 (longe) | Editor vira o **foco principal** |
| Fal.ai era infra de geração | Fal.ai pode continuar como infra de **modelos auxiliares** (SAM, inpainting, polish pass) |

**O que o ChatGPT erra (e o editor resolve):** boxes, textos, tons de imagem (filtro amarelo recorrente). É exatamente onde a edição pós-geração agrega.

---

## Arquitetura-alvo

```
┌──────────────────────────────────────────────────┐
│ AUTOR gera a imagem no ChatGPT (com pranchas)    │
│ → faz upload no editor                            │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│ PIPELINE DE DESCOMPILAÇÃO (backend Python)        │
│  • Vision (Claude/GPT-4V): entende o layout       │
│  • SAM 2: segmenta formas/ícones/regiões          │
│  • OCR (PaddleOCR): extrai texto + bbox + estilo  │
│  • Font matching: identifica fonte mais próxima   │
│  • Inpainting (Fal.ai): reconstrói fundo limpo    │
│  → devolve JSON de camadas + assets               │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│ EDITOR WEB (frontend canvas/SVG)                  │
│  • Camadas visíveis e clicáveis                   │
│  • Edição de texto, fonte, cor, tamanho           │
│  • Boxes redimensionáveis com cor/borda           │
│  • Color grading (resolver filtro amarelo)        │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│ POLISH PASS (img2img strength baixo)              │
│  Limpa bordas, integra elementos editados         │
│  → PNG/PDF final                                  │
└──────────────────────────────────────────────────┘
```

---

## Stack proposta

**Backend:**
- Python + FastAPI (já planejado)
- Vision/Layout: Claude (Anthropic API, chave existente)
- Segmentação: SAM 2 via Fal.ai
- OCR: PaddleOCR (ou EasyOCR)
- Inpainting: LaMa ou SD inpaint via Fal.ai
- Polish pass: FLUX/SDXL img2img via Fal.ai

**Frontend:**
- Web (mobile + desktop, mesmo código)
- Canvas editor: **Konva.js** (recomendado) ou Fabric.js
- SVG pra vetores de boxes/formas

**Infra:**
- Railway (hospedagem do backend, conta existente)
- Cloudflare R2 (storage de imagens, conta existente)

---

## Roadmap

| Etapa | Status | O quê | Critério de "pronto" |
|---|---|---|---|
| **0 — Fundação** | ✅ feita | Docs, briefing, paleta, guias visuais | — |
| **A — Pranchas v2** | 🔄 em andamento (autor) | 61 fichas no formato v2; servem de input pro ChatGPT | Pranchas João + Leônidas + estilo entregues |
| **B — POC do pipeline de descompilação** | ⬜ | Script Python que recebe 1 PNG e devolve JSON de camadas + fundo limpo. Sem UI. | JSON identifica textos, boxes, cena com >80% de precisão visual |
| **C — Editor web (MVP)** | ⬜ | Interface básica: upload, exibir camadas, editar texto/fonte/cor, mover/redimensionar box | Autor consegue editar a imagem de exemplo do ChatGPT |
| **D — Inpainting & polish generativo** | ⬜ | Reconstrói fundo quando move/remove elemento + pass final pra limpar bordas | Saída final indistinguível de imagem nativa |
| **E — Color grading** | ⬜ | Controles de temperatura, saturação, tinta (resolve filtro amarelo do ChatGPT) | Autor consegue neutralizar tons em 1 clique |
| **F — Produção real** | ⬜ | Integrar no fluxo dos 11 livros, exportação PDF, presets por livro | 1 capítulo completo editado de ponta a ponta |

### Backlog / talvez

- **LoRAs no Fal.ai**: só se ChatGPT API virar caro ou inconsistente em escala
- **App mobile nativo**: só se a versão web no celular ficar limitada
- **Editor de composição multi-página**: pra produzir o livro inteiro num único arquivo
- **Feedback 👍/👎** em cada edição pra realimentar prompts

---

## Princípios

1. **Cada etapa entrega algo testável sozinha.** B funciona no terminal antes de C. C funciona sem D.
2. **Começar pelo backend.** Se a IA não conseguir separar bem as camadas, a UI não importa.
3. **Web first.** Funciona no celular e no desktop com mesmo código.
4. **Não inventar consistência.** O ChatGPT + pranchas já resolvem personagens. Não recriar isso à toa.
5. **Fal.ai vira infra auxiliar.** Não pra gerar do zero — só pra SAM, inpaint e polish.

---

## Próximo passo concreto

Iniciar a **Etapa B** com a especificação em [`ETAPA_B_POC_DESCOMPILACAO.md`](ETAPA_B_POC_DESCOMPILACAO.md). Usar a imagem de exemplo do ChatGPT (Constituição + PM/Defensoria Pública) como caso de teste inicial.
