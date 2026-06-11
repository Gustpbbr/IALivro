# INFRAESTRUTURA — o que JÁ existe e o que falta

> **Para o agente:** o autor levantou a infraestrutura de três projetos antigos
> dele (Fluux, Gus, Dimagem). O resumo abaixo diz o que dá para **reaproveitar**
> neste projeto de IA de imagem e o que precisa ser **criado do zero**. Antes de
> recriar qualquer serviço, **confirme com o autor** se a conta correspondente
> ainda está ativa.

---

## Conclusão de uma linha

**Falta criar exatamente UMA conta nova: um serviço de geração/treino de imagem na
nuvem (Fal.ai ou Replicate).** Todo o resto — hospedagem, chaves de LLM, storage,
repositório — já existe e pode ser reaproveitado.

---

## Mapa de reaproveitamento

| Necessidade deste projeto | Já existe em… | Veredito |
|---|---|---|
| **LLM "diretor de arte" (texto → prompt técnico)** | Projeto **Gus** → `ANTHROPIC_API_KEY` + `OPENAI_API_KEY` | ✅ Reusa direto. Não precisa de chave nova de LLM |
| **Hospedar backend/interface (Fase 2)** | Projeto **Gus** → conta **Railway** (já com cartão e plano pago) | ✅ Reusa — adiciona um serviço novo. Padrão Dockerfile/FastAPI dele transplanta direto |
| **Armazenar imagens + modelos `.safetensors`** | Projeto **Dimagem** → conta **Cloudflare** (habilita o R2) | ✅ Use **Cloudflare R2** (barato, feito p/ arquivos grandes) |
| **Repositório** | Conta GitHub (todos os projetos) | ✅ Repo novo, privado, grátis |
| **Frontend bonito (se quiser, Fase 2+)** | **Fluux** → Vercel · **Dimagem** → Cloudflare Pages | ✅ Reusa quando chegar a hora |
| **MCPs (Drive, GitHub…)** | Conta Claude do autor | ✅ Já disponíveis em qualquer sessão |
| **GPU / API de imagem (treino + geração)** | — Nenhum projeto tem | 🆕 **CRIAR** (única conta nova obrigatória) |

---

## A única coisa a criar

- **Conta na Fal.ai ou na Replicate** (pay-as-you-go).
  - Treino de um LoRA: ~US$ 2–5 por treino.
  - Geração de imagem: ~US$ 0,03 por imagem (modelo FLUX).
  - Precisa de cartão; carregar ~US$ 10 de crédito basta para começar.
- **(Opcional, Fase 1)** provisionar um bucket no **Cloudflare R2** para guardar os
  `.safetensors` e as imagens geradas.

---

## Decisões já tomadas (com base no inventário)

1. **Storage → Cloudflare R2, não Supabase.** O Supabase do autor (projeto Fluux)
   já está no limite de **2 projetos grátis** (prod + staging). A conta Cloudflare
   está livre e o R2 é melhor para arquivos grandes.
2. **Railway só na Fase 2.** Na Fase 1 (treinar + gerar via API, agente orquestrando
   do repo), **não se liga servidor** — zero custo de hospedagem. O Railway entra
   quando o autor quiser o chat rodando 24h.

---

## Alertas herdados do inventário

- ⚠️ **Railway do Gus gasta ~US$ 10–20/mês** com cartão ativo; o serviço
  `gus-mcp-server` só é usado quando o autor abre o Claude Chat. Vale conferir o
  *sleep-on-idle* dele um dia (não é tarefa deste projeto, mas é dinheiro parado).
- ⚠️ **Bug de push 403 recorrente** no ambiente do autor: já travou commits em
  outros projetos (perda de trabalho local não commitado no Gus). **Commite e dê
  push cedo e com frequência** neste projeto para não perder trabalho.
- ⚠️ **Confirmar contas ativas** antes de reusar: o autor precisa checar billing em
  Railway, Cloudflare, Anthropic e OpenAI (só ele vê os painéis logados).
