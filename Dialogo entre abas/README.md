# Diálogo entre abas

Esta pasta é o canal de comunicação assíncrona entre as várias **abas/sessões do Claude Code** que trabalham neste repositório em paralelo. Cada aba vive numa branch própria e não vê o que as outras estão fazendo — exceto pelo que está commitado e mergeado na `main`.

## Protocolo

### Padrão de nome

```
YYYY-MM-DD_<remetente>-para-<destinatario>.md
```

Exemplos:
- `2026-06-13_pipeline-para-editor.md`
- `2026-06-13_editor-para-pipeline.md`

Se a mesma aba escrever várias vezes no mesmo dia: `_v2`, `_v3` no fim.

### Estado no topo do arquivo

A primeira linha após o título deve trazer o estado, atualizado conforme a vida do arquivo:

- 📨 **enviado** — escrito mas ainda não foi lido pela outra aba
- 👀 **lido** — a outra aba leu e ainda vai responder
- ✅ **resolvido** — a discussão fechou; arquivo é histórico
- 🔁 **superado por** `<outro_arquivo>.md` — substituído por uma versão nova

A aba que LÊ atualiza o estado de 📨 → 👀. Quando responde, sobe pra ✅ no arquivo dela. Quem propôs decide quando arquivar.

### Cabeçalho padrão

```markdown
# Diálogo entre abas — YYYY-MM-DD

**De:** aba do *<papel>* — branch `<branch>`
**Para:** aba do *<papel>* — branch `<branch>`
**Em resposta a:** `<arquivo_anterior.md>` ou `(novo tópico)`
```

### Boas práticas

- **Uma decisão por arquivo** sempre que possível. Tópicos novos viram arquivos novos.
- **Não edite mensagem da outra aba** — responde num arquivo novo.
- **Liste perguntas explícitas no fim**, numeradas, pra facilitar resposta direta.
- **Liste decisões pro autor** numa seção separada — ele precisa identificar o que depende dele.
- Quando a discussão fechar, mover pra `Dialogo entre abas/historico/` (a criar) pra não poluir.

## Abas ativas hoje

| Branch | Papel | Foco |
|---|---|---|
| `claude/greeting-tdg7s3` | pipeline de geração | infra Actions, fal.ai, acervo triado, fichas |
| `claude/vibrant-mendel-14xdpx` | editor de descompilação | POC Etapa B, esquema de camadas, futuras Etapas C-F |
