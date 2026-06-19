# Mockup interativo — Editor Etapa C

Demo estática do editor de descompilação. Abre no celular ou no navegador desktop, carrega a imagem de exemplo do ChatGPT (Constituição) e mostra as 38 camadas detectadas pela Etapa B como áreas clicáveis.

## Pra abrir

### Opção 1 — Servidor local
```bash
cd editor/mockup
python3 -m http.server 8000
# abre http://localhost:8000 no celular (na mesma rede WiFi: http://<IP-do-PC>:8000)
```

### Opção 2 — GitHub Pages
Se ativar Pages no repo (Settings → Pages → branch main, pasta `/editor/mockup`), abre em qualquer celular sem servidor local.

### Opção 3 — Abrir o arquivo direto
Tem dia que abrir `index.html` no navegador funciona. Tem dia que CORS bloqueia o `fetch()` do JSON. Se acontecer, use a opção 1.

## O que tem de verdade aqui

✅ Renderiza imagem do ChatGPT + 38 bboxes coloridas por tipo
✅ Toque/clique em camada abre painel com propriedades
✅ Edita texto, fonte, cor, tamanho, peso (mudanças vivem em memória até reload)
✅ Botões 🟢 🟡 🔵 de apagar (mostram alerta explicando o que aconteceria)
✅ Botão 👁 esconde bboxes pra ver a imagem original
✅ Layout mobile-first; em telas grandes painel vai pra direita
✅ Mover X/Y de uma camada atualiza a bbox em tempo real

## O que NÃO tem (vai pra implementação de verdade)

❌ Edição visual real do texto (mostra na imagem). Hoje só edita os campos.
❌ Apagar não apaga visualmente. Só alert.
❌ Sem backend, sem exportação real.
❌ Não chama Fal/Anthropic.
❌ Sem auto-save.
❌ Sem undo/redo.

## Por que esse mockup importa

Antes de gastar 2 semanas codando o editor de verdade, o autor toca, testa, sente. Decide:

- Os tamanhos de toque tão bons no celular?
- As bboxes coloridas ajudam ou poluem?
- O painel embaixo é confortável ou precisa ir pro lado?
- As 3 opções de apagar fazem sentido?
- Falta algo óbvio?

Tudo que sair desse teste vira ajuste no `ETAPA_C_ARQUITETURA.md` antes de partir pra implementação.
