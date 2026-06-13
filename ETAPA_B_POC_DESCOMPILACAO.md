# ETAPA B — POC do Pipeline de Descompilação

> Primeiro passo concreto do `PLANO.md` v2. Objetivo: provar que dá pra "explodir" uma imagem raster do ChatGPT em camadas editáveis, **sem interface ainda**. Só backend + linha de comando.

---

## Objetivo

Receber **1 imagem PNG** gerada pelo ChatGPT e devolver:

1. Um **JSON de camadas** descrevendo cada elemento identificado
2. Um **PNG do fundo limpo** (cena sem texto e sem boxes)
3. **PNGs recortados** de cada ícone/elemento gráfico isolado

Tudo em disco. Sem UI. Roda via `python descompila.py imagem.png`.

---

## Entrada de teste

Imagem de exemplo: a infográfico do ChatGPT enviada em 13/06 ("Justiça, Proteção e Dignidade — A Constituição no Centro de Tudo"). Contém:

- Título grande no topo
- Subtítulo
- 2 brasões (PM e Defensoria)
- 2 boxes laterais de cabeçalho (Polícia Militar / Defensoria Pública)
- Cena central (doberman PM, coruja DP, família, escadaria de prédio público)
- 1 box "Como atuamos juntos" (com lista)
- 1 box "Valores"
- 1 box "Resultados que transformam vidas"
- Faixa central com texto da Constituição
- Box "A Constituição é a nossa direção" (com bússola e 4 itens)
- Faixa de rodapé

Ideal pra testar: tem texto de tamanhos variados, boxes com fundos diferentes, ícones, cena central complexa.

---

## Pipeline (passo a passo)

### 1. Análise semântica de layout (Claude vision)

Manda a imagem pro Claude com prompt do tipo:

> "Analise esta imagem e descreva, em JSON, todos os elementos visuais distintos: títulos, blocos de texto, caixas com fundo colorido, ícones, brasões, e a cena central. Para cada um, dê: tipo, conteúdo textual (se houver), bounding box aproximada (x, y, largura, altura em % da imagem), cor de fundo aproximada, cor do texto."

Saída: estrutura inicial do JSON de camadas.

### 2. Segmentação fina (SAM 2 via Fal.ai)

Pra cada bbox que o Claude apontou, roda SAM 2 com prompt de ponto/box pra ter máscara pixel-precisa do elemento. Útil pra:
- Recortar ícones com fundo transparente
- Saber onde exatamente está cada box (não só bbox retangular)
- Separar a cena central do fundo geral

### 3. OCR (PaddleOCR)

Roda em paralelo no resto da imagem pra pegar:
- Texto exato (Claude vision às vezes parafraseia)
- Bounding box pixel-precisa de cada linha de texto
- Confiança por linha

Reconcilia com a análise do Claude (mesmo texto, bbox mais precisa).

### 4. Estimativa de estilo do texto

Pra cada bloco de texto:
- **Cor:** amostra de cor mediana dos pixels do texto
- **Tamanho (px):** altura do bbox / número de linhas
- **Fonte aproximada:** classifica como serif / sans-serif / display via heurística simples (proporção, presença de serifas). **Font matching real fica pra Etapa C** — basta agora dizer "fonte aproximada: serif elegante" e deixar o usuário escolher.

### 5. Inpainting do fundo (Fal.ai)

Cria máscara unindo todos os textos e boxes detectados. Roda inpainting (LaMa ou SD inpaint) pra reconstruir o que estava embaixo. Resultado: PNG limpo só com a cena central + cenário.

### 6. Exportação

```
output/
├── camadas.json          # estrutura completa
├── fundo_limpo.png       # cena sem text/boxes
├── icones/
│   ├── brasao_pm.png
│   ├── brasao_defensoria.png
│   ├── icone_familia.png
│   └── ...
└── debug/
    ├── bboxes_visualizadas.png   # mesma imagem com retângulos por cima
    └── mascara_inpainting.png
```

---

## Formato do `camadas.json` (proposta)

