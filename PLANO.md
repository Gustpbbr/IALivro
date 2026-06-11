# PLANO — IA de imagem especializada na coleção

> **Para o agente:** este é o plano que o autor quer que você **avalie, atualize e
> melhore** antes de executar (ver Protocolo de Início no `CLAUDE.md`). Ele foi
> desenhado com a lógica "começar enxuto e barato, validar, depois escalar". O
> objetivo e o universo estão em `UNIVERSO.md`; o que reaproveitar, em
> `INFRAESTRUTURA.md`.

---

## Objetivo

Construir um **Orquestrador de Narrativa Visual**: uma IA de imagem que ilustra os
capítulos dos 11 livros mantendo **consistência rigorosa** de personagens,
cenários e estilo (ver `UNIVERSO.md` §2). O autor escreve/cola o trecho do
capítulo; o sistema gera a ilustração no traço da coleção.

---

## Arquitetura-alvo (híbrida)

```
┌───────────────────────────────────────────────┐
│  AUTOR escreve o trecho do capítulo (PT-BR)    │
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│  "DIRETOR DE ARTE" (LLM via chave Anthropic/   │
│  OpenAI já existentes) → vira prompt técnico,  │
│  injeta trigger words do estilo + personagens  │
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│  MODELO DE IMAGEM na nuvem (Fal.ai/Replicate)  │
│  base FLUX/SDXL + LoRA de estilo + LoRA persona │
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│  Imagem volta → salva em /outputs + R2         │
└───────────────────────────────────────────────┘
```

> **Avaliado em 11/06/2026** (ver `docs/PESQUISA_FABLE5_E_ESTADO_DA_ARTE.md`):
> - **Serviço principal: Fal.ai** (combina LoRA de estilo + personagem nativamente,
>   já treina FLUX.2, tem skill pronta de Claude Code). Replicate como backup.
> - **Modelo base: FLUX.1-dev** para começar (maduro, barato); testar **FLUX.2**
>   em A/B na Fase 1 (geração mais barata + multi-referência).
> - **Licença comercial: resolvida** — imagens geradas via Fal/Replicate podem ser
>   usadas comercialmente nos livros.
> - **Texto-em-imagem** (placas, brasões): gerar com **Nano Banana Pro / Ideogram**,
>   não com FLUX+ControlNet (ver Fase 3).

---

## FASE 1 — Validação enxuta (barata, sem interface) ⭐ COMECE AQUI

Meta: provar que dá para reproduzir o **estilo** e **1–2 personagens** com
consistência, gastando ~US$ 10. Sem construir app ainda.

1. **Reunir o dataset.** O autor tem imagens dos **caps 1–5 do Livro 1** (sobem
   via Google Drive) + 4 imagens de referência em `referencia_visual/imagens/`.
   Organizar em:
   - `/dataset/100_estilo/` — imagens que representam o traço da coleção.
   - `/dataset/200_<personagem>/` — imagens de 1–2 personagens Tier 1
     (sugestão: **João** e **Leônidas/STF**, os mais centrais).
2. **Fabricar o que faltar.** Prática de 2026: não é preciso ter 25–30 imagens
   prontas por personagem — basta **1 boa arte-modelo**; um modelo de edição com
   referência (Qwen-Image-Edit / Nano Banana) fabrica o restante do turnaround
   (ângulos, poses, expressões). O ideal por personagem: 25–30 imagens (mínimo 10).
3. **Legendar (captions).** Para cada imagem, um `.txt` de mesmo nome com a
   **trigger word única no início** (ex.: `estilo_colecao_xyz`, `joao_cidadao_xyz`)
   + descrição. Descrever o que deve poder VARIAR (roupa, fundo, pose) para o
   modelo não grudar isso na identidade do personagem.
4. **Treinar o LoRA de estilo** via API da **Fal.ai**. Custo ~US$ 2–3 por treino
   (Replicate como backup, ~US$ 1,50).
5. **Gerar testes** de cenas dos caps 1–5 e comparar com as imagens originais:
   o traço bate? O personagem se mantém? O agente faz uma triagem automática por
   vision (gerar → comparar com referência → regenerar se houver drift), e o autor
   dá o veredito final. Ajustar captions/peso e re-treinar se preciso.
6. **Decisão de porteira:** só avançar para a Fase 2 quando a consistência estiver
   aprovada pelo autor.

