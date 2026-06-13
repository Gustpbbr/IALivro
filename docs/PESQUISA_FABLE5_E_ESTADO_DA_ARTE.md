# Pesquisa — Fable 5, Claude Code e o estado da arte de IA de imagem (junho/2026)

> Pesquisa profunda feita em 11/06/2026 pelo agente (Claude Fable 5 no Claude Code), a pedido
> do autor, antes de iniciar a Fase 1 do projeto. Quatro frentes pesquisadas em paralelo na web
> (anúncios oficiais, benchmarks independentes, opiniões de usuários e documentação técnica),
> cruzadas com a documentação oficial da API da Anthropic.
>
> **Nota de método:** muitos sites bloquearam leitura direta (HTTP 403); nesses casos a
> informação vem dos resumos indexados pelos buscadores. Números de "% de consistência" vindos
> de blogs comerciais devem ser lidos com cautela. Lacunas estão marcadas explicitamente.

---

## 1. O que é o Fable 5 — e o que ele faz de verdade

**Fatos confirmados (documentação oficial + imprensa):**

- Lançado em **9 de junho de 2026**, é o primeiro modelo da família Claude 5 e da classe
  "Mythos" — acima do Opus 4.8 em capacidade. Existe um irmão, o Claude Mythos 5 (mesmo modelo,
  menos salvaguardas, acesso restrito).
- **Contexto de 1 milhão de tokens** (dá para carregar capítulos inteiros + todos os guias
  visuais de uma vez) e **até 128 mil tokens de saída**.
- **Vision de alta resolução**: lê imagens de até **2576px no lado maior** e analisa
  **múltiplas imagens na mesma conversa** — o caso de uso "comparar/contrastar imagens" é
  citado na documentação oficial. Custo: até ~4784 tokens por imagem grande.
- **Foco declarado**: trabalho agêntico de longo horizonte — "quanto mais longa e complexa a
  tarefa, maior a vantagem". Turnos de muitos minutos são normais e esperados.
- **Preço (API)**: US$ 10/milhão de tokens de entrada e US$ 50/milhão de saída — 2× o Opus 4.8.
  O tokenizer novo gasta **~30% mais tokens** pelo mesmo conteúdo ("tokenizer tax").
- **Salvaguardas**: classificadores podem recusar pedidos em cibersegurança e biologia
  (irrelevantes para este projeto); quando recusam, há fallback para o Opus 4.8.

**Benchmarks (números do lançamento; comparações entre fornecedores têm ruído de 1–3 pontos):**

| Benchmark | Fable 5 | Opus 4.8 | GPT-5.5 | Gemini 3.1 Pro |
|---|---|---|---|---|
| SWE-Bench Pro (engenharia de software) | **80,3%** | 69,2% | 58,6% | 54,2% |
| FrontierCode Diamond | **29,3%** | 13,4% | 5,7% | — |
| GPQA Diamond (ciência) | 91,3% | — | 92,8% | **94,3%** |
| "Senior Engineer" (Every) | **91/100** | 63 | 62 | — |

**O que usuários reais dizem (Reddit/HN/X/blogs, primeiros dias):**

- 👍 Diffs "mais cirúrgicos", tarefas em menos turnos (um dev relatou o mesmo resultado com
  metade dos tokens); fica na tarefa por mais tempo e **valida o próprio trabalho** antes de
  declarar pronto; melhor modelo de coding segundo várias avaliações independentes.
- 👎 Custo alto quando usado via API (tokenizer + preço 2×); lentidão no primeiro token
  (pensa muito antes de responder — melhor para trabalho assíncrono do que chat rápido);
  **falsos positivos dos classificadores** foi a maior reclamação prática (palavras como
  "câncer" sinalizadas em contexto acadêmico) — a Anthropic admitiu e ajustou.

> **Relevância para o autor:** dentro do Claude Code com assinatura, o custo por token da API
> não se aplica diretamente — os limites são os do plano. O custo de API só importa se
> usarmos o Fable 5 como "diretor de arte" via chave de API na Fase 2 (e aí o Opus 4.8 ou o
> Sonnet 4.6 provavelmente bastam, por uma fração do preço).

---

## 2. O que o Fable 5 + Claude Code conseguem fazer NESTE projeto