```json
{
  "imagem_origem": "exemplo_constituicao.png",
  "dimensoes": { "largura": 1024, "altura": 1536 },
  "camadas": [
    {
      "id": "titulo_principal",
      "tipo": "texto",
      "conteudo": "JUSTIÇA, PROTEÇÃO E DIGNIDADE",
      "bbox": { "x": 80, "y": 32, "w": 880, "h": 72 },
      "estilo": {
        "fonte_classe": "serif_elegante",
        "tamanho_px": 56,
        "cor": "#1a1a1a",
        "peso": "bold",
        "alinhamento": "center"
      }
    },
    {
      "id": "box_polmilitar",
      "tipo": "caixa",
      "bbox": { "x": 40, "y": 140, "w": 220, "h": 180 },
      "cor_fundo": "#2d4a2b",
      "cor_borda": "#c9a961",
      "espessura_borda": 2,
      "raio_canto": 6,
      "filhos": ["titulo_polmilitar", "texto_polmilitar"],
      "mascara": "mascaras/box_polmilitar.png"
    },
    {
      "id": "icone_brasao_pm",
      "tipo": "icone",
      "arquivo": "icones/brasao_pm.png",
      "bbox": { "x": 70, "y": 30, "w": 100, "h": 100 }
    },
    {
      "id": "cena_central",
      "tipo": "cena",
      "bbox": { "x": 0, "y": 180, "w": 1024, "h": 900 },
      "descricao": "Doberman PM, coruja DP, família vista de costas, escadaria de prédio público"
    }
  ]
}
```

---

## Critério de "pronto"

A POC passa quando, rodando na imagem de exemplo:

- [ ] JSON identifica pelo menos 80% dos blocos de texto visíveis
- [ ] Bounding boxes não erram por mais de ~10 pixels
- [ ] Texto extraído pelo OCR está correto em pelo menos 90% dos casos
- [ ] Fundo limpo (inpainting) não tem buracos óbvios na cena central
- [ ] Brasões são extraídos como ícones separados
- [ ] Cores de fundo dos boxes são razoavelmente próximas do original

Não precisa estar perfeito — é POC. Erros de 1-2 boxes ou texto pequeno são aceitáveis.

---

## Custo estimado

| Item | Por execução |
|---|---|
| Claude vision (1 chamada) | ~US$ 0,02 |
| SAM 2 via Fal (várias máscaras) | ~US$ 0,05 |
| OCR (PaddleOCR local) | grátis |
| Inpainting (1 chamada Fal) | ~US$ 0,02 |
| **Total por imagem** | **~US$ 0,10** |

Durante desenvolvimento (50-100 iterações): ~US$ 5-10.

---

## Estrutura sugerida do código

```
poc_descompilacao/
├── descompila.py          # CLI principal
├── etapas/
│   ├── analise_layout.py  # chama Claude vision
│   ├── segmentacao.py     # chama SAM via Fal
│   ├── ocr.py             # PaddleOCR
│   ├── estilo_texto.py    # amostra cor, estima tamanho
│   ├── inpainting.py      # chama Fal inpaint
│   └── exportar.py        # gera JSON + arquivos
├── prompts/
│   └── claude_layout.txt  # prompt da etapa 1
├── tests/
│   └── exemplo_constituicao.png
└── requirements.txt
```

---

## O que NÃO entra nesta etapa

- Editor visual (Etapa C)
- Font matching real / DeepFont (Etapa C)
- Polish pass de re-renderização (Etapa D)
- Color grading (Etapa E)
- Qualquer interface web

---

## Decisões em aberto

1. **Onde rodar a POC?** Local na máquina do autor ou já num container Railway?
2. **Qual modelo Claude usar pro vision?** Opus 4.7/4.8 (mais caro, mais preciso) ou Sonnet 4.6 (mais barato)?
3. **PaddleOCR ou EasyOCR?** Testar os dois numa amostra e ver qual lê melhor textos pequenos.
4. **Imagem de teste única ou já 3-4 imagens diferentes?** Começar com 1 e expandir.
