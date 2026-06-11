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

> **Avalie:** os nomes de modelos/serviços abaixo são de meados de 2026 e podem ter
> evoluído. Verifique o estado da arte (modelo base com melhor consistência +
> melhor texto-na-imagem, melhor custo de treino) antes de fixar.

---

## FASE 1 — Validação enxuta (barata, sem interface) ⭐ COMECE AQUI

Meta: provar que dá para reproduzir o **estilo** e **1–2 personagens** com
consistência, gastando ~US$ 10. Sem construir app ainda.

1. **Reunir o dataset.** O autor tem imagens dos **caps 1–5 do Livro 1** (na
   máquina dele) + 6 imagens de referência no projeto-mãe
   (`referencia_visual/imagens/`: pranchas de MP, AGU, CNMP, grupo 6). Organizar em:
   - `/dataset/100_estilo/` — imagens que representam o traço da coleção.
   - `/dataset/200_<personagem>/` — 10–20 imagens variadas de 1–2 personagens Tier 1
     (sugestão: **João** e **Leônidas/STF**, os mais centrais).
2. **Legendar (captions).** Para cada imagem, um `.txt` de mesmo nome com a
   descrição + **trigger word única** (ex.: `estilo_colecao_xyz`,
   `joao_cidadao_xyz`). Descrever o que NÃO é identidade (roupa, fundo) para o
   modelo não grudar isso no personagem.
3. **Treinar o LoRA de estilo** via API (Fal.ai/Replicate). Custo ~US$ 2–5.
4. **Gerar testes** de cenas dos caps 1–5 e comparar com as imagens originais:
   o traço bate? O personagem se mantém? Ajustar captions/peso e re-treinar se
   preciso.
5. **Decisão de porteira:** só avançar para a Fase 2 quando a consistência estiver
   aprovada pelo autor.

> Nesta fase **não há servidor ligado** — você (agente) dispara o treino/geração
> via API e salva os resultados no repo. Custo de hospedagem = zero.

## FASE 2 — Interface (o "ChatGPT ilustrador")

1. **Backend** (Python) que recebe o texto, chama o "diretor de arte" (LLM) para
   montar o prompt, injeta as trigger words e chama a API de imagem.
2. **Interface de chat** (Gradio/Streamlit para começar — simples; ou frontend
   Vercel depois). Barra lateral para escolher personagem em cena e peso do estilo.
3. **Hospedagem:** reaproveitar a conta **Railway** do autor (ver `INFRAESTRUTURA.md`).
   Padrão Dockerfile/FastAPI do projeto Gus transplanta direto.
4. **Storage:** imagens e modelos no **Cloudflare R2**.

## FASE 3 — Consistência avançada e produção em lote

1. **LoRAs dos demais Tier 1** (lista em `UNIVERSO.md` §6), conforme o autor precisar.
2. **Texto fiel na imagem** (placas, "Livro Dourado", brasões): modelo base com
   encoder T5 (FLUX/SD3) e, em casos difíceis, **ControlNet de tipografia**.
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

## Custos esperados (confirmar valores atuais)

| Item | Quando | Estimativa |
|---|---|---|
| Treino de LoRA | por treino | ~US$ 2–5 |
| Geração de imagem | por imagem | ~US$ 0,03 (FLUX) |
| Storage R2 | mensal | centavos até GBs |
| Railway | Fase 2+ | reaproveita conta existente |
| LLM diretor de arte | por uso | chave já existente |
| **Pontapé inicial** | único | **~US$ 10 de crédito** |

---

## Riscos / decisões em aberto (para você endereçar)

- **Onde os modelos/datasets moram** (R2 vs Git LFS vs outro) — decidir cedo.
- **Modelo base definitivo** (consistência vs texto-na-imagem vs custo) — verificar
  o estado da arte atual.
- **Quantos LoRAs de personagem** valem a pena vs prompt+estilo — começar pelos
  Tier 1 e medir.
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