> Nesta fase **não há servidor ligado** — você (agente) dispara o treino/geração
> via API e salva os resultados no repo. Custo de hospedagem = zero.

## Decisões de produto (alinhamento com o autor — em andamento)

- **Variações por cena** (11/06/2026): cada pedido gera múltiplas opções de imagem
  para o autor escolher, não uma única. (Quantidade padrão a definir; impacta custo
  por cena: ~US$ 0,02–0,035 × nº de variações.)
- **Destino: livro digital em HTML, tablet Samsung em modo retrato** (11/06/2026).
  Coluna de texto de 650px (CSS do projeto-mãe). Sem requisitos de impressão.
- **4 perfis de enquadramento** (11/06/2026), nas resoluções nativas do FLUX:
  | Perfil | Resolução de geração |
  |---|---|
  | Tela cheia (retrato) | 896×1440 (alt. 832×1216) |
  | Meia página (paisagem) | 1216×832 |
  | Bloco lateral | 1024×1024 ou 768×1024 |
  | Vinheta panorâmica | 1440×640 (proporção extrema — validar na Fase 1) |

  **Upscale 2x só na variação aprovada** antes de exportar (telas de tablet são
  high-DPI; gerar em ~1MP onde o FLUX rende melhor e ampliar a vencedora).
  A interface (Fase 2) terá menu de perfis travando width×height.
- **Fase 3**: os capítulos existem como HTML estruturado no projeto-mãe — o
  pipeline de lote pode ler o HTML para identificar cenas-chave e o perfil de
  enquadramento de cada imagem.
- **2 variações por cena** como padrão (11/06/2026) — custo ~US$ 0,04–0,07/cena.
- **Texto embutido na imagem (fixo), não HTML sobreposto** (11/06/2026): as
  imagens vivem em boxes fixos no layout; texto reescalável vazaria do box.
  Imagens com texto (placas, títulos, brasões) são geradas/finalizadas com
  Nano Banana Pro/Ideogram + QA letra a letra.
- **Interação pelas duas vias** (11/06/2026): colar o trecho do capítulo (o
  diretor de arte identifica cena/personagens/enquadramento) OU pedido dirigido
  ("cap. 6, João + Leônidas no plenário, meia página"). Mesmo motor, duas entradas.
- **Correção sobre a imagem aprovada** (11/06/2026): edição por
  inpainting/referência (FLUX Kontext / Qwen-Image-Edit / Nano Banana via fal.ai)
  — altera só o trecho errado mantendo o resto intacto. **Promovida da Fase 4
  para a interface da Fase 2** (botão "Corrigir" ao lado de cada variação).
- **Volume por capítulo: variável** conforme o conteúdo — sistema por demanda.
- **Usuário único: só o autor** (11/06/2026). Sem cadastro/multiusuário na
  interface — apenas proteção simples de acesso (a instância no Railway não
  pode ficar aberta para a internet).

> ✅ **Alinhamento de produto concluído em 11/06/2026.**

## FASE 2 — Interface (o "ChatGPT ilustrador")

1. **Backend** (Python) que recebe o texto, chama o "diretor de arte" (LLM) para
   montar o prompt, injeta as trigger words e chama a API de imagem. Para o
   diretor de arte, usar **Opus 4.8 ou Sonnet 4.6** via chave existente (qualidade
   suficiente para trecho→prompt, por uma fração do custo do Fable 5).
2. **Interface de chat** (Gradio/Streamlit para começar — simples; ou frontend
   Vercel depois). Barra lateral para escolher personagem em cena e peso do estilo.
   Backlog: **painel de ajustes finos** (brilho, saturação, temperatura) rodando no
   navegador — corrige tonalidade sem re-gerar a imagem (custo zero de API).
3. **Hospedagem:** reaproveitar a conta **Railway** do autor (ver `INFRAESTRUTURA.md`).
   Padrão Dockerfile/FastAPI do projeto Gus transplanta direto.
4. **Storage:** imagens e modelos no **Cloudflare R2**.

## FASE 3 — Consistência avançada e produção em lote

1. **LoRAs dos demais Tier 1** (lista em `UNIVERSO.md` §6), conforme o autor precisar.
   Regra prática: **máximo 2 LoRAs de personagem por imagem** — cenas de grupo se
   resolvem por composição/inpainting ou por modelo com referência nativa
   (Nano Banana Pro aceita até 14 imagens de referência).
