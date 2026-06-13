# ROADMAP — Do zero aos 11 livros ilustrados

> Guia mestre do projeto, criado em 12/06/2026. Status atualizado a cada marco.
> Legenda: ✅ concluído · 🔄 em andamento · ⬜ a fazer

---

## ETAPA 0 — Fundação ✅ CONCLUÍDA (11–12/06)

- [x] Repositório organizado (estrutura, README, .gitignore, docs)
- [x] Pesquisa profunda: Fable 5, estado da arte de consistência de personagem,
      Fal.ai vs Replicate, licenças (`docs/PESQUISA_FABLE5_E_ESTADO_DA_ARTE.md`)
- [x] PLANO.md atualizado com decisões técnicas (FLUX.1-dev base, fal.ai,
      modo rascunho/final, máx. 2 LoRAs de personagem por cena)
- [x] Alinhamento de produto 100%: 2 variações/cena, 4 perfis de enquadramento,
      tablet/HTML como destino, interface mobile-first, correção por inpainting,
      texto fixo na imagem, usuário único
- [x] Infraestrutura: conta fal.ai criada + `FAL_KEY` no cofre do GitHub
- [x] Ponte Drive→GitHub via Actions (importação automática funcionando)
- [x] 66 imagens importadas e triadas uma a uma (`docs/TRIAGEM_DATASET_2026-06-12.md`)
- [x] Linha de produção das pranchas definida: modelo de ficha v2 + checklist
      das 61 (Prancha A + Prancha B, bloco de renderização padrão, alturas)

## ETAPA 1 — Acervo canônico 🔄 EM ANDAMENTO

**Responsável: autor (outra aba, repo-mãe) · Custo: geração das pranchas**

- [🔄] Reescrever as 61 fichas no formato v2 e gerar Pranchas A + B
      (piloto Dimas aprovado; 16 pranchas antigas já importadas)
- [ ] Resolver os 6 conflitos canônicos da triagem (Livro 9, cor do DF, ursos,
      João realista, girino do Téo, nomes antigos)
- [ ] Subir pranchas novas no Drive → importação automática → triagem
- [ ] Enviar LISTA_FINAL consolidada (nomes/grupos/alturas) para sincronizar
      o UNIVERSO.md e fixar as trigger words
- [ ] **Cenas limpas**: confirmar se existem ilustrações de cena dos caps 1–5
      sem texto; se não, fabricar (Etapa 2)

> ⏱️ É o caminho crítico do projeto — o ritmo aqui define o ritmo do todo.
> Mínimo para destravar a Etapa 3: pranchas A+B de **João + Leônidas** + ~15
> imagens de estilo.

## ETAPA 2 — Preparação do dataset ⬜ (custo zero, agente)

- [x] Script de fatiamento (Pillow) ✅ (13/06 — `training/fatiar.py`, engine validada; coords finais no layout v2)
- [x] Banco de fichas canônicas v1 ✅ (13/06 — `referencia_visual/BANCO_FICHAS_CANONICAS.md`, 61 personagens + alturas + trigger words; reconciliar com LISTA_FINAL)
- [~] Gerador de captions baseline pronto ✅ (13/06 — `training/gerar_captions.py`); refinamento por imagem com visão quando o dataset real existir
- [ ] Dataset de estilo: recortes de arte pura + cenas fabricadas
      (Qwen-Edit/Nano Banana a partir da prancha do Templo) se necessário
- [ ] Montagem final: `dataset/100_estilo/`, `200_joao/`, `201_leonidas_stf/`

## ETAPA 3 — Treino piloto e validação (Fase 1 do PLANO) ⬜ ~US$ 10–15

- [x] Smoke test da FAL_KEY ✅ (12/06 — `outputs/smoke_test_templo.png`, circuito GitHub→fal→repo validado)
- [x] Workflow de treino/geração via GitHub Actions ✅ (12/06 — `fal-pipeline.yml`, tipo smoke_test; tipos treino_lora/geracao a adicionar)
- [~] Pipeline de treino/geração pronto ✅ (13/06 — tipos treino_lora e geracao em `processar_pedidos.py`, com trava de custo); falta disparar com dataset real
- [ ] Treinar LoRA de estilo (~US$ 2–3) → gerar testes → QA por vision + autor
- [ ] Treinar LoRAs João e Leônidas (~US$ 4–6) → testes de consistência
- [ ] A/B: FLUX.1-dev vs FLUX.2; modo rascunho (schnell) vs final (dev)
- [ ] **PORTEIRA: aprovação do autor** — só avança se o traço e os personagens
      convencerem. Senão: ajustar captions/pesos e re-treinar

