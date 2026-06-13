# Fatiamento de pranchas

`training/fatiar.py` recorta painéis nomeados de uma prancha, em coordenadas
**fracionárias** (independentes da resolução).

## Fluxo
1. `python training/fatiar.py grade <prancha.png>` → gera `<prancha>__grade.png`
   com uma grade 10×10 rotulada (0.0–1.0) para localizar os painéis.
2. Criar `training/fatiamento/<personagem>.json` com os recortes (ver `leonidas.json`).
3. `python training/fatiar.py recortar training/fatiamento/<personagem>.json`
   → recortes salvos em `<saida>/<trigger>__<nome>.png`.

## Importante
- A engine está **validada** (piloto Leônidas, 12/06/2026).
- As 16 pranchas atuais são da geração antiga e serão substituídas pelas v2
  (Prancha A + B, layout fixo). Quando as v2 chegarem, define-se **um conjunto
  de coordenadas por tipo de prancha** (A e B) e reusa-se nas 61 — caçar
  coordenada por imagem só é necessário enquanto o layout varia.
- `leonidas.json` fica como exemplo de formato.
