# CLAUDE.md — Orquestrador de Narrativa Visual (IA de imagem da coleção)

> **Para o agente (Claude Code / Fable 5):** este é o repositório de uma **IA de
> imagem especializada** no universo de uma coleção didática de 11 livros de
> Direito. O objetivo, o universo e a infraestrutura estão nos três documentos
> companheiros — **leia os três antes de propor qualquer coisa**:
> 1. `UNIVERSO.md` — o que precisa ser desenhado (61 personagens, estilo, regras visuais).
> 2. `PLANO.md` — o passo a passo do projeto (fases 1→4).
> 3. `INFRAESTRUTURA.md` — o que o autor JÁ tem e pode reaproveitar (não recriar do zero).

---

## ⚠️ PROTOCOLO DE INÍCIO (faça isto PRIMEIRO, antes de escrever código)

1. **Leia** `UNIVERSO.md`, `PLANO.md` e `INFRAESTRUTURA.md`.
2. **Busque suas próprias capacidades atuais** (ferramentas, MCPs, limites do
   ambiente) e diga, com honestidade, **o que você consegue e o que não consegue**
   fazer deste plano neste ambiente. Não prometa o que não pode executar.
3. **Avalie criticamente o plano** com olhos de 2026: o que está atualizado, o que
   mudou (modelos base, serviços de treino/inferência, preços), o que dá para
   simplificar ou melhorar. Proponha ajustes **antes** de executar.
4. **Confirme o ponto de partida** com o autor (a Fase 1 enxuta do `PLANO.md`) e só
   então comece. Não pule para construir a interface completa sem validar o estilo.

---

## QUEM FAZ O QUÊ (papéis)

| Autor (Diretor Criativo) | Você (Engenheiro) |
|---|---|
| Define o que é "bom" — estética, fidelidade à narrativa, aprovação final | Escreve TODO o código (pipeline, backend, interface, scripts) |
| Fornece as imagens base e as chaves de API | Configura serviços, chama APIs de treino/geração |
| Aprova/reprova as imagens geradas | Estrutura o repositório, automatiza o fluxo, corrige bugs |
| Decide rumos e prioridades | Explica cada passo em linguagem simples e pede confirmação |

> **O autor não é programador.** Explique decisões técnicas em português claro,
> sem jargão desnecessário. Quando precisar que ele faça algo fora do código
> (criar conta, colar uma chave, subir imagens), dê o passo a passo.

---

## REGRAS DE OURO

1. **Consistência visual acima de tudo.** O propósito do projeto é que os 61
   personagens e o estilo se mantenham idênticos do Livro 1 ao Livro 11. Toda
   decisão técnica serve a isso.
2. **A fonte canônica do universo prevalece.** `UNIVERSO.md` resume; em dúvida de
   personagem/estilo, vale a fonte no projeto-mãe (`00_FUNDACAO_E_GUIAS/`).
3. **Reaproveite antes de criar.** Veja `INFRAESTRUTURA.md` — o autor já tem
   conta Railway, chaves Anthropic/OpenAI, conta Cloudflare. Crie só o
   estritamente necessário (a conta de geração de imagem).
4. **Comece enxuto.** Fase 1 = validar o LoRA de estilo + 1–2 personagens gastando
   centavos, ANTES de construir a interface (a "catedral"). Não inverta.
5. **Segurança de credenciais.** Nunca hardcode chaves no código. Use variáveis de
   ambiente / secrets. Nunca commite `.env`.
6. **Custo sob controle.** Antes de rodar treinos/gerações em lote, estime e avise
   o custo. Geração paga por uso — nada de loops caros sem aprovação.
7. **Aprovação humana para ações com efeito no mundo.** Treinar, gastar créditos,
   apagar arquivos, publicar — confirmar com o autor antes.

---

## ESTADO ESPERADO DO REPOSITÓRIO (a montar — ver PLANO.md)

```
/dataset/         imagens base, organizadas por estilo e por personagem
/captions/        legendas (.txt) com trigger words
/training/        scripts e configs de treino do LoRA (via API de nuvem)
/models/          LoRAs treinados (.safetensors) — provavelmente em storage externo
/app/             backend + interface de chat (Fase 2)
/feedback/        positivos/negativos para re-treino
/outputs/         imagens geradas, nomeadas por capítulo
```

> Esta estrutura é uma sugestão do plano — **avalie e proponha o que for melhor**
> antes de criar.

---

## NÃO FAÇA
- Não trate as alegações de marketing sobre modelos como fato — **verifique** preços,
  nomes de serviços e capacidades antes de afirmar.
- Não inche o repositório com modelos pesados (.safetensors, datasets enormes) sem
  decidir com o autor onde eles moram (storage externo é melhor que Git).
- Não construa a interface completa antes de o estilo estar validado.
