# Triagem visual do acervo — 12/06/2026

> 66 imagens importadas do Google Drive (`dataset/_inbox/`) e analisadas uma a uma
> por vision (4 lotes em paralelo). Este documento consolida a classificação, o
> plano de aproveitamento e as pendências canônicas para decisão do autor.

## Visão geral

| Categoria | Qtde aprox. | Aproveitamento |
|---|---|---|
| Pranchas individuais de personagem (template completo: vistas + paleta + texturas) | 15 personagens + Templo da República | Fatiar: vistas/close-ups → dataset de personagem; textos → captions e fichas canônicas |
| Pranchas de grupo (retratos por família: felinos, jacarés, primatas, aves, militares…) | ~12 pranchas, ~40 retratos | Recortar retratos individuais → datasets de personagem |
| Fichas de identidade visual dos livros (paleta/tipografia/ícones) | ~13 | **Fora do treino** → referência canônica do diretor de arte |
| Infográficos didáticos (conceitos com texto/setas) | ~6 | Recorte cuidadoso só das vinhetas/personagens limpos |
| "Relíquias" (artefatos: Livro Dourado, balança, toga, cofre do Erário, selo) | 2 | Recortes de props canônicos — ouro para consistência de objetos |
| **Cenas ilustradas limpas (sem texto)** | **0** | ⚠️ Ver pendência nº 1 |

## Cobertura de personagens