2. **Texto fiel na imagem** (placas, "Livro Dourado", brasões): gerar essas imagens
   específicas com **Nano Banana Pro ou Ideogram** (os melhores em texto legível,
   inclusive português) ou em vetor (Recraft) — substitui a aposta antiga em
   ControlNet de tipografia.
3. **Geração em lote:** dado um capítulo, o sistema identifica as cenas-chave (as
   fichas de handoff e o rastreamento JSON do projeto-mãe ajudam) e gera as imagens
   nomeadas (`cap06_cena1.png`…) para o autor revisar.
4. **Coerência por família** e regras de figurino (ver `referencia_visual/`).

## FASE 4 — Melhoria contínua

1. **Feedback 👍/👎** por imagem → pastas `/feedback/positivo` e `/negativo`.
   Positivos acumulados realimentam re-treinos; negativos viram prompt negativo.
2. **Referências arrastáveis (IP-Adapter):** o autor solta uma textura/cenário e a
   IA usa como referência visual (sem copiar).
3. **Correção pontual (inpainting):** corrigir um pedaço da imagem (letra errada,
   detalhe) sem regenerar tudo.
4. **Dataset vivo:** novas pastas (`150_taverna_capX/`) + botão "Atualizar IA".

---

## Práticas de engenharia adotadas (11/06/2026)

- **Plano antes de código**: mudanças relevantes são propostas e aprovadas pelo
  autor antes da execução (já é o fluxo do Claude Code).
- **Testes no backend (Fase 2)**: `pytest` cobrindo falhas de API (timeout da
  fal.ai → mensagem amigável, nunca tela travada). Fase 1 usa validação leve.
- **Hooks de pre-commit (Fase 2)**: linter/typecheck rodam antes de cada commit.
- **Bibliotecas**: `fal-client` (assíncrono) para treino/geração; `boto3` com
  endpoint da Cloudflare para o R2; Gradio/Streamlit com state management no chat.
- **SEM frameworks de enxame** (Claude Flow/LangGraph/CrewAI) e **sem skills de
  terceiros** (ex.: "superpowers"): os papéis (historiador do universo, diretor de
  arte, crítico visual, porteira de gasto) são etapas de um pipeline Python simples;
  paralelismo usa subagentes nativos do Claude Code. Menos pontos de falha,
  manutenção mais simples.

---

## Custos esperados (confirmar valores atuais)

| Item | Quando | Valor confirmado (jun/2026) |
|---|---|---|
| Treino de LoRA (FLUX, Fal.ai) | por treino | ~US$ 2–3 (Replicate: ~US$ 1,50) |
| Geração de imagem com LoRA | por imagem 1024² | US$ 0,035 (FLUX.1) / US$ 0,021 (FLUX.2) |
| Storage R2 | mensal | centavos até GBs |
| Railway | Fase 2+ | reaproveita conta existente |
| LLM diretor de arte (Opus/Sonnet) | por uso | chave já existente |
| **Fase 1 completa** | único | **~US$ 10–15 de crédito** |
| Projeto completo (estilo + ~15 Tier 1 + re-treinos) | estimativa | ~US$ 50–150 em treinos |

---

## Riscos / decisões em aberto (para você endereçar)

- **Onde os modelos/datasets moram**: dataset pequeno fica no Git (Fase 1);
  migra para R2 quando crescer.
- ~~Modelo base definitivo~~ **DECIDIDO (11/06/2026)**: FLUX.1-dev para começar,
  A/B com FLUX.2 na Fase 1. Serviço: Fal.ai. Licença comercial confirmada.
- **Quantos LoRAs de personagem** valem a pena vs prompt+estilo — começar pelos
  Tier 1 e medir. (Tier 2/3 podem usar referência nativa em vez de LoRA.)
- **Quarteto pop-up** tem estilo cartoon distinto — pode exigir um LoRA de estilo
  próprio (avaliar).
- **Bug de push 403** no ambiente do autor — commitar e dar push cedo e frequente
  (ver `INFRAESTRUTURA.md`).

---

## Primeiro passo concreto

Depois de ler os três documentos e fazer a sua autoavaliação crítica (Protocolo de
Início no `CLAUDE.md`), proponha ao autor o arranque da **Fase 1**: a estrutura de
pastas do dataset e a lista exata de imagens que ele precisa reunir e subir. Não
gere custo nem treine nada antes do "ok" dele.
