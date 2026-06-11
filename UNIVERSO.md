# UNIVERSO — A Coleção (briefing completo para a IA de imagem)

> **Para quem lê isto (Claude Code / Fable 5 no repositório novo):** este documento é
> autossuficiente. Ele descreve o universo ficcional que a IA de imagem precisa
> aprender a desenhar com **consistência absoluta**. Foi extraído da fonte canônica
> do projeto-mãe (a coleção de livros), em `00_FUNDACAO_E_GUIAS/FUNDACAO_UNIVERSO/`.
> O objetivo do projeto está no `PLANO.md`; a infraestrutura reaproveitável, no
> `INFRAESTRUTURA.md`; as regras de trabalho, no `CLAUDE.md`.

---

## 1. O que é a coleção

Uma **coleção didática de Direito brasileiro para concursos**, em **11 livros**.
Cada matéria é ensinada de duas formas que se complementam:

- **Pilar técnico** — o material jurídico puro (doutrina, lei, jurisprudência,
  tabelas, questões). Produzido **primeiro**.
- **Capítulo narrativo** — uma história que ensina o conteúdo do pilar de forma
  envolvente. Produzido **depois**, integra 100% o pilar.

Tudo se passa num **universo ficcional comum aos 11 livros**: **61
personagens-animais** representam as instituições do Estado brasileiro. O
protagonista fixo é **João**, um trabalhador rural que atravessa a coleção
inteira descobrindo o mundo institucional dentro de um sonho lúcido no **Templo
da República**.

### Os 11 livros
| # | Livro | # | Livro |
|---|---|---|---|
| 1 | Direito Constitucional | 7 | Processo Penal |
| 2 | Direito Administrativo | 8 | Direito do Trabalho |
| 3 | AFO (Adm. Financeira e Orçamentária) | 9 | Administração Geral/Pública |
| 4 | Direito Civil | 10 | Ética no Serviço Público |
| 5 | Processo Civil | 11 | Direitos Humanos |
| 6 | Direito Penal | | |

> O Livro 1 tem **19 capítulos**. Cada livro define seu próprio número de
> capítulos. Hoje há imagens prontas apenas dos **5 primeiros capítulos do
> Livro 1** (na máquina do autor, fora deste repositório).

---

## 2. O problema que a IA de imagem resolve

Modelos genéricos de imagem geram cenas bonitas, mas **não mantêm consistência**:
esquecem o rosto do personagem, mudam o traço de um capítulo para o outro,
destroem a identidade visual. Com **61 personagens recorrentes**, **11 livros** e
um **estilo visual próprio**, a consistência é o requisito central.

**O alvo:** uma IA especializada que garanta que "o Leão do STF" seja **sempre o
mesmo Leão, no mesmo traço**, do capítulo 1 do Livro 1 ao capítulo final do
Livro 11 — e que cada cena respeite a lógica visual do universo (abaixo).

---

## 3. O princípio do casting — família biológica = macrofunção

O elenco **não é aleatório**: cada **família biológica** espelha uma
**macrofunção** do Estado. A biologia do animal ensina a função. Para a IA de
imagem, isso é uma regra de **coerência visual por família**: animais da mesma
família compartilham gama de cor, porte e postura.

