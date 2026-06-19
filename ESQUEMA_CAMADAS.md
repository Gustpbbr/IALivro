# ESQUEMA_CAMADAS — Contrato Etapa B → Etapa C

> Passo 9 do `ETAPA_B_PASSO_A_PASSO.md`. Este documento congela o formato do `camadas.json` como **contrato** entre o pipeline de descompilação e o editor.
>
> A partir daqui, qualquer mudança neste esquema deve ser explicitamente versionada (`schema_version`) e acordada entre as duas etapas. Se o pipeline mudar a saída, o editor precisa saber.

**Versão:** `1`
**Última atualização:** 2026-06-13

---

## Estrutura raiz

```json
{
  "schema_version": 1,
  "imagem_origem": "exemplo_constituicao.png",
  "dimensoes": { "largura": 1024, "altura": 1536 },
  "fundo_limpo": "fundo_limpo.png",
  "camadas": [ ... ],
  "_meta": { ... }
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `schema_version` | int | sim | Versão deste esquema. Editor recusa abrir versões desconhecidas. |
| `imagem_origem` | string | sim | Nome do arquivo da imagem original (raster do ChatGPT). |
| `dimensoes` | obj | sim | `{ largura, altura }` em pixels. |
| `fundo_limpo` | string | sim | Caminho relativo do PNG da cena sem UI (saída do Passo 7). |
| `camadas` | array | sim | Lista de camadas, ordenadas por hierarquia visual (título → fundo). |
| `_meta` | obj | não | Metadados de processamento (modelo, tokens, reconciliação). |

---

## Tipos de camada

Toda camada tem campos comuns:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | string | sim | Identificador único em `snake_case`. |
| `tipo` | enum | sim | `texto` \| `caixa` \| `icone` \| `cena` \| `linha_divisoria` |
| `bbox` | obj | sim | `{ x, y, w, h }` em pixels absolutos. |
| `z` | int | não | Ordem de empilhamento (maior = mais ao topo). Default = índice no array. |
| `mascara` | string | não | Caminho do PNG binário da máscara individual (pra P3 modos 🟡/🔵). |

### Tipo `texto`

```json
{
  "id": "titulo_principal",
  "tipo": "texto",
  "conteudo": "JUSTIÇA, PROTEÇÃO E DIGNIDADE",
  "bbox": { "x": 130, "y": 50, "w": 764, "h": 64 },
  "estilo": {
    "cor": "#1a1a1a",
    "cor_fundo_local": "#f0e8d6",
    "tamanho_px": 56,
    "fonte_classe": "serif",
    "peso": "bold",
    "alinhamento": "center"
  }
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `conteudo` | string | sim | Texto literal. Multi-linha usa `\n`. |
| `estilo.cor` | hex | sim | Cor do texto (amostrada pelo Passo 5). |
| `estilo.cor_fundo_local` | hex | não | Cor do pixel ao redor do texto (útil pra entender contexto). |
| `estilo.tamanho_px` | int | sim | Altura aproximada da glifa em pixels. |
| `estilo.fonte_classe` | enum | sim | `serif` \| `sans_serif` \| `display`. Editor mapeia pra fonte real. |
| `estilo.peso` | enum | não | `normal` \| `bold` \| `light`. Default `normal`. |
| `estilo.alinhamento` | enum | não | `left` \| `center` \| `right`. Default `left`. |

**Editável:** conteúdo, cor, tamanho, fonte (do catálogo do editor), peso, alinhamento, posição.

### Tipo `caixa`

```json
{
  "id": "box_polmilitar",
  "tipo": "caixa",
  "bbox": { "x": 18, "y": 168, "w": 200, "h": 158 },
  "cor_fundo": "#5a2a1a",
  "cor_borda": "#c9a961",
  "espessura_borda": 2,
  "raio_canto": 6,
  "filhos": ["titulo_box_polmilitar", "corpo_box_polmilitar"],
  "mascara": "mascaras/box_polmilitar.png"
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `cor_fundo` | hex | sim | Cor de preenchimento. `null` se transparente. |
| `cor_borda` | hex | não | Cor da borda. `null` se sem borda. |
| `espessura_borda` | int | não | Em pixels. Default 0 (sem borda). |
| `raio_canto` | int | não | Border-radius em pixels. Default 0. |
| `filhos` | array | não | IDs de camadas filhas (textos, ícones contidos). Editor agrupa visualmente. |

**Editável:** cor fundo, cor borda, espessura, raio, posição, tamanho. Apagar oferece 🟢/🟡/🔵.

### Tipo `icone`

```json
{
  "id": "icone_brasao_pm",
  "tipo": "icone",
  "bbox": { "x": 40, "y": 28, "w": 108, "h": 130 },
  "arquivo_recorte": "icones/icone_brasao_pm.png",
  "descricao": "Escudo dourado com tons azuis, brasão da Polícia Militar"
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `arquivo_recorte` | string | sim quando SAM rodou | Caminho do PNG transparente recortado. |
| `descricao` | string | não | O que Claude vision descreveu (útil pra busca e re-substituição). |

**Editável:** posição, tamanho, rotação, substituir por outro PNG.

### Tipo `cena`

```json
{
  "id": "cena_central",
  "tipo": "cena",
  "bbox": { "x": 0, "y": 150, "w": 1024, "h": 700 },
  "descricao": "Doberman PM, coruja Defensoria, família, escadaria..."
}
```

**Editável:** apenas posição/escala. A cena em si é responsabilidade do ChatGPT (re-gerar) ou do Passo 7 (inpainting).

### Tipo `linha_divisoria`

```json
{
  "id": "linha_horizontal_01",
  "tipo": "linha_divisoria",
  "bbox": { "x": 100, "y": 900, "w": 824, "h": 2 },
  "cor": "#c9a961",
  "espessura": 2,
  "estilo": "solida"
}
```

**Editável:** cor, espessura, estilo (`solida` | `tracejada`). Apagar só 🟢.

---

## Modos de "apagar" por tipo (P3)

| Tipo | 🟢 simples | 🟡 refazer fundo | 🔵 estender cena |
|---|:---:|:---:|:---:|
| `texto` | ✅ | ✅ | — |
| `caixa` | ✅ | ✅ | ✅ |
| `icone` | ✅ | ✅ | — |
| `cena` | — | — | — |
| `linha_divisoria` | ✅ | — | — |

🟢 grátis (revela `fundo_limpo.png`). 🟡 ~US$ 0,02 (inpainting + prompt opcional). 🔵 ~US$ 0,04 (outpainting).

---

## Campos meta (informativos, editor pode ignorar)

```json
"_meta": {
  "claude": {
    "modelo": "claude-sonnet-4-6",
    "tokens_input": 1500,
    "tokens_output": 4200
  },
  "reconciliacao": {
    "iou_min": 0.3,
    "ocr_total": 25,
    "ocr_casados": 18,
    "ocr_orfaos": 7,
    "claude_suspeitos": 2
  }
}
```

Camadas individuais podem carregar `_ocr_confianca`, `_suspeita`, `_origem` durante debug — o Passo 8 deve **remover** antes da exportação final. Esses campos não entram no contrato.

---

## Compatibilidade pra Sentido 2 (composição direta)

Quando o editor permitir criar camadas do zero (Etapa C futura), a estrutura é a mesma — apenas sem campos opcionais que dependem de descompilação:

- Sem `_ocr_confianca`
- `mascara` opcional (não tem máscara pra elemento criado do nada)
- `estilo.cor_fundo_local` opcional

O esquema é **válido para os dois caminhos** desde a v1.

---

## Validação

Sugestão: editor valida com JSON Schema antes de abrir. Esqueleto inicial em `poc_descompilacao/etapas/exportar.py` futuro, ou doc separado.

Versionamento: ao mudar este esquema, incrementar `schema_version`. Editor recusa abrir versão maior que conhece (forward-incompatible por default).
