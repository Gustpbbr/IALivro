# CHECKLIST — Revisão das 61 pranchas individuais

> **Para a sessão do repositório-mãe (Livro):** instruções do que analisar e
> alterar ao reescrever as fichas/pranchas dos 61 personagens. Decidido pelo
> autor + agente do repo IALivro em 12/06/2026. Exemplo concreto do formato
> atualizado: `MODELO_FICHA_ATUALIZADA_SOFIA.md` (no repo IALivro).

## A. Acrescentar em TODAS as fichas

0. **Formato em DUAS pranchas por personagem** (decidido 12/06/2026, após o
   piloto do Dimas — a prancha única fica lotada e os painéis pequenos geram
   recortes de baixa resolução para o dataset):
   - **PRANCHA A — Identidade institucional**: cabeçalho, identificação, 5
     vistas, paleta, símbolo, elementos de trabalho, texturas, detalhes,
     missão/atributos/valores, aplicações (o formato atual).
   - **PRANCHA B — Performance**: EXPRESSÕES (4 close-ups grandes de rosto) +
     POSES DE AÇÃO (2, corpo inteiro) + TRAJE ALTERNATIVO (se figurino
     variável) — painéis GRANDES, fundo neutro, mesma direção de renderização.
1. **SEÇÃO 0 — DIREÇÃO DE RENDERIZAÇÃO**: bloco padrão **idêntico palavra por
   palavra** em todas (copiar do modelo da Sofia), mudando apenas a 1ª linha
   (espécie) **+ no máximo 1 linha extra específica da espécie** (ex.: "sem
   nenhum traço de primata ou humano no rosto: crânio, focinho e olhos 100%
   caninos" — validado no piloto do Dimas). O núcleo permanece idêntico nas 61.
   - Conteúdo-chave: hiper-realista; 90% animal / 10% antropomorfização; sem
     cartoon/mascote/animação infantil; pelagem/plumagem fio a fio; wildlife
     photography + creature design AAA; materialidade física real; iluminação
     editorial premium; **fundo neutro nas vistas e close-ups**.
   - **Referência por ANEXO, não por nome**: o autor sempre anexa 1–2 pranchas
     aprovadas como guia ao gerar. Renomear esses arquivos para
     `PRANCHA_MODELO_01.png`, `PRANCHA_MODELO_02.png`… e o bloco de prompt
     referencia "as pranchas-modelo anexadas" (nunca "igual ao Leônidas" — o
     gerador não conhece os personagens por nome, só vê os anexos).
   - **Exceção — Quarteto pop-up** (Veríssimo, Lúcia, Lúmen, Nexus): bloco
     CARTOON próprio (declarar explicitamente: estilo cartoon 2D vivo, cores
     chapadas vibrantes, contorno definido, quebra da quarta parede), também
     idêntico entre os 4.
2. **Altura canônica (metadado)**: campo `Altura: X,XX m` na IDENTIFICAÇÃO.
   Régua: **João = 1,80 m**. Grandes ≈ 1,95–2,20 m (gorila, rinoceronte, leão);
   médios ≈ 1,60–1,90 m; pequenos ≈ 1,20–1,60 m (sagui, anfíbios, esquilo).
   ⚠️ **NUNCA** escrever "menor em escala" ou desenhar régua/João na prancha solo
   (degrada o detalhe na geração). A escala relativa só será usada pelo diretor
   de arte em cenas com 2+ personagens. **Criar tabela única de alturas dos 61**
   no documento canônico.
3. **Figurino: FIXO ou VARIÁVEL** (campo na IDENTIFICAÇÃO). Se variável entre
   livros, incluir 1 vista com traje alternativo.
4. **SEÇÃO EXPRESSÕES** — 4 close-ups de rosto: neutra/padrão, positiva,
   preocupada/empática, firme/severa (adaptar nomes à personalidade).
   → **Renderizar na PRANCHA B**, em painéis grandes.
5. **SEÇÃO POSES DE AÇÃO** — 2 poses de corpo inteiro além do turnaround
   (uma da função típica + uma de movimento), fundo neutro.
   → **Renderizar na PRANCHA B**, em painéis grandes.

## A.1 QA pós-geração (conferir a imagem contra a ficha, antes de aprovar)

Divergências reais encontradas no piloto do Dimas — checar em toda geração:
- [ ] **Cabeçalho sem Tier** (o gerador herdou "Tier 2" da prancha-modelo antiga;
      todos são T1 e o campo foi removido das fichas)
- [ ] Painéis de EXPRESSÕES e POSES presentes (na Prancha B)
- [ ] Nº de texturas/detalhes igual ao da ficha
- [ ] Objetos restritos ao lugar certo (ex.: viatura só nas aplicações, nunca
      nas vistas)
- [ ] Nome, grupo e metadados idênticos aos da ficha (LISTA_FINAL)

## B. Padronizar em TODAS as fichas

6. **5 vistas fixas**: 3/4 (principal), frente, perfil esq., perfil dir., costas
   — corpo inteiro, fundo neutro, mesma iluminação (hoje há pranchas com 3).
7. **Nomes, grupo e tier conforme a LISTA_FINAL** (fonte canônica). Divergências
   já detectadas nas pranchas antigas: "Leônidas Supremo"→Leônidas
   Constitucional; "Sofia Alba/Defensora"→Sofia Acesso; "Gregório
   Congresso"→Tito Bicameral; "Álvaro Custos"→Álvaro Parquet;
   "Baltasar/Boris/Nestor" (Executivo)→nomes da LISTA_FINAL; Domingos =
   **caracal** (não felino pintado).
8. **Paleta**: nome descritivo + hex (como na ficha da Sofia) — o hex orienta o
   QA; o nome descritivo orienta a geração.
9. **Formato**: vertical 2:3, 2400×3600px, mesmo template de diagramação.
10. **Tier 1 para todos** (decisão do autor, 12/06/2026) — treino de LoRA
    acontecerá em ondas, por ordem de aparição nos livros.

## C. Conflitos canônicos a resolver durante a revisão

11. **Livro 9**: teal #2A8B8B ("Administração Geral") vs azul #3891D6 ("Direito
    Administrativo Geral") — fixar um.
12. **DF / Capital Federativa**: confirmar espécie única roxa/rosa (prancha
    individual ✅) e aposentar infográficos com DF como canindé/arara vermelha.
13. **Prancha dos URSOS** (entes federativos antigos): arquivar como histórico —
    casting abandonado, nunca usar como referência.
14. **João**: confirmar que o canônico é o REALISTA da prancha individual (com
    progressão narrativa); a versão cartoon de prancha de grupo é descartada.
15. **Téo Transitório**: girino não-antropomorfizado — confirmar se é
    intencional (coerente com a fase larval) ou se ganha versão antropomórfica.

## D. Lembrete de fluxo

- Pranchas novas geradas → subir na pasta do Drive ("Imagens Livro /
  Pranchas_individuais") → o repo IALivro importa via GitHub Actions e refaz a
  triagem/fatiamento automaticamente.
- Ao final da revisão, enviar a LISTA_FINAL atualizada (nomes/grupos/alturas)
  para o repo IALivro sincronizar o UNIVERSO.md e definir as trigger words.