| Grupo | Família(s) | Macrofunção | Gama de cor / porte |
|---|---|---|---|
| 1 — Executivo: chefia | Canídeos selvagens | Comando do Executivo | Cinza/branco/marrom-terroso; atléticos |
| 2 — Executivo: segurança | Canídeos de trabalho | Polícia | Fardas; atléticos, alerta |
| 3 — Executivo: operacional | Diversas especializadas | Arrecadação, tesouro, etc. | Trajes funcionais |
| 4 — Legislativo | Primatas | Deliberação, voto | Cinza/marrom/negro; robustos, gestuais |
| 5 — Judiciário | Felinos | Julgar | Dourado/âmbar/negro/marfim; imponentes, eretos |
| 6 — Controle | Crocodilianos | Auditoria (TCU/TCE/CGU) | Verde-escuro/oliva; pesados, baixos |
| 7 — Funções essenciais | Aves (rapina/corvídeo/coruja) | MP, AGU, Defensoria, CNMP | Branco/negro/marrom-avermelhado; elegantes, asas visíveis |
| 8 — Forças Armadas | Rinoceronte/orca/águia | Defesa (terra/mar/ar) | Fardas verde/branca/azul |
| 9 — Regulação | Vespídeos + mamangava | Agências + CADE | Amarelo-e-preto |
| 10 — Sociedade | Diversas exclusivas | Cidadão, sociedade, sindicato, OAB | Cada ator com família própria |
| 11 — Entes federativos | Psitacídeos (araras/papagaio) | União, Estados, Municípios, DF | Azul/vermelho/verde/roxo; coloridos, vibrantes |
| 12 — Agentes públicos | Anfíbios | Regimes funcionais | Menores, humildes |
| 13 — Quarteto pop-up | Insetos + aranha | Disciplinas-base | **Estilo cartoon** (fora do realismo institucional) |

> **Regra visual de controle interno:** o **CNJ** é felino (pantera-negra) e o
> **CNMP** é ave de rapina (falcão) — eles controlam o próprio Poder por dentro,
> **não** migram para crocodiliano. Cada subgrupo de ave é visualmente distinto
> (a silhueta de uma arara ≠ a de uma águia ≠ a de uma coruja).

---

## 4. Catálogo dos 61 personagens

Coluna **Tier** = profundidade visual (define prioridade de treino — ver §6):
**T1** protagonista (LoRA dedicado), **T2** coadjuvante, **T3** figurante (estilo
+ prompt detalhado bastam).

### Grupo 1 — Executivo: chefia (canídeos selvagens)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 1 | Régis Federal | Lobo-cinzento | Presidente da República | T1 |
| 2 | Afonso Estadual | Coiote | Governador | T3 |
| 3 | Augusto Urbano | Chacal-dourado | Prefeito | T3 |
| 4 | Cassiano Esplanada | Licaon (cão-selvagem-africano) | Ministros/Secretários | T3 |
| 5 | Renata Autarca | Raposa | Administração indireta | T2 |

### Grupo 2 — Executivo: segurança pública (canídeos de trabalho)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 6 | Hector Federalis | Pastor-alemão | Polícia Federal | T2 |
| 7 | Raul Inquérito | Bloodhound | Polícia Civil / Delegado | T3 |
| 8 | Dimas Ostensivo | Dobermann | Polícia Militar | T3 |

### Grupo 3 — Executivo: operacionais e entidades (famílias diversas)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 9 | Aurora Horizonte | Grou | Planejamento/orçamento (SOF/SPI) | T2 |
| 10 | Augusta Fiscal | Formiga cortadeira | Arrecadação (Receita/Fazenda) | T2 |
| 11 | Valério Erário | Castor | Tesouro Nacional / Conta Única | T2 |
| 12 | Bruno Empenho | Tatu-galinha | Execução da despesa | T3 |
| 13 | Gael Laboris | Lobo-guará | MTE (Trabalho e Emprego) | T3 |
| 14 | Otávio Monetário | Esquilo | BACEN | T3 |
| 15 | Juvenal Segurado | Jabuti | INSS | T3 |

### Grupo 4 — Legislativo (primatas)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 16 | Tito Bicameral | Gorila | Congresso Nacional | T1 |
| 17 | Anselmo Federativo | Orangotango | Senado Federal | T1 |
| 18 | Chico Popular | Chimpanzé | Câmara dos Deputados | T1 |
| 19 | Bento Parlamentar | Macaco-prego | Assembleia Legislativa | T2 |
| 20 | Nico Edilidade | Sagui | Câmara Municipal | T3 |
| 21 | Helena Comissão | Lêmure-de-cauda-anelada | Fiscalização legislativa | T2 |

