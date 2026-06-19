# ETAPA C — Design System do Editor

> Companheiro do `ETAPA_C_ARQUITETURA.md`. Lá está **como** o editor funciona. Aqui está **como ele se parece**: paleta, tipografia, componentes, micro-interações.
>
> Este doc sai da aplicação da receita "Designer de Interface" da `Biblioteca-Claude-code`. Princípio guia: **o editor é ambiente neutro pra deixar as cores do livro brilharem.**

---

## 1. Hierarquia de cores — duas camadas

Existem **dois sistemas de cor** vivendo no editor, e é importante não misturar:

| Camada | Cores | Função |
|---|---|---|
| **UI do editor** (chrome, painéis, botões) | Paleta neutra/escura própria | Não competir com o conteúdo |
| **Tokens do projeto** (oferecidos ao autor) | 11 paletas dos livros + apoio + pop-up | O autor pinta texto/box/borda com essas |

A UI nunca usa as cores dos livros. Os tokens nunca aparecem no chrome. Disciplina.

---

## 2. Paleta da UI do editor (chrome)

Dark, quente, com toque dourado pra remeter à identidade do projeto sem ficar barulhento.

| Token | Hex | Uso |
|---|---|---|
| `--bg` | `#1a1614` | Fundo do palco e janela |
| `--painel-bg` | `#2a2218` | Painéis (topbar, propriedades) |
| `--borda` | `#3a302a` | Linhas divisórias, bordas de input |
| `--texto` | `#e8e0d0` | Texto principal da UI |
| `--texto-fraco` | `#a89b87` | Texto secundário/labels |
| `--acento` | `#c9a961` | Botões ativos, ícones, links (vem do **Dourado de apoio** §2) |
| `--acento-claro` | `#f0d89a` | Hover do acento, títulos no painel |

**Cores semânticas (feedback ao usuário):**

| Token | Hex | Uso |
|---|---|---|
| `--ok` | `#4ade80` | Sucesso, auto-save concluído, bbox texto |
| `--aviso` | `#facc15` | Atenção, custos médios, linha divisória |
| `--erro` | `#f87171` | Erro, conexão perdida |
| `--info` | `#60a5fa` | Informação, bbox caixa |

**Cores de bbox por tipo de camada** (já implementadas no mockup):

| Tipo | Hex | Token |
|---|---|---|
| texto | `#4ade80` | `--cor-texto-bbox` |
| caixa | `#60a5fa` | `--cor-caixa-bbox` |
| ícone | `#fb923c` | `--cor-icone-bbox` |
| cena | `#ec4899` | `--cor-cena-bbox` |
| linha_divisoria | `#facc15` | `--cor-linha-bbox` |

---

## 3. Tokens do projeto (oferecidos ao autor)

Quando o autor abre o seletor de cor de um texto/box no editor, ele vê **três abas**:

1. **Aba "Livro atual"** — paleta do livro em edição: principal + secundária + escala tonal (80/60/40/20%). Padrão.
2. **Aba "Apoio"** — Dourado de apoio, Preto suave, Cinza-escuro, Branco, Ouro Leônidas.
3. **Aba "Pop-up"** — quarteto cartoon (Veríssimo, Lúcia, Lúmen, Nexus) com seus 3 hex cada.

Fonte canônica: `SISTEMA_CORES_COMPLETO_v2.md`. Editor lê o arquivo, monta os seletores dinamicamente.

**Custom color picker** existe mas fica em aba secundária "Outras". Não quero o autor "inventando" cores fora da paleta.

---

## 4. Tipografia

### Catálogo de fontes oferecidas no editor

Pequeno e curado. 6 fontes — 2 serif, 2 sans, 2 display. Carregadas via Google Fonts (gratuitas, web-safe).

| Classe | Fonte primária | Fallback | Quando usar |
|---|---|---|---|
| `serif` | **Cormorant Garamond** | Georgia | Títulos clássicos, citações |
| `serif` | **Source Serif Pro** | Times New Roman | Corpo de texto editorial |
| `sans_serif` | **Inter** | system-ui | UI, listas, infográficos |
| `sans_serif` | **Work Sans** | Helvetica | Subtítulos, badges |
| `display` | **Cinzel** | Trajan, serif | Brasões, títulos solenes |
| `display` | **Playfair Display** | serif | Capas, destaques |

