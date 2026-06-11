# IALivro — Orquestrador de Narrativa Visual

IA de imagem especializada na coleção didática de 11 livros de Direito:
ilustra os capítulos mantendo **consistência rigorosa** de personagens
(61 personagens-animais), cenários e estilo.

> Este repositório nasceu do kit de partida preparado no repo-mãe dos livros.
> A fonte canônica do universo continua lá (`00_FUNDACAO_E_GUIAS/`); em
> divergência, ela prevalece sobre os resumos daqui.

## Documentos principais

| Arquivo | Para quê |
|---|---|
| `CLAUDE.md` | Regras do projeto + protocolo de início para o agente |
| `UNIVERSO.md` | Briefing do universo (61 personagens, estilo, regras visuais) |
| `PLANO.md` | Passo a passo (Fase 1 enxuta → Fase 4) |
| `INFRAESTRUTURA.md` | O que já existe e pode ser reaproveitado |

## Estrutura

```
referencia_visual/   DNA visual: guias (cores, personagens, cenários) + imagens de referência
dataset/             imagens de treino (ver dataset/README.md) — captions .txt ao lado de cada imagem
training/            scripts e configs de treino dos LoRAs (via API de nuvem)
outputs/             imagens geradas, nomeadas por capítulo
docs/                material de pesquisa e apoio
```

## Estado atual

**Fase 1 — Validação enxuta** (ver `PLANO.md`): reunir o dataset dos caps 1–5
do Livro 1, legendar, treinar o LoRA de estilo e validar a consistência antes
de construir qualquer interface.