| Tarefa do plano | Consegue? | Evidência |
|---|---|---|
| Escrever todo o código do pipeline (Python, APIs, backend, interface) | ✅ Sim | Ponto mais forte do modelo (benchmarks + relatos) |
| Chamar APIs da Fal.ai/Replicate para treinar LoRA e gerar imagens | ✅ Sim | Padrão estabelecido: a Replicate tem MCP oficial; a fal.ai tem skill de Claude Code pronta (`fal-train`, ~US$2/treino) |
| Gerar captions do dataset (descrições + trigger words) | ✅ Sim | Vision lê cada imagem e descreve; trabalho clássico de LLM |
| **Checar consistência de personagem via vision** | ⚠️ Sim, com limites | Caso documentado: 32 ilustrações consistentes geradas via Claude Code comparando cada output contra referência e regenerando quando havia drift. Pega bem o drift **grosseiro** (cor errada, roupa diferente, estilo mudou); diferenças **finas** de traço/tonalidade são menos confiáveis (paper acadêmico: estilo e estética são as dimensões onde LLM-juiz mais desalinha do humano). O autor continua sendo o aprovador final. |
| Operar autonomamente por longos períodos | ✅ Sim | Especialidade do Fable 5 ("trabalho de 2 meses em 1 dia" no marketing; relatos reais de execuções de 36h) |
| **Gerar imagens nativamente** | ❌ Não | Confirmado pela Anthropic: Claude analisa imagens mas não gera pixels. A geração é dos modelos de imagem (FLUX etc.) via API — exatamente como o plano prevê |
| **Treinar modelos localmente** | ❌ Não | Este ambiente não tem GPU; treino é via API de nuvem — como o plano prevê |

**Atritos práticos conhecidos** (de quem já orquestrou pipelines de imagem com Claude Code):
jobs longos de treino pedem fila + webhooks em vez de espera bloqueante; salvar seed + template
de prompt travado é essencial para reprodutibilidade; MCPs com dezenas de tools incham o
contexto (a Replicate criou o "Code Mode" exatamente para isso).

**Sobre não-programadores:** o fenômeno "vibe coding" é real (63% dos usuários não têm
background de programação), mas os travamentos acontecem sempre nos mesmos lugares — deploy,
CI/CD, variáveis de ambiente. No nosso arranjo isso fica comigo (Engenheiro); o papel do autor
(Diretor Criativo) está protegido desses atritos.

---

## 3. Estado da arte: consistência de personagem (junho/2026)

**A grande mudança de 2025–2026:** surgiram modelos com **referência de personagem nativa** —
você dá imagens do personagem e ele mantém a identidade sem treinar nada:

- **FLUX.2** (Black Forest Labs, nov/2025): até 10 imagens de referência; texto-em-imagem
  muito melhor que o FLUX.1. Variantes: pro (API), dev (aberto, 32B), klein (leve, 4B/9B).
- **Nano Banana Pro / Gemini 3 Pro Image** (Google): até 14 referências; apontado como **o
  melhor para texto legível dentro da imagem, inclusive em português** — relevante para
  placas, brasões e o "Livro Dourado".
- **GPT Image 2** (OpenAI): identidade persistente, mas histórico de drift com múltiplos
  personagens na cena.
- **Qwen-Image-Edit** (Alibaba, aberto): muito usado para **fabricar datasets multi-ângulo**
  de um personagem a partir de uma única arte-modelo.
- SDXL e SD 3.5 saíram das listas de ponta; a comunidade migrou para FLUX e Qwen.

**LoRA ainda é o caminho? Resposta nuançada:**

- Para poucos personagens/cenas, a referência nativa **substituiu o LoRA**.
- Para o nosso caso — **61 personagens, 11 livros, centenas de ilustrações no mesmo traço** —
  as fontes ainda apontam **LoRA como o método mais confiável em escala**: reprodutível,
  versionável e barato por imagem (referência nativa degrada com vários personagens na cena
  e custa mais por geração).
- IP-Adapter/InstantID praticamente sumiram das recomendações (InstantID é só rosto humano —
  inútil para animais antropomórficos).
- **Consenso emergente: abordagem híbrida** — usar Qwen-Edit/Nano Banana para *fabricar* o
  dataset multi-ângulo de cada personagem, e treinar LoRA de estilo + LoRAs de personagem
  sobre FLUX. Isso resolve nosso maior gargalo: não precisamos de 10–20 imagens prontas de
  cada personagem; precisamos de **1 boa arte-modelo** e o resto se fabrica.

**Práticas recomendadas (treino FLUX):** 25–30 imagens por personagem é o ideal (10 é o
mínimo); trigger word única no início de cada caption; descrever nos captions o que deve poder
variar (roupa, fundo, pose) para não "grudar" no personagem; LoRA de estilo separado
(peso ~0,6) + personagem (peso ~0,9); **máximo 2 LoRAs de personagem por imagem** — cenas de
grupo se resolvem por composição/inpainting ou pelos modelos de referência nativa.

---

## 4. Fal.ai vs Replicate — custos e licença

| Item | Fal.ai | Replicate |
|---|---|---|
| Treino LoRA FLUX.1 | ~US$ 2–3 (fast training; portrait trainer US$0,0024/step) | **~US$ 1,46** (fast-flux-trainer, ~2 min) |
| Treino LoRA FLUX.2 | US$ 0,008/step (✅ já suporta) | Não encontrado trainer oficial FLUX.2 |
| Geração com LoRA | US$ 0,035/MP (FLUX.1) · **US$ 0,021/MP (FLUX.2)** | FLUX schnell US$ 0,003/img; fine-tunes por tempo de GPU |
| Múltiplos LoRAs por chamada | ✅ Nativo (array `loras` com pesos) | `extra_lora` (1 extra) ou modelo comunitário (até 20) |
| Velocidade | Mais rápida (cold start ~0,5s) | Fila mais lenta, mas async mais maduro |
| Catálogo | Adota modelos novos primeiro | ~1000+ modelos comunitários |

