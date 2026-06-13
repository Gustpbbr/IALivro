# ETAPA B — Passo a Passo de Execução

> Companheiro do `ETAPA_B_POC_DESCOMPILACAO.md`. Lá está **o quê** vamos construir. Aqui está **como** e **em que ordem**. Pra cada passo: o que fazer, como saber se funcionou, e qual a saída.

## Como ler este documento

Cada passo tem:
- **Objetivo** — o que está sendo provado
- **O que fazer** — ações concretas
- **Saída esperada** — arquivo ou comportamento observável
- **Critério de OK** — como decidir se passa pro próximo

Não pula passo. Cada um destrava o seguinte e isola falhas.

## Esclarecimento: Etapa B × Etapa C

| | Etapa B | Etapa C |
|---|---|---|
| **O quê** | Motor backend de descompilação | Editor visual (app de verdade) |
| **Interface** | Nenhuma. CLI/Python. | Web, mobile e desktop |
| **Define** | Vocabulário de camadas (o JSON) | Funções do app (ações do usuário) |
| **Pergunta que responde** | "Dá pra separar a imagem em partes editáveis?" | "Como o autor edita essas partes?" |

**O JSON de saída da Etapa B amarra a Etapa C.** Se a Etapa B só extrai "cor do box", você não consegue editar "gradiente do box" depois. Por isso o passo 9 abaixo é dedicado a fechar o esquema do JSON antes da Etapa C começar.

## Pré-decisões (resolver antes do Passo 1)

1. **Onde rodar?**
   - Recomendado: **local na máquina do autor** durante a POC. Mais barato, iteração rápida, sem latência de deploy.
   - Railway entra na Etapa C, quando virar serviço.

2. **Modelo Claude pro vision:**
   - Recomendado: **Sonnet 4.6** pra começar (mais barato, qualidade já alta pra layout).
   - Subir pra Opus 4.7/4.8 só se Sonnet falhar em casos complexos.

3. **OCR:**
   - Recomendado: começar com **PaddleOCR** (melhor em PT-BR e textos pequenos).
   - Manter EasyOCR como fallback se PaddleOCR der trabalho de instalar.

4. **Imagens de teste:**
   - Começar com **1 só** (a do ChatGPT da Constituição) até o pipeline rodar de ponta a ponta.
   - Depois validar com 3-4 imagens variadas.

## Passo 0 — Setup do ambiente

**Objetivo:** ter Python + dependências básicas rodando.

**O que fazer:**
- Criar pasta `poc_descompilacao/` no repo
- Criar `requirements.txt` com: `anthropic`, `paddleocr`, `pillow`, `requests`, `python-dotenv`, `numpy`
- Criar `.env.example` com placeholders: `ANTHROPIC_API_KEY`, `FAL_KEY`
- Criar `.env` real (gitignored) com as chaves
- Adicionar `.env` e `poc_descompilacao/output/` ao `.gitignore`

**Saída esperada:** `pip install -r requirements.txt` roda sem erro.

**Critério de OK:** Python importa `anthropic` e `paddleocr` sem reclamar.

## Passo 1 — Carregar imagem e visualizar

**Objetivo:** garantir que conseguimos abrir a imagem e ler dimensões corretas. Trivial, mas evita problemas chatos depois (orientação EXIF, perfil de cor, etc.).

**O que fazer:**
- Script `descompila.py` que recebe caminho da imagem
- Abre com PIL, imprime largura x altura, modo de cor (RGB/RGBA)
- Salva uma cópia em `output/debug/imagem_original.png` pra confirmar

**Saída esperada:**
```
$ python descompila.py tests/exemplo_constituicao.png
Imagem: 1024 x 1536, modo RGB
Salva em output/debug/imagem_original.png
```

**Critério de OK:** PNG salvo é idêntico ao original.

## Passo 2 — Análise semântica via Claude vision

**Objetivo:** Claude lê a imagem e descreve o layout em JSON estruturado. Este é o "cérebro" da descompilação.

**O que fazer:**
- Criar `prompts/claude_layout.txt` com instruções claras (ver prompt-base abaixo)
- Chamar Claude Sonnet 4.6 com `image` + prompt
- Pedir resposta em JSON estrito
- Salvar resposta em `output/debug/01_claude_layout.json`