**15 personagens com prancha individual completa** (em `pranchas_individuais/`):
João (#45), Leônidas (#22), Tito (#16), Anselmo (#17), Chico (#18), Cervantes (#49),
Magna (#50), Rubra (#51), Municipalis (#52), Capital Federativa (#53), Renata (#5),
Mirela (#47), Severino (#54), Clara CLT (#55), Téo (#56). + **Templo da República** (cenário).

**Dos 15 Tier 1**: 8 cobertos com prancha individual. Faltam: Sofia, Álvaro, Gu,
Crocus*, Nyx*, Augusto/STJ* e Régis* (*têm retratos bons em pranchas de grupo).

~40 personagens adicionais aparecem em pranchas de grupo com retratos recortáveis.

## ⚠️ Pendências para decisão do AUTOR

1. **Não há cenas limpas no acervo.** Tudo tem texto/diagramação. O LoRA de estilo
   pode ser treinado com recortes das regiões de arte pura, mas: **existem
   ilustrações de cena "puras" dos caps 1–5 ainda não subidas?** Se sim, subir;
   se não, treinamos com recortes + fabricação.
2. **Conflito Livro 9**: uma ficha diz teal `#2A8B8B` ("Administração Geral"),
   outra diz azul `#3891D6` ("Direito Administrativo Geral"). Qual vale?
3. **Cor do DF**: a prancha individual (Capital Federativa) é roxa/rosa — bate com
   o UNIVERSO.md ✅. Mas dois infográficos de Entes Federativos mostram o DF como
   arara-canindé (azul/amarela) e arara vermelha-e-verde. Confirmar que roxa/rosa
   é o cânone e que os infográficos são versões antigas.
4. **Nomes divergentes** (pranchas vs UNIVERSO.md) — indicam material de geração
   anterior do universo. Exemplos: "Leônidas Supremo" vs Leônidas Constitucional;
   "Gregório Congresso" vs Tito Bicameral; "Álvaro Custos" vs Álvaro Parquet;
   "Baltasar/Boris/Nestor" vs Régis/Afonso/Augusto; "Domingos Labor" como felino
   pintado vs caracal (canônico). **Vale o UNIVERSO.md?** (Regra de Ouro nº 2 diz
   que sim — confirmar e padronizar trigger words pelo cânone.)
5. **Prancha dos URSOS** (`...e9fd7de1`): casting de entes federativos abandonado
   (ursos ≠ psitacídeos). Proposta: arquivar como histórico, **nunca treinar**.
6. **João em estilo cartoon** numa prancha de grupo (`...78572d7d`) vs João
   realista na prancha individual. Confirmar: o João canônico é o realista?

## Plano de aproveitamento (próxima etapa)

1. Renomear os 66 arquivos com nomes significativos (ex.:
   `prancha_leonidas_stf.png`, `identidade_livro08_trabalho.png`).
2. Reorganizar: pranchas → `referencia_visual/pranchas/`; identidades →
   `referencia_visual/guias/identidades/`; infográficos → `referencia_visual/infograficos/`.
3. Fatiar pranchas individuais (script Pillow): vistas + close-ups → datasets.
4. Extrair fichas canônicas de texto de cada prancha (banco do diretor de arte).
5. Montar dataset do LoRA de estilo com os recortes de arte pura + avaliar
   fabricação de cenas (Qwen-Edit/Nano Banana) a partir da prancha do Templo.

---

## Tabelas completas por lote

### Lote 1 — raiz (16 arquivos)

| arquivo | categoria | conteúdo | texto | destino |
|---|---|---|---|---|
| 7f91191c | identidade-livro | Livro 8 — Trabalho (laranja #E85D04) | muito | referência |
| 8b4256dd | prancha-grupo | Felinos Judiciário: J. Trabalho, J. Militar, J. Estadual | muito | recortar |
| d29c2141 | identidade-livro | Livro 7 — Proc. Penal (vermelho) | muito | referência |
| 7a0d8fcc | infográfico | Entes Federativos (4 psitacídeos; DF=canindé ⚠️) | muito | recortar |
| 3e61da7e | infográfico | "Forças Invisíveis" (prescrição, coisa julgada) | muito | recortar |
| d0f7a59f | ficha | Dossiê Crocus/TCU (2 págs) | muito | referência |
| cea1c00b | prancha-grupo | Forças Armadas: Exército, Marinha, FAB — altíssima qualidade | pouco | recortar ⭐ |
| 670abb22 | identidade-livro | Livro 1 — Constitucional (ocre) | muito | referência |
| 5e44accb | identidade-livro | Família dos Azuis (Livros 2/3/9) | muito | referência |
| 6f25f0c6 | prancha-grupo | 5 crocodilianos do Controle | pouco | recortar |
| 8c83c5b1 | identidade-livro | Livro 10 — Ética (roxo) | muito | referência |
| aa3e41ee | infográfico | "Forças que Transformam o Estado" | muito | recortar |
| 0c8cdec8 | infográfico | Entes Federativos v2 (DF=vermelha ⚠️ duplicata divergente) | muito | recortar |
| 85311fca | ficha | Crocus/TCU individual (retrato bom) | muito | recortar |
| 13272e4d | identidade+arte | Livro 1 com Leônidas segurando a Constituição ⭐ | muito | recortar |
| 8b1bef67 | identidade-livro | Paletas Livros 10 e 11 | muito | referência |

### Lote 2 — raiz (16 arquivos)

| arquivo | categoria | conteúdo | texto | destino |
|---|---|---|---|---|
| 23d56f30 | guia de cores | Vermelhos e laranjas institucionais | muito | referência |
| 7ee3bdf6 | prancha-grupo | Legislativo: 6 primatas (retratos excelentes) | muito | recortar ⭐ |
| 39fe0c33 | infográfico | "Três Guardiões": Crocus, Álvaro, Leônidas | muito | recortar |
| 5ee29b53 | prancha | Teodoro/Sindicatos (búfalo) retrato grande | muito | recortar |
| 00850c00 | infográfico | Agentes públicos: 3 anfíbios | muito | recortar |
| 2d621043 | identidade-livro | Livro 2 — Administrativo (azul-marinho) | muito | referência |
| 7a90b042 | prancha-grupo | Legislativo compacto + paletas individuais | muito | recortar |
| 2690f321 | identidade-livro | Livro 4 — Civil (verde-floresta) | muito | referência |
| 5a1ebfae | prancha-grupo | Funções Essenciais: 4 aves em ternos | muito | recortar ⭐ |
| 2490d7ed | identidade-livro | Livro 3 — AFO (azul-petróleo) | muito | referência |
| 243dba87 | infográfico | Entes Federativos (DF com fundo de Brasília) | muito | recortar |
| d21e4753 | prancha-grupo | Judiciário togado: Leônidas, Augusto/STJ, Caio — "quase cena" | muito | recortar ⭐ |
| 96294ba4 | ficha | Crocus canônica (texto denso) | muito | referência |
| 3645fd95 | identidade-livro | Livro 11 — Direitos Humanos (rosa) | muito | referência |
| a9a9dd1a | prancha-grupo | Ciclo orçamentário: coruja, formiga, castor, tatu | muito | recortar |
| d650d49c | prancha-grupo | Executivo orçamentário (poses alternativas) | pouco | recortar |

### Lote 3 — raiz (18 arquivos)

| arquivo | categoria | conteúdo | texto | destino |
|---|---|---|---|---|
| af70b2b9 | prancha-grupo | Executivo: lobo, coiote, chacal, licaon, raposa (nomes antigos ⚠️) | muito | recortar |
| 2cdcd6ac | prancha-grupo | Segurança: pastor-alemão, bloodhound, dobermann (+lobo-guará) | muito | recortar |
| eafc3e6d | identidade-livro | Livro 5 — Proc. Civil (verde-oliva) | muito | referência |
| aac5f137 | identidade-livro | Família dos Azuis (Livro 9 = teal ⚠️ conflito) | muito | referência |
| e96c014f | ficha | TCU/Crocus competências (texto jurídico) | muito | referência |
| fec35a35 | identidade-livro | Livro 6 — Penal (vermelho-escuro) | muito | referência |
| bc9e6c2c | prancha-grupo | 5 crocodilianos do Controle (v2) | muito | recortar |
| e599499f | infográfico | "Relíquias da Justiça": Livro Dourado, balança, toga ⭐ props | muito | recortar |
| cad5ca41 | prancha-grupo | Autônomas: Nyx/CNJ, Cervantes/OAB, BACEN, INSS, CADE | muito | recortar ⭐ |
| a46bc3c6 | identidade-livro | Família dos Verdes (Livros 4 e 5) | muito | referência |
| a6bc006d | prancha-grupo | Regulação: 3 vespídeos (falta mamangava) | muito | recortar |
| e9fd7de1 | prancha-grupo | URSOS — casting abandonado ⚠️ NÃO TREINAR | muito | arquivo histórico |
| c76238ec | prancha-grupo | Quarteto pop-up cartoon (2º estilo) | muito | recortar (dataset cartoon) |
| 3bacc23b | identidade-livro | Livro 9 = azul #3891D6 ⚠️ conflito com aac5f137 | muito | referência |
| 5d3d9da5 | prancha-grupo | Judiciário: 6 felinos (Domingos como pintado vs caracal ⚠️) | pouco | recortar ⭐ |
| 965cec0b | ficha | Crocus character sheet (template bom) | muito | recortar |
| e287f61c | infográfico | "Relíquias da Administração": cofre, selo, inquérito ⭐ props | muito | recortar |
| 78572d7d | prancha-grupo | Sociedade: João CARTOON ⚠️, Clara abelha, Mirela | pouco | recortar (validar João) |

### Lote 4 — pranchas individuais (16 arquivos)

| arquivo | personagem/cenário | nota |
|---|---|---|
| 68bdae8a | **Templo da República** (cenário) | Completa: exterior, interior, Livro Dourado, luz ao longo do dia ⭐ |
| faa0b3a5 | Leônidas (#22) | "Leônidas Supremo" na prancha ⚠️ nome |
| f2856d9c | Tito Bicameral (#16) | Sem divergências |
| 50f52e63 | Chico Popular (#18) | Cena hero no plenário |
| c07e43cb | Cervantes Ordem (#49) | Tribuna da OAB |
| 8b702178 | Anselmo Federativo (#17) | Pelagem ruiva, contraste com Chico |
| 9c2e2402 | Renata Autarca (#5) | Organograma da Adm. Indireta |
| ca702cbf | Clara CLT (#55) | Comparativo celetista×estatutário |
| 0339fa39 | Severino Estabilidade (#54) | Caracterização excelente |
| 36222f03 | Mirela Mercantil (#47) | Cross-over com os 3 vínculos |
| 3fbe7930 | Téo Transitório (#56) | Girino não-antropomorfizado (confirmar) |
| 609fc5a2 | **João (#45)** | Progressão narrativa Livro 1→11 ⭐; chapéu de palha = âncora |
| ec6faffd | Magna Federativa (#50) | Azuis fiéis ao Grupo 11 |
| 9ffd05d1 | Rubra Federação (#51) | Silhueta distinta da Magna ✅ |
| f7dff6f8 | Municipalis (#52) | Art. 30, "ente mais próximo" |
| 1230a8ec | Capital Federativa (#53) | DF roxa/rosa ✅ híbrido com 2 livros |
