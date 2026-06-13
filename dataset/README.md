# dataset/ — imagens de treino dos LoRAs

Estrutura no padrão dos treinadores de LoRA (`<repetições>_<conceito>`):

```
dataset/
├── 100_estilo/           traço da coleção (estilo geral, sem foco em 1 personagem)
├── 200_joao/             João, o protagonista humano (10–20 imagens variadas)
└── 201_leonidas_stf/     Leônidas Constitucional, o Leão do STF (10–20 imagens variadas)
```

## O que o autor precisa subir (Fase 1)

**Tudo, sem curadoria** — pranchas de personagens, cenas dos caps 1–5 e infográficos,
numa pasta do Google Drive. A triagem é trabalho do agente:

| Material | Destino no dataset |
|---|---|
| **Pranchas de personagem** (vistas + detalhes + paletas) | Fatiadas via script (Pillow): vistas frente/3-4/perfil e close-ups viram imagens de treino do personagem; caixas de texto ficam de fora. Os textos das pranchas alimentam as captions |
| **Cenas completas** (João no horizonte, árvore da Constituição…) | `100_estilo/` — ensinam luz, cerrado, concreto, atmosfera |
| **Personagens nítidos dentro de cenas** | Recortados para o dataset do personagem — só se o recorte tiver resolução decente; figurantes minúsculos/de costas ficam de fora (viram ruído) |
| **Infográficos com muito texto/setas** | Fora do treino (ou só regiões limpas recortadas) — texto embutido ensina o modelo a gerar "letras fantasmas" |
| **Paletas hexadecimais** | Não vão pro treino: o diretor de arte as traduz em descrições de cor no prompt, e o QA as usa para conferir as cores das imagens geradas |

O que faltar de variedade por personagem (ângulos, expressões) será **fabricado**
com modelo de edição por referência (Qwen-Image-Edit / Nano Banana) a partir das
vistas das pranchas — meta de 25–30 imagens por personagem treinado.

## Captions (legendas)

Cada imagem terá um `.txt` de mesmo nome ao lado dela (ex.: `cena01.png` +
`cena01.txt`) com a descrição da cena + a **trigger word** do conceito.
As captions serão geradas/revisadas pelo agente — o autor só precisa subir
as imagens.

## Regras

- Formatos: PNG ou JPG, na maior resolução disponível.
- Não subir imagens borradas, cortadas ou fora do estilo final aprovado.
- Quando o dataset crescer, ele migra para o Cloudflare R2 (decisão do PLANO.md).