**Prompt-base (rascunho):**
```
Analise esta imagem e identifique cada elemento visual distinto.
Retorne JSON com a chave "camadas", lista de objetos com:
- id: identificador descritivo em snake_case (ex: "titulo_principal")
- tipo: "texto" | "caixa" | "icone" | "cena" | "linha_divisoria"
- conteudo: texto literal se aplicável, null caso contrário
- bbox: {x, y, w, h} em PIXELS (não percentual)
- cor_fundo: hex aproximado, se caixa
- cor_texto: hex aproximado, se texto
- tamanho_aproximado: "pequeno" | "medio" | "grande" | "titulo"
- observacoes: anomalias visuais (filtro amarelo, ruído, etc.)

NÃO invente texto que não está visível. Se não conseguir ler, deixe conteudo: null.
Ordene por hierarquia visual (título primeiro, fundo por último).
```

**Saída esperada:** JSON com ~15-25 camadas pra imagem de teste.

**Critério de OK:** títulos e boxes principais identificados, sem alucinação textual. Aceita-se erro de bbox de até ~10% pra primeira passada.

## Passo 3 — OCR fino com PaddleOCR

**Objetivo:** pegar o texto exato e bbox precisa. O Claude às vezes parafraseia ou ignora texto pequeno; PaddleOCR pega tudo com precisão pixel.

**O que fazer:**
- Rodar PaddleOCR na imagem inteira (idioma: português)
- Salvar lista de `(texto, bbox, confiança)` em `output/debug/02_ocr.json`
- Gerar imagem de debug com bbox desenhada por cima (`output/debug/02_ocr_visual.png`)

**Saída esperada:** lista de ~20-40 blocos de texto com confiança >0.8 na maioria.

**Critério de OK:** abrir `02_ocr_visual.png` e ver que cada texto está dentro de um retângulo, sem grandes omissões.

## Passo 4 — Reconciliação Claude + OCR

**Objetivo:** mesclar as duas fontes. Claude dá a estrutura semântica ("isto é um título"), PaddleOCR dá o texto e bbox precisos.

**O que fazer:**
- Pra cada camada de tipo "texto" do Claude, achar bloco(s) PaddleOCR com IoU > 0.3
- Substituir o texto e bbox do Claude pelos do PaddleOCR
- Marcar camadas Claude sem match PaddleOCR como "suspeitas" (provável alucinação)
- Marcar blocos PaddleOCR sem match Claude como "texto_orfao" (criar nova camada)
- Salvar resultado em `output/debug/03_reconciliado.json`

**Saída esperada:** JSON com camadas consolidadas, sem duplicatas.

**Critério de OK:** nenhum texto importante da imagem está faltando, nenhum texto alucinado sobrou.

## Passo 5 — Estimativa de estilo do texto

**Objetivo:** pra cada bloco de texto, estimar cor real, tamanho em pixels, e classe de fonte (serif/sans/display).

**O que fazer:**
- Pra cada texto:
  - **Cor:** amostrar pixels dentro do bbox, filtrar fundo, calcular mediana RGB
  - **Tamanho:** altura do bbox / linhas detectadas
  - **Classe de fonte:** heurística simples por proporção (largura/altura), se serifa for detectável via templating ou só pedir pro Claude classificar
- Anexar ao JSON em `output/debug/04_com_estilo.json`

**Saída esperada:** cada camada texto tem `estilo.cor`, `estilo.tamanho_px`, `estilo.fonte_classe`.

**Critério de OK:** cor do título principal bate visualmente (±10 em RGB). Tamanhos relativos coerentes (título > subtítulo > corpo).

## Passo 6 — Segmentação fina com SAM 2 (Fal.ai)

**Objetivo:** pra ícones, brasões e a cena central, ter máscara precisa em vez de só bbox retangular. Permite recortar com transparência.

**O que fazer:**
- Pra cada camada tipo "icone" ou "cena":
  - Chamar SAM 2 via Fal.ai passando o ponto central do bbox como prompt
  - Salvar máscara em `output/debug/sam_<id>.png`
  - Recortar PNG transparente em `output/icones/<id>.png`

**Saída esperada:** PNGs transparentes dos brasões PM, Defensoria, e qualquer ícone principal.

**Critério de OK:** abrir os PNGs e ver o ícone com fundo limpo, sem pedaço cortado.

## Passo 7 — Inpainting do fundo

**Objetivo:** gerar a versão "fundo limpo" — a cena central sem textos e sem boxes por cima.

**O que fazer:**
- Criar máscara unindo todos os bbox de texto + boxes
- Chamar Fal.ai inpainting (LaMa) com a imagem + máscara
- Salvar resultado em `output/fundo_limpo.png`

