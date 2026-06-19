# Como testar o editor — 3 caminhos

Escolha o que for mais fácil pra você. Em ordem de simplicidade pra celular:

---

## 🟢 Caminho A — Codespaces (recomendado, abre no navegador)

**Vantagens:** sem instalar nada, funciona no celular, GitHub cuida do servidor.
**Tempo:** ~2 minutos.
**Custo:** grátis até 60h/mês na conta pessoal.

### Passo a passo:

1. No celular, vá em https://github.com/Gustpbbr/IALivro
2. Botão verde **"Code"** → aba **"Codespaces"** → **"Create codespace on main"**
3. Aguarda 1-2 min — o GitHub abre uma IDE no navegador com tudo pronto
4. Na IDE, abre o **terminal** (botão "+ Terminal" no menu, ou Ctrl+`)
5. Cola e dá Enter:
   ```bash
   cd editor/backend && uvicorn main:app --host 0.0.0.0 --port 8000
   ```
6. Vai aparecer uma notificação tipo "Your application running on port 8000 is available" → clica **"Open in Browser"**
7. **Editor abre numa nova aba pública**. Esse é o link que você pode usar também no celular.

### Pra parar:
No terminal aperta `Ctrl+C`. Pra fechar o codespace: GitHub.com → **Codespaces** → ⋯ → **Stop**.

---

## 🟡 Caminho B — Railway (deploy persistente, sempre online)

**Vantagens:** URL pública permanente, mesmo depois de fechar tudo.
**Tempo:** ~5 minutos a primeira vez.
**Custo:** US$5/mês na sua conta Railway (que já existe).

### Passo a passo:

1. Acessa https://railway.app/new
2. **"Deploy from GitHub repo"** → seleciona **Gustpbbr/IALivro**
3. Em **Root Directory** coloca: `editor`
4. Railway lê o `Dockerfile` e `railway.toml` daquela pasta e faz o build
5. Quando terminar (~3 min), clica em **Generate Domain** → copia a URL
6. Abre essa URL no celular → editor pronto

### Pra atualizar:
Cada `git push main` re-deploya automático.

---

## 🔵 Caminho C — Local (Mac/Windows/Linux)

**Vantagens:** roda na sua máquina, controle total.
**Tempo:** ~3 minutos se já tem Python.
**Pré-requisito:** Python 3.11+ instalado.

### Passo a passo:

```bash
# 1. Clonar
git clone https://github.com/Gustpbbr/IALivro
cd IALivro/editor/backend

# 2. Ambiente virtual
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# 3. Dependências
pip install -r requirements.txt

# 4. Servir
uvicorn main:app --reload --port 8000
```

Abre `http://localhost:8000` no navegador.

### Pra acessar do celular na mesma rede WiFi:

1. Pega o IP local do seu computador:
   - **Mac/Linux:** `ifconfig | grep "inet " | grep -v 127.0.0.1`
   - **Windows:** `ipconfig` → procura "IPv4 Address"
2. Roda com `--host 0.0.0.0` em vez de só `--reload`:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3. No celular, acessa `http://SEU-IP:8000` (ex: `http://192.168.1.42:8000`)

---

## Sugestão de teste (qualquer caminho)

Tenho um `camadas.json` de exemplo (a imagem da Constituição que descompilamos). Sequência sugerida:

1. **Tela inicial** — clica em "Escolher camadas.json"
2. Sobe o arquivo `editor/mockup/camadas_demo.json` (basicamente o exemplo)
3. **Opcionalmente** sobe um fundo: `editor/mockup/fundo_demo.png`
4. Clica em "Iniciar edição"
5. Vai aparecer a imagem com 38 bboxes coloridas
6. Toca/clica em uma camada → painel abre
7. Muda texto, fonte, cor
8. Clica em "Exportar" — vai baixar o PNG editado em **modo diff** (só o que mudou)
9. Compara com o original

## O que esperar / o que não esperar

✅ Edição persiste — se sair e voltar, o estado da sessão mantém
✅ Mobile-first — bom em celular
✅ Trocar livro muda cor da topbar
✅ Atalho `Esc` deseleciona, `Z` esconde bboxes
✅ Modo diff: só altera o que você mexer

⚠️ Sem fundo enviado, exporta fundo branco
⚠️ Apagar 🟡/🔵 retorna 501 (precisa Fal — Etapa D)
⚠️ Não tem undo ainda (C10 — próxima sub-etapa)
⚠️ Imagens grandes podem demorar a renderizar

## Problema comum

**"Failed to fetch" ao subir JSON:** servidor não tá rodando ou porta errada. Confere se viu `Uvicorn running on http://0.0.0.0:8000`.

**Editor abre mas não carrega:** abre as DevTools do navegador (F12), aba "Console", e me manda o erro vermelho.

**Imagem do fundo é a imagem completa do ChatGPT:** uso modo diff por padrão pra preservar. Se quiser ver re-renderização total (precisaria de fundo limpo), passe `?modo=completo` no URL do export.
