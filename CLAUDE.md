# CLAUDE.md — IALivro

Briefing automático lido a cada sessão Claude Code no repositório `gustpbbr/ialivro`.

---

## O que é o projeto

**Orquestrador de Narrativa Visual + Editor de Descompilação.** Sistema pra produzir e editar imagens didáticas de uma coleção de 11 livros de Direito Brasileiro, mantendo consistência de 61 personagens-animais. A geração de imagens é feita no **ChatGPT** (alimentado pelas pranchas do autor). A edição/refinamento dessas imagens é feita por um **editor próprio** que descompõe o raster em camadas editáveis.

**Estado atual (jun/2026):** pós-pivot. O foco hoje é o editor (Etapas B-F), não a geração de imagens. Ver `PLANO.md` pra roadmap completo.

---

## Documentos canônicos (ler em ordem quando entrar em assunto novo)

1. **`PLANO.md`** — roadmap atual, princípios P1-P4, etapas A-F
2. **`UNIVERSO.md`** — 61 personagens, estilo, regras visuais (input do ChatGPT)
3. **`ESQUEMA_CAMADAS.md`** — contrato entre POC de descompilação e editor
4. **`ETAPA_B_POC_DESCOMPILACAO.md`** + **`ETAPA_B_PASSO_A_PASSO.md`** — POC do motor
5. **`ETAPA_C_ARQUITETURA.md`** — desenho do editor
6. **`Dialogo entre abas/README.md`** — protocolo de coordenação multi-aba
7. **`historico/`** — planos antigos (pré-pivot, pra referência)

Documentos auxiliares: `SISTEMA_CORES_COMPLETO_v2.md`, `GUIA_PADRONIZACAO_VISUAL_PERSONAGENS.md`, `GUIA_DIRECAO_ARTE_CENARIOS_CENAS.md`, `INFRAESTRUTURA.md`.

---

## Como trabalhar comigo (princípios)

1. **Explicite suposições.** Se a tarefa tem mais de uma leitura, declare e pergunte. Não interprete em silêncio.
2. **Mínimo viável.** Se 50 linhas resolvem, não escreva 200. Sem abstração especulativa, sem "flexibilidade" não pedida.
3. **Mudanças cirúrgicas.** Altere só o que a tarefa pede. Não refatore o adjacente, não toque em lógica que não domina.
4. **Execução por objetivo.** Defina critério de sucesso antes de codar. Itera até bater o critério.

---

## Sobre o autor

Gustavo, anestesiologista. **Não programa direto** — todo código é escrito por IA via conversa, ele revisa e aprova. Comunicação em **português brasileiro informal**. Crítica direta bem-vinda, jargão técnico desnecessário não. Quando algo dependa dele (criar conta, colar chave, subir arquivo), passe instruções passo-a-passo.

---

## Quem faz o quê

| Autor | Eu (Claude Code) |
|---|---|
| Define o que é "bom" — estética, fidelidade narrativa, aprovação final | Escreve TODO o código (pipeline, backend, editor, scripts) |
| Fornece pranchas e imagens base | Configura serviços, chama APIs |
| Aprova/reprova imagens e features | Estrutura repo, automatiza fluxo, corrige bugs |
| Decide rumos e prioridades | Explica decisões em português claro |

---

## Multi-aba (importante)

Mais de uma sessão Claude Code pode estar trabalhando no IALivro ao mesmo tempo, cada uma na própria branch. A coordenação é feita por arquivos `.md` em `Dialogo entre abas/` (ver `README.md` da pasta pra protocolo: padrão de nome, estados 📨/👀/✅).

**Abas ativas hoje:**
- `claude/greeting-tdg7s3` — pipeline de geração (infra Actions, fal.ai, acervo, fichas)
- `claude/vibrant-mendel-14xdpx` — editor de descompilação (POC, esquema, Etapas C-F)

**Quando você entrar:** identifique sua branch, veja se há novidades pra ti em `Dialogo entre abas/`.

---

## Regras de ouro (não-negociáveis)

1. **P1 — Camadas sempre:** texto/box vivem como camadas vetoriais no editor; nunca raster queimado. `camadas.json` é a fonte da verdade.
2. **P4 — IA pinta cena, app desenha UI:** texto e elementos didáticos são overlay vetorial; IA cuida só de cena, inpainting e polish.
3. **Custos sob controle.** Antes de rodar APIs pagas em lote, estime e avise. Nada de loops caros sem aprovação.
4. **Segredos.** Nunca hardcode chaves. Nunca commite `.env`. Use secrets do repo ou env vars.
5. **Aprovação humana pra efeitos no mundo.** Push pra main, gastos, publicação, exclusão — confirma antes.
6. **Modelo: Sonnet 4.6** pra vision/análise (custo-benefício). Opus 4.7/4.8 só quando Sonnet falhar.

---

## Branch de trabalho

Cada sessão tem uma branch designada (informada na inicialização). Faça commits descritivos lá, e proponha merge na `main` quando o autor pedir.

---

## Quando você não souber

Pergunte. Não invente. Não trate alegações de marketing como fato — verifique preços, modelos e capacidades antes de afirmar.