**Saída esperada:** PNG mostrando só cena + cenário, sem texto ou boxes visíveis.

**Critério de OK:** comparação visual — buracos não óbvios. Aceita-se algumas imperfeições; perfeição vem na Etapa D (polish).

## Passo 8 — Exportação final

**Objetivo:** produzir o pacote completo que serve de entrada pra Etapa C.

**O que fazer:**
- Consolidar JSON final em `output/camadas.json` (formato da seção "Formato do `camadas.json`" do doc de especificação)
- Garantir que todos os caminhos de arquivo no JSON são relativos a `output/`
- Gerar `output/debug/visualizacao_final.png`: imagem original com retângulos por cima de cada camada

**Saída esperada:**
```
output/
├── camadas.json
├── fundo_limpo.png
├── icones/
│   ├── brasao_pm.png
│   ├── brasao_defensoria.png
│   └── ...
└── debug/
    ├── 01_claude_layout.json
    ├── 02_ocr.json
    ├── 03_reconciliado.json
    ├── 04_com_estilo.json
    ├── visualizacao_final.png
    └── mascara_inpainting.png
```

**Critério de OK:** olhando só pra `visualizacao_final.png`, dá pra entender o que foi identificado.

## Passo 9 — Fechar o esquema do JSON

**Objetivo:** congelar o formato de `camadas.json` como **contrato** entre a Etapa B e a Etapa C. Sem isso a Etapa C trabalha em areia movediça.

**O que fazer:**
- Revisar o JSON gerado e perguntar: "esse vocabulário é suficiente pra editar tudo que o autor precisa?"
- Documentar o esquema final em `ESQUEMA_CAMADAS.md` (com exemplos de cada tipo)
- Listar **propriedades editáveis** por tipo de camada (vai virar a base das funções da Etapa C)

**Exemplo de propriedades editáveis por tipo:**

| Tipo | Editável |
|---|---|
| `texto` | conteúdo, fonte, tamanho, cor, peso, alinhamento, posição |
| `caixa` | cor de fundo, cor de borda, espessura, raio do canto, posição, tamanho |
| `icone` | posição, tamanho, rotação, cor (se mono), substituir por outro |
| `cena` | só posição/escala — edição da cena em si é responsabilidade do ChatGPT (re-gerar) |
| `linha_divisoria` | cor, espessura, estilo (sólida/tracejada) |

**Saída esperada:** `ESQUEMA_CAMADAS.md` no repo, revisado pelo autor.

**Critério de OK:** autor assina embaixo. Esquema vira contrato.

## Passo 10 — Validação com imagens extras

**Objetivo:** confirmar que o pipeline funciona em mais de 1 caso. Achar onde ele quebra.

**O que fazer:**
- Pegar 3-4 imagens variadas (pranchas de personagem, infográfico denso, cena simples sem texto, página com muito texto)
- Rodar `descompila.py` em cada uma
- Anotar erros em `RESULTADOS_VALIDACAO.md`

**Saída esperada:** tabela com cada imagem, % de elementos identificados, principais erros.

**Critério de OK:** pelo menos 3 das 4 imagens passam nos critérios do Passo 8.

## Passo 11 — Decisão de porteira

**Objetivo:** decidir se a Etapa B está pronta o suficiente pra começar a Etapa C, ou se precisa de mais iteração.

**Perguntas pro autor:**
1. O esquema `camadas.json` cobre o que você quer editar?
2. A precisão (passos 1-7) é suficiente, ou preciso melhorar antes?
3. Os custos por imagem (~US$ 0,10) estão dentro do esperado?
4. Tem algum tipo de imagem (do livro real) que ainda não testamos e precisa testar?

**Saída esperada:** "go" ou "iterar". Se go, abrir documento da Etapa C.

## Resumo visual

```
[setup] → [carregar] → [Claude vision] → [OCR] → [reconciliar] → [estilo]
                                                                     ↓
                              [exportar] ← [inpainting] ← [SAM 2 ícones]
                                  ↓
                       [esquema JSON congelado]
                                  ↓
                       [validação com 3-4 imagens]
                                  ↓
                            [Etapa C ou iterar]
```

## O que NÃO entra nesta etapa (lembrete)

- Editor visual / UI
- Font matching real (DeepFont) — agora basta classificar serif/sans
- Polish pass de re-renderização
- Color grading
- Hospedagem em Railway
- Qualquer integração com ChatGPT