**Licença comercial (crítico para os livros): ✅ resolvido.** A licença do FLUX.1-dev
restringe *hospedar o modelo*, não *as imagens geradas* — "outputs podem ser usados para
qualquer fim, inclusive comercial". E tanto a fal quanto a Replicate têm acordo com a Black
Forest Labs cobrindo o uso comercial via API. Para risco zero absoluto existe o FLUX.1-schnell
(Apache 2.0). **Ilustrar livros comerciais gerando via fal/Replicate é seguro.**

**Estimativa para o projeto:** Fase 1 (1 LoRA de estilo + 2 de personagem + ~100 imagens de
teste) ≈ **US$ 10–15** — bate com o plano. Projeto completo (estilo + ~15 personagens Tier 1 +
re-treinos) ≈ US$ 50–150 em treinos, + centavos por imagem gerada.

---

## 5. Implicações para o PLANO.md (recomendações)

1. **A arquitetura do plano está validada** — diretor de arte (LLM) → modelo de imagem com
   LoRAs via API → revisão. Nada a mudar na espinha dorsal. ✅
2. **Fal.ai como serviço principal** (múltiplos LoRAs nativos, FLUX.2, skill pronta de Claude
   Code), Replicate como alternativa/backup. A "única conta nova" do INFRAESTRUTURA.md.
3. **Modelo base**: começar com **FLUX.1-dev** (maduro, barato, ferramentas estáveis) e
   avaliar FLUX.2 (geração mais barata, multi-referência) num teste A/B na própria Fase 1.
4. **Novidade que muda a Fase 1**: usar modelo de edição (Qwen-Image-Edit / Nano Banana) para
   **fabricar os datasets multi-ângulo** dos personagens a partir das artes existentes —
   reduz drasticamente o que o autor precisa reunir.
5. **Texto-em-imagem** (placas, brasões, "Livro Dourado"): não depender do FLUX —
   usar **Nano Banana Pro ou Ideogram** para essas imagens específicas, ou vetor (Recraft).
   Atualiza a aposta da Fase 3 em "ControlNet de tipografia".
6. **Cenas de grupo** (vários dos 61 animais juntos): planejar desde já composição/inpainting
   ou referência nativa — máx. 2 LoRAs de personagem por geração.
7. **QA visual com vision**: incluir no pipeline o loop "gerar → comparar com referência →
   regenerar se drift" (caso documentado funciona), mantendo o autor como aprovador final.
8. **Diretor de arte na Fase 2**: usar Opus 4.8/Sonnet 4.6 via API (não Fable 5) — qualidade
   suficiente para converter trecho→prompt por uma fração do custo.

---

## Fontes principais

**Fable 5:** anthropic.com/news/claude-fable-5-mythos-5 · techcrunch.com (09/06/2026) ·
vellum.ai/blog/claude-fable-5-and-mythos-5-benchmarks-explained · every.to/vibe-check ·
simonwillison.net/2026/Jun/9/claude-fable-5 · news.ycombinator.com/item?id=48464975 ·
fortune.com (10/06/2026, refusals) · openrouter.ai/anthropic/claude-fable-5 ·
exame.com e olhardigital.com.br (cobertura PT)

**Claude Code / vision:** platform.claude.com/docs/en/build-with-claude/vision ·
support.claude.com (Claude não gera imagens) · arxiv.org/html/2509.12750v1 (LLM-as-judge) ·
aiphotogenerator.net (caso das 32 ilustrações) · github.com/replicate/replicate-mcp-code-mode ·
claudemarketplaces.com (skill fal-train) · scientificamerican.com (vibe coding) ·
alura.com.br/artigos/claude-code-para-criar-site

**Consistência de personagem:** bfl.ai/models/flux-2 · blog.google (Nano Banana Pro) ·
huggingface.co/Qwen/Qwen-Image-Edit-2511 · apatero.com (guias LoRA) · civitai.com/articles/7203 ·
arxiv.org/html/2402.16843v2 (Multi-LoRA) · docs.midjourney.com (Omni Reference) ·
allaboutai.com e prompting.systems (livros ilustrados com IA)

**Fal/Replicate/licença:** fal.ai/models e fal.ai/pricing · replicate.com/blog/fine-tune-flux ·
replicate.com/docs/guides/extend/working-with-loras ·
huggingface.co/black-forest-labs/FLUX.1-dev (licença + discussão #136) · bfl.ai/licensing ·
scopeful.org/blog/fal-vs-replicate · getdeploying.com/fal-ai-vs-replicate
