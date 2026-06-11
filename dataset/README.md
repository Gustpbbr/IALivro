# dataset/ — imagens de treino dos LoRAs

Estrutura no padrão dos treinadores de LoRA (`<repetições>_<conceito>`):

```
dataset/
├── 100_estilo/           traço da coleção (estilo geral, sem foco em 1 personagem)
├── 200_joao/             João, o protagonista humano (10–20 imagens variadas)
└── 201_leonidas_stf/     Leônidas Constitucional, o Leão do STF (10–20 imagens variadas)
```

## O que o autor precisa subir (Fase 1)

Das imagens prontas dos **caps 1–5 do Livro 1**:

1. **`100_estilo/`** — todas as ilustrações que representam bem o traço da
   coleção (cenas, cenários, grupos). Quanto mais variadas, melhor.
2. **`200_joao/`** — 10–20 imagens do João em poses, ângulos, roupas e fundos
   diferentes. Variedade evita que o modelo "grude" roupa/fundo na identidade.
3. **`201_leonidas_stf/`** — idem para o Leônidas (Leão do STF).

A mesma imagem pode aparecer em mais de uma pasta se servir aos dois propósitos.

## Captions (legendas)

Cada imagem terá um `.txt` de mesmo nome ao lado dela (ex.: `cena01.png` +
`cena01.txt`) com a descrição da cena + a **trigger word** do conceito.
As captions serão geradas/revisadas pelo agente — o autor só precisa subir
as imagens.

## Regras

- Formatos: PNG ou JPG, na maior resolução disponível.
- Não subir imagens borradas, cortadas ou fora do estilo final aprovado.
- Quando o dataset crescer, ele migra para o Cloudflare R2 (decisão do PLANO.md).