Mapeamento da Etapa B → C: `fonte_classe` retornado pelo Passo 5 sugere `serif`/`sans_serif`/`display`. Editor oferece as 2 fontes daquela classe e deixa autor escolher.

### Tipografia da própria UI

Toda interface usa **Inter** (system-ui fallback). Nunca usar fontes do catálogo de tokens na UI.

### Escala tipográfica

| Tamanho | Px | Uso na UI |
|---|---|---|
| `--font-xs` | 11 | Tags, badges, hint |
| `--font-sm` | 13 | Label de campo, texto secundário |
| `--font-base` | 15 | Texto padrão da UI |
| `--font-md` | 17 | Título do painel selecionado |
| `--font-lg` | 20 | Cabeçalho de sessão |

Editor de **conteúdo** (o texto da camada) — escala independente, controlada pelo autor em pixels.

---

## 5. Componentes base

### 5.1 Topbar (60px altura fixa)
```
[Logo IALivro] [livro atual: Constitucional ▼]    [👁 bbox]  [↺ desfazer]  [Exportar ↗]
```
- Logo à esquerda com seletor de livro atual (define paleta padrão dos tokens)
- Ações à direita: toggle bbox, undo, exportar
- Fundo `--painel-bg`, borda inferior `--borda`

### 5.2 Palco (canvas SVG)
- Fundo `#0d0a08` (mais escuro que `--bg`) pra criar contraste com o papel branco da imagem
- Imagem renderizada com sombra suave
- Bbox sobreposta com cor por tipo (ver §2)
- Camada selecionada: stroke 5px + fill com 18% de opacidade do acento

### 5.3 Painel de propriedades
- **Mobile (< 900px):** aparece embaixo, altura máx 50vh, scroll vertical
- **Desktop:** lateral direita, 360px largura fixa
- Cabeçalho fixo (sticky) com nome da camada + tag de tipo + botão fechar
- Cada campo segue padrão: `label uppercase + input grande (min 44px altura)`

### 5.4 Botões de apagar (tripla 🟢🟡🔵)
Renderizados como **3 botões adjacentes ocupando largura igual**, cada um com:
- Emoji + texto curto + descrição pequena embaixo
- Cor de fundo com 15% de opacidade da cor semântica (--ok/--aviso/--info)
- Min-height 56px (toque confortável)
- Active: `scale(0.97)` por 100ms

### 5.5 Campo de texto editável
- Background: `--bg` (mais escuro que o painel)
- Borda: 1px `--borda`
- Padding 10px 12px
- Border-radius 6px
- Focus: borda `--acento`

### 5.6 Seletor de cor
- Combo de `<input type="color">` 50x44px + texto hex monospace
- Editar qualquer lado atualiza o outro
- Sob título "Cor do texto" ou similar

### 5.7 Seletor de fonte
- Dropdown com `<select>` mostrando "Família: Serif · Fonte: Cormorant"
- 6 opções totais (ver §4)
- Preview rápido da fonte no item do dropdown

### 5.8 Slider de número
- `<input type="range">` ocupando 80% da largura + valor numérico fixo à direita
- Mostra unidade (`px`, `%`) junto do número

### 5.9 Toast / notificação
- Aparece no canto superior direito, slide-in 200ms
- Tipos: sucesso (verde), aviso (amarelo), erro (vermelho)
- Auto-dismiss em 3s, exceto erro (manual)
- Casos: "Auto-save concluído", "Inpainting em progresso", "Erro ao exportar"

---

## 6. Micro-interações

Pequenas, contidas, justificadas. Nunca decorativas.