## ETAPA 4 — Interface (Fase 2 do PLANO) ⬜ ~1–2 semanas de build

- [x] Maquete visual mobile-first (design) ✅ (13/06 — `design/mockup_*.png`); aguarda feedback do autor antes do build funcional

- [ ] Backend Python (FastAPI): diretor de arte (Opus/Sonnet via chave existente)
      → prompt técnico → fal.ai → 2 variações
- [ ] Interface mobile-first (Gradio/Streamlit): colar trecho OU pedido dirigido,
      menu de perfis de enquadramento, botões aprovar/corrigir (inpainting),
      painel de ajustes finos, 👍/👎
- [ ] Hospedagem no Railway (conta existente) + storage R2 (LoRAs e outputs)
- [ ] pytest + hooks de pre-commit + teste end-to-end pelo navegador
- [ ] Upscale 2x automático da variação aprovada

## ETAPA 5 — Produção em lote (Fase 3 do PLANO) ⬜

- [ ] Leitura dos capítulos HTML → identificação de cenas-chave e enquadramentos
- [ ] Ondas de LoRAs por ordem de aparição nos livros (todos T1; ~US$ 2–3/treino)
- [ ] Cenas de grupo: composição/inpainting ou referência nativa (Nano Banana)
- [ ] Imagens com texto (placas, brasões): motor de tipografia + QA letra a letra
- [ ] Lote do Livro 1 completo → revisão do autor → repetir por livro

## ETAPA 6 — Melhoria contínua (Fase 4 do PLANO) ⬜

- [ ] Feedback 👍/👎 alimentando re-treinos (com aviso de custo)
- [ ] Botão "Atualizar IA" (dataset vivo)
- [ ] Referências arrastáveis (modelos de edição por referência)
- [ ] LoRA cartoon do Quarteto pop-up

## ETAPA 4+ — Editor de composição por camadas ⬜ (backlog, upgrade da interface)

Mini-editor visual no navegador: cada personagem é uma camada (figurinha com
fundo transparente, gerada via LoRA) que o autor arrasta, redimensiona e
posiciona livremente numa tela; um botão "Harmonizar" faz um passe de IA
(inpainting/img2img leve) para unificar luz, sombra e bordas — composição
coesa, não colagem.
- "Girar" o personagem = trocar pela vista correta do turnaround (não rotacionar
  pixel) → alimentado diretamente pela **Prancha B** (5 vistas + poses).
- Tecnologia de harmonização: FLUX Kontext / Qwen-Edit / Nano Banana via API.
- Não exige novos insumos do autor: reusa as mesmas pranchas e LoRAs.
- Só depois da interface de chat (Etapa 4) validada.

---

## Expectativa de término (estimativas honestas)

| Marco | Estimativa | Depende de |
|---|---|---|
| Etapa 3 validada (estilo + 2 personagens aprovados) | **~1–2 semanas** | Pranchas de João/Leônidas + cenas de estilo prontas na outra aba |
| Sistema completo no ar (Etapa 4) | **~3–6 semanas** do início | Etapa 3 aprovada |
| Livro 1 ilustrado de ponta a ponta | ~2–4 semanas após o sistema no ar | Volume de cenas + ritmo de revisão do autor |
| Livros 2–11 | Contínuo — acompanha a escrita | Produção das pranchas + capítulos |

> **A variável dominante não é técnica — é o ritmo de produção das 61 pranchas
> e das aprovações do autor.** O pipeline em si (Etapas 2–4) soma ~3–4 semanas
> de engenharia. Custo total estimado até o sistema completo: **US$ 30–60**
> (piloto + primeiras ondas de treino + gerações de teste); Railway/R2 nas
> contas existentes.

## Próximas 3 ações concretas

1. **Autor**: produzir pranchas A+B de João e Leônidas (destravam a Etapa 3) e
   responder a pendência das cenas limpas dos caps 1–5.
2. **Agente**: smoke test da FAL_KEY (~US$ 0,03 — pedir OK) + script de
   fatiamento usando as 16 pranchas atuais como ensaio.
3. **Autor**: seguir a fábrica das demais 59 pranchas em paralelo.