### Grupo 5 — Judiciário (felinos)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 22 | Leônidas Constitucional | Leão | STF | T1 |
| 23 | Augusto Uniformizador | Tigre | STJ | T1 |
| 24 | Caio Sufrágio | Onça-pintada | Justiça Eleitoral (TSE/TREs) | T2 |
| 25 | Domingos Dissídio | Caracal | Justiça do Trabalho (TST/TRTs) | T2 |
| 26 | Artur Castrense | Lince | Justiça Militar (STM) | T3 |
| 27 | Júlio Comarca | Gato-selvagem | Justiça Estadual (TJs) | T2 |
| 28 | Nyx Integridade | Pantera-negra | CNJ | T1 |
| 61 | ChaCha Seccional | Gata Bengal | Justiça Federal (TRF/juízes federais) | T2 |

> Atenção visual: a **onça-pintada** (Caio, #24) e a **gata Bengal** (ChaCha,
> #61) são distintas de propósito — Bengal tem rosetas/marmoreado dourado menores
> e porte doméstico; onça-pintada é selvagem, rosetas maiores.

### Grupo 6 — Controle e fiscalização (crocodilianos)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 29 | Crocus Contas | Crocodilo-do-nilo | TCU | T1 |
| 30 | Açu Auditor | Jacaré-açu | TCE | T3 |
| 31 | Jaciara Relatoria | Jacaré-açu fêmea | Conselheira de contas | T3 |
| 32 | Gavriel Transparência | Gavial | CGU | T3 |
| 33 | Otávio Controle Interno | Jacaré-do-papo-amarelo | Auditor interno | T3 |

### Grupo 7 — Funções essenciais à justiça (aves)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 34 | Álvaro Parquet | Águia-careca | Ministério Público | T1 |
| 35 | Fausto Corregedor | Falcão-peregrino | CNMP | T2 |
| 36 | Gu Advocatus | Corvo | AGU | T1 |
| 37 | Sofia Acesso | Coruja-das-neves | Defensoria Pública | T1 |

### Grupo 8 — Forças Armadas (terra/mar/ar)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 38 | Rômulo Soberania | Rinoceronte-branco | Exército | T2 |
| 39 | Orcus Atlântico | Orca | Marinha | T3 |
| 40 | Stella Aeroespacial | Águia-marinha-de-Steller | Força Aérea | T3 |

### Grupo 9 — Regulação e concorrência (vespídeos + mamangava)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 41 | Vésper Regulação | Vespa-mandarina | Agência reguladora federal | T3 |
| 42 | Selene Concessão | Vespa-caçadora | Agência reguladora setorial | T3 |
| 43 | Bruno Compliance | Marimbondo | Fiscalização operacional | T3 |
| 44 | Valentina Antitruste | Mamangava | CADE | T3 |

### Grupo 10 — Sociedade, setor privado e trabalho (famílias exclusivas)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 45 | **João** | Humano | Cidadão comum (PROTAGONISTA) | T1 |
| 46 | Clara Coletiva | Abelha-rainha | Sociedade civil organizada | T2 |
| 47 | Mirela Mercantil | Marta | Fornecedor / setor privado | T2 |
| 48 | Teodoro Convenção | Búfalo-africano | Sindicatos | T2 |
| 49 | Cervantes Ordem | Cervo-nobre (red deer) | OAB | T1 |

### Grupo 11 — Entes federativos (psitacídeos)
| # | Nome | Animal | Instituição | Tier |
|---|---|---|---|---|
| 50 | Magna Federativa | Arara-azul-grande | União | T1 |
| 51 | Rubra Federação | Arara-vermelha | Estado-membro | T1 |
| 52 | Municipalis | Papagaio-verdadeiro | Município | T2 |
| 53 | Capital Federativa | Espécie única (roxa/rosa) | Distrito Federal | T2 |

### Grupo 12 — Agentes públicos (anfíbios)
| # | Nome | Animal | Regime | Tier |
|---|---|---|---|---|
| 54 | Severino Estabilidade | Sapo-cururu | Estatutário (Lei 8.112/90) | T2 |
| 55 | Clara CLT | Perereca (rã-verde) | Celetista (CLT) | T2 |
| 56 | Téo Transitório | Girino | Temporário (art. 37, IX) | T3 |

### Grupo 13 — Quarteto pop-up (insetos + aranha — ESTILO CARTOON)
| # | Nome | Animal | Cor | Disciplina | Tier |
|---|---|---|---|---|---|
| 57 | Veríssimo Linguagem | Grilo | Verde | Português | T2 |
| 58 | Lúcia Algoritmo | Joaninha | Vermelho | Raciocínio Lógico | T2 |
| 59 | Lúmen Ético | Vaga-lume | Amarelo/luz | Ética | T2 |
| 60 | Nexus Digital | Aranha | Azul/prata | Informática | T2 |

> O Quarteto pop-up é desenhado em **estilo cartoon propositalmente diferente**
> do realismo institucional dos demais — quebra a quarta parede. Para a IA, é
> quase um **segundo estilo** dentro do mesmo projeto.

---

## 5. A lógica visual do espaço (cenários codificam a Constituição)

A geografia **não é decorativa** — ela codifica a estrutura constitucional. Três
eixos que devem aparecer na composição das cenas:

| Eixo | O que codifica | Como desenhar |
|---|---|---|
| **Vertical** | Hierarquia de instâncias | Mais alto = instância maior (STF no ápice). A Constituição/o Templo está **acima de tudo**. |
| **Horizontal** | Separação dos Poderes | Executivo, Legislativo e Judiciário **lado a lado**, sem hierarquia entre si. |
| **Concêntrico** | Pacto federativo | Círculos do centro para fora: União → Estados → Municípios (abrangência, não superioridade). |

As **funções essenciais** (MP, OAB, AGU, Defensoria — aves e cervo) **transitam**
entre os espaços: desenhá-las em movimento/voo entre os reinos comunica que não
pertencem a nenhum Poder.

**Narrador:** a **Voz do Templo** — a própria Constituição observando o mundo.
**Artefatos recorrentes:** o **Livro Dourado** (a Constituição), o **Templo da
República** (cenário-quadro). **Degradê:** o estilo acompanha a progressão do
livro (mais "história" no início, mais "estudo" no fim), mas o universo visual é
o mesmo do começo ao fim.

---

## 6. O que isso significa para o treino (resumo operacional)

- **1 LoRA de estilo** (o "traço da coleção") treinado nas imagens dos caps 1–5 +
  pranchas existentes — é a prioridade nº 1, garante a identidade do conjunto.
- **LoRAs de personagem só para os Tier 1** de início (João, Leônidas, Tito,
  Sofia, Álvaro, Cervantes, Gu, Crocus, Nyx, Augusto/STJ, Chico, Anselmo, Régis,
  Magna, Rubra). ~10–20 imagens variadas por personagem.
- **Tier 2 e Tier 3** se resolvem com o LoRA de estilo + prompt detalhado da
  ficha (animal + figurino + cor + acessório), sem LoRA dedicado — pelo menos no
  começo.
- **Coerência por família:** ao gerar, respeitar a gama de cor/porte da família
  (tabela §3) e as regras de figurino (toga preta no Judiciário, fardas nas
  Forças Armadas, etc. — detalhe no `referencia_visual/`).
- **O Quarteto pop-up** pede um tratamento de estilo separado (cartoon).
- **Texto dentro da imagem** (placas, "Livro Dourado", brasões) exige modelo base
  com bom encoder de texto (FLUX/SD3) e, em casos difíceis, ControlNet de
  tipografia — ver `PLANO.md`.

> **Fontes canônicas (no projeto-mãe, para consulta/atualização):**
> `00_FUNDACAO_E_GUIAS/FUNDACAO_UNIVERSO/` (fundamentos, lista de personagens,
> protagonistas por livro, glossário, manual de estilo) e
> `00_FUNDACAO_E_GUIAS/DIRECAO_ARTE/` (pranchas, sistema de cores, padronização
> visual). Em qualquer divergência, **a fonte canônica prevalece** sobre este
> resumo.