| Gatilho | Animação | Duração |
|---|---|---|
| Selecionar camada | Bbox engrossa stroke + fill aparece | 150ms ease-out |
| Hover bbox (desktop) | Fill `rgba(255,255,255,0.08)` | 150ms |
| Botão active | `scale(0.97)` | 100ms |
| Painel abre/fecha (mobile) | Slide vertical | 250ms ease-out |
| Auto-save (concluído) | Indicador discreto pisca verde 1x | 800ms |
| Inpainting rodando | Indicador rotaciona até completar | infinito |
| Toast | Slide-in + fade-out | 200ms / 300ms |

**Sem decoração:** sem confetes ao exportar, sem partículas, sem hover-bounce. Editor profissional, não joguinho.

---

## 7. Layout responsivo (breakpoints)

| Largura | Layout |
|---|---|
| `< 600px` | Mobile portrait. Painel embaixo, palco rola horizontal se imagem for grande. |
| `600-899px` | Mobile landscape / tablet portrait. Mesmo layout mobile mas com mais respiro. |
| `≥ 900px` | Desktop. Painel à direita 360px, palco centralizado. |

Tudo testado com toque (grandes alvos: 44x44px min) e com mouse.

---

## 8. Acessibilidade

- Contraste mínimo 4.5:1 pra textos (`--texto` sobre `--bg` = 11:1 ✅)
- Foco visível em todos os controles via `outline: 2px solid var(--acento)`
- Atalhos de teclado pra desktop:
  - `Esc` — deseleciona camada
  - `Del` — abre menu apagar
  - `Z` — toggle bbox
  - `Ctrl/Cmd + Z` — desfazer
  - `Ctrl/Cmd + Shift + Z` — refazer

---

## 9. Variáveis CSS centralizadas (entregável)

Todo CSS deriva de variáveis. Quando virar implementação, mora num arquivo `:root` único. Esqueleto:

```css
:root {
  /* Cores UI */
  --bg: #1a1614;
  --painel-bg: #2a2218;
  --borda: #3a302a;
  --texto: #e8e0d0;
  --texto-fraco: #a89b87;
  --acento: #c9a961;
  --acento-claro: #f0d89a;

  /* Semânticas */
  --ok: #4ade80;
  --aviso: #facc15;
  --erro: #f87171;
  --info: #60a5fa;

  /* Bbox por tipo */
  --cor-texto-bbox: #4ade80;
  --cor-caixa-bbox: #60a5fa;
  --cor-icone-bbox: #fb923c;
  --cor-cena-bbox: #ec4899;
  --cor-linha-bbox: #facc15;

  /* Tipografia */
  --font-ui: 'Inter', system-ui, sans-serif;
  --font-xs: 11px;
  --font-sm: 13px;
  --font-base: 15px;
  --font-md: 17px;
  --font-lg: 20px;

  /* Espaçamento (escala 4) */
  --gap-1: 4px;
  --gap-2: 8px;
  --gap-3: 12px;
  --gap-4: 16px;
  --gap-6: 24px;
  --gap-8: 32px;

  /* Raio */
  --raio-sm: 4px;
  --raio-md: 6px;
  --raio-lg: 12px;

  /* Sombra */
  --sombra-suave: 0 2px 6px rgba(0,0,0,0.3);
  --sombra-forte: 0 4px 20px rgba(0,0,0,0.5);
}
```

---

## 10. O que NÃO entra neste design system

- Tema claro / dark mode toggle — single mode (escuro) é suficiente pra POC
- Customização de tema pelo usuário — fora de escopo
- Animações de loading complexas — usa indicadores discretos
- Ícones decorativos extras — só funcionais
- Mais de 6 fontes no catálogo — disciplina importa

---

## 11. Próximos passos depois deste doc

1. Atualizar o mockup (`editor/mockup/`) pra refletir 100% deste design
2. Codar `editor/frontend/css/tokens.css` com as variáveis acima
3. Codar componentes base como classes utilitárias (`.btn-apagar`, `.campo`, etc.)
4. Validar com autor: paleta, fontes escolhidas, hierarquia visual

---

**Versão:** 1
**Última atualização:** 2026-06-19
**Origem do método:** receita "Designer de Interface" — `Gustpbbr/Biblioteca-Claude-code`
