# POC — Descompilação de imagens em camadas

Implementação da **Etapa B** do projeto IALivro. Veja a especificação em [`../ETAPA_B_POC_DESCOMPILACAO.md`](../ETAPA_B_POC_DESCOMPILACAO.md) e o passo a passo em [`../ETAPA_B_PASSO_A_PASSO.md`](../ETAPA_B_PASSO_A_PASSO.md).

## Setup

```bash
cd poc_descompilacao
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com suas chaves
```

## Uso

```bash
python descompila.py tests/imagens/exemplo_constituicao.png
```

Imagens versionadas pra teste vão em `tests/imagens/` (no Git). Imagens efêmeras podem ir direto em `tests/` (gitignored).

A saída vai pra `output/`. Cada execução **sobrescreve** a anterior.

## Status dos passos

- [x] Passo 0 — Setup
- [x] Passo 1 — Carregar imagem
- [x] Passo 2 — Análise semântica (Claude)
- [x] Passo 3 — OCR
- [x] Passo 4 — Reconciliação
- [x] Passo 5 — Estilo de texto
- [x] Passo 6 — SAM 2 (implementado, precisa FAL_KEY pra rodar)
- [x] Passo 7 — Inpainting + máscaras individuais (implementado, precisa FAL_KEY)
- [x] Passo 8 — Exportação final
- [ ] Passo 9 — Esquema do JSON congelado
- [ ] Passo 10 — Validação com mais imagens
- [ ] Passo 11 — Decisão de porteira

## Estrutura

```
poc_descompilacao/
├── descompila.py          # CLI principal
├── etapas/                # módulos de cada passo
│   └── __init__.py
├── prompts/               # prompts pra Claude
├── tests/
│   └── imagens/           # imagens versionadas pra teste
├── output/                # resultados (gitignored)
├── requirements.txt
├── .env.example
└── README.md
```
