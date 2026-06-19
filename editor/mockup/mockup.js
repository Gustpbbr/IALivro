// Mockup interativo da Etapa C — IALivro
// Carrega camadas_demo.json, renderiza bboxes clicáveis em cima da imagem
// e simula o painel de propriedades + ações de apagar.
//
// Refletindo o design system de ETAPA_C_DESIGN.md.

const SVG_NS = "http://www.w3.org/2000/svg";
let camadas = [];
let selecionadaId = null;
let bboxVisivel = true;

const CATALOGO_FONTES = {
  serif: [
    { id: "cormorant", nome: "Cormorant Garamond", classe: "fonte-cormorant" },
    { id: "source-serif", nome: "Source Serif Pro", classe: "fonte-source-serif" },
  ],
  sans_serif: [
    { id: "inter", nome: "Inter", classe: "fonte-inter" },
    { id: "work-sans", nome: "Work Sans", classe: "fonte-work-sans" },
  ],
  display: [
    { id: "cinzel", nome: "Cinzel", classe: "fonte-cinzel" },
    { id: "playfair", nome: "Playfair Display", classe: "fonte-playfair" },
  ],
};

// ============================================================
// CARGA
// ============================================================
async function carregar() {
  const resp = await fetch("camadas_demo.json");
  const dados = await resp.json();
  camadas = dados.camadas;
  renderizarBboxes();
  document.getElementById("painel-titulo").textContent =
    `${camadas.length} camadas detectadas`;
  toast("Imagem carregada. Toque numa camada pra editar.", "sucesso");
  atualizarCorLivro();
}

function renderizarBboxes() {
  const grupo = document.getElementById("grupo-bbox");
  grupo.innerHTML = "";

  const ordem = ["cena", "caixa", "linha_divisoria", "icone", "texto"];
  const ordenadas = [...camadas].sort(
    (a, b) => ordem.indexOf(a.tipo) - ordem.indexOf(b.tipo)
  );

  for (const c of ordenadas) {
    const rect = document.createElementNS(SVG_NS, "rect");
    rect.setAttribute("class", `bbox tipo-${c.tipo}`);
    rect.setAttribute("x", c.bbox.x);
    rect.setAttribute("y", c.bbox.y);
    rect.setAttribute("width", c.bbox.w);
    rect.setAttribute("height", c.bbox.h);
    rect.dataset.id = c.id;
    rect.addEventListener("click", (e) => {
      e.stopPropagation();
      selecionar(c.id);
    });
    grupo.appendChild(rect);
  }
}

function selecionar(id) {
  selecionadaId = id;
  document.querySelectorAll(".bbox").forEach((el) => {
    el.classList.toggle("selecionada", el.dataset.id === id);
  });
  renderizarPainel();
}

// ============================================================
// PAINEL
// ============================================================
function renderizarPainel() {
  const camada = camadas.find((c) => c.id === selecionadaId);
  const titulo = document.getElementById("painel-titulo");
  const corpo = document.getElementById("painel-corpo");
  const fechar = document.getElementById("painel-fechar");

  if (!camada) {
    titulo.textContent = "Toque numa camada";
    corpo.innerHTML = `<div class="vazio"><p>Toque numa camada da imagem pra editar.</p></div>`;
    fechar.hidden = true;
    return;
  }

  fechar.hidden = false;
  titulo.innerHTML = `${camada.id}<span class="tag-tipo tipo-${camada.tipo}">${camada.tipo}</span>`;

  let html = "";

  if (camada.tipo === "texto") {
    html += renderTexto(camada);
  } else if (camada.tipo === "caixa") {
    html += renderCaixa(camada);
  } else if (camada.tipo === "icone") {
    html += renderIcone(camada);
  } else if (camada.tipo === "cena") {
    html += renderCena(camada);
  } else if (camada.tipo === "linha_divisoria") {
    html += renderLinha(camada);
  }

  // Posição (todos exceto cena)
  if (camada.tipo !== "cena") {
    html += `<div class="linha-dupla" style="margin-top: var(--gap-2);">`;
    html += campoNumero("X", camada.bbox.x, 0, 1024, (v) => { camada.bbox.x = v; redesenharBbox(camada); }, "px");
    html += campoNumero("Y", camada.bbox.y, 0, 1536, (v) => { camada.bbox.y = v; redesenharBbox(camada); }, "px");
    html += `</div>`;
  }

  // Apagar
  if (camada.tipo !== "cena") {
    html += renderApagar(camada);
  }

  corpo.innerHTML = html;
}

function renderTexto(camada) {
  let html = campoTextarea("Conteúdo", camada.conteudo || "", (v) => {
    camada.conteudo = v;
  });
  const estilo = camada.estilo || {};

  html += campoCor("Cor do texto", estilo.cor || camada.cor_texto || "#000000", (v) => {
    camada.estilo = camada.estilo || {};
    camada.estilo.cor = v;
  });

  html += campoNumero("Tamanho", estilo.tamanho_px || 16, 8, 120, (v) => {
    camada.estilo = camada.estilo || {};
    camada.estilo.tamanho_px = v;
  }, "px");

  // Catálogo de fontes
  const classe = estilo.fonte_classe || camada.fonte_classe || "serif";
  const fonteId = estilo.fonte_id || CATALOGO_FONTES[classe][0].id;
  const opcoes = [];
  for (const [cls, fontes] of Object.entries(CATALOGO_FONTES)) {
    for (const f of fontes) {
      opcoes.push([f.id, `${cls === "sans_serif" ? "Sans" : cls.charAt(0).toUpperCase() + cls.slice(1)} · ${f.nome}`, cls]);
    }
  }
  html += campoSelectFonte("Fonte", fonteId, opcoes, (v, cls) => {
    camada.estilo = camada.estilo || {};
    camada.estilo.fonte_id = v;
    camada.estilo.fonte_classe = cls;
    atualizarPreviewFonte(camada);
  });

  // Preview da fonte com o conteúdo atual
  const fonteAtual = todasFontes().find(f => f.id === fonteId) || CATALOGO_FONTES.serif[0];
  html += `<div class="fonte-preview ${fonteAtual.classe}" id="fonte-preview" style="color: ${estilo.cor || "#000"}; background: #fff;">${escapeHtml((camada.conteudo || "Aa").slice(0, 30))}</div>`;

  html += campoSelect("Peso", estilo.peso || "normal",
    [["normal", "Normal"], ["bold", "Negrito"], ["light", "Fino"]],
    (v) => {
      camada.estilo = camada.estilo || {};
      camada.estilo.peso = v;
    });

  return html;
}

function renderCaixa(camada) {
  let html = campoCor("Cor de fundo", camada.cor_fundo || "#ffffff", (v) => {
    camada.cor_fundo = v;
  });
  html += campoCor("Cor da borda", camada.cor_borda || "#000000", (v) => {
    camada.cor_borda = v;
  });
  html += `<div class="linha-dupla">`;
  html += campoNumero("Borda", camada.espessura_borda || 0, 0, 10, (v) => {
    camada.espessura_borda = v;
  }, "px");
  html += campoNumero("Raio canto", camada.raio_canto || 0, 0, 50, (v) => {
    camada.raio_canto = v;
  }, "px");
  html += `</div>`;
  return html;
}

function renderIcone(camada) {
  let html = `<p style="margin-bottom: var(--gap-4); color: var(--texto-fraco); font-size: var(--font-sm);">
    ${escapeHtml(camada.observacoes || "Ícone identificado.")}
  </p>`;
  html += campoNumero("Largura", camada.bbox.w, 20, 400, (v) => {
    camada.bbox.w = v;
    redesenharBbox(camada);
  }, "px");
  html += campoNumero("Altura", camada.bbox.h, 20, 400, (v) => {
    camada.bbox.h = v;
    redesenharBbox(camada);
  }, "px");
  return html;
}

function renderCena(camada) {
  return `<p style="color: var(--texto-fraco); font-size: var(--font-sm); line-height: 1.5;">
    <strong style="color: var(--texto);">Cena central</strong> — esta é a ilustração principal.
    Edição da cena em si é feita re-gerando no ChatGPT.
    Aqui você só pode mover ou redimensionar.
  </p>`;
}

function renderLinha(camada) {
  let html = campoCor("Cor", camada.cor || "#888888", (v) => { camada.cor = v; });
  html += campoNumero("Espessura", camada.espessura || 1, 1, 10, (v) => {
    camada.espessura = v;
  }, "px");
  return html;
}

function renderApagar(camada) {
  let html = `<div class="acoes-apagar">`;
  html += `<button class="btn-apagar verde" onclick="toast('🟢 Apagar simples — revelaria fundo_limpo.png (grátis, instantâneo)', 'sucesso')">
    🟢 Apagar<small>fundo limpo</small>
  </button>`;
  if (camada.tipo === "caixa" || camada.tipo === "texto" || camada.tipo === "icone") {
    html += `<button class="btn-apagar amarelo" onclick="toast('🟡 Refazer fundo — chamaria inpainting (~US$ 0,02)', 'aviso')">
      🟡 Refazer<small>+ prompt</small>
    </button>`;
  }
  if (camada.tipo === "caixa") {
    html += `<button class="btn-apagar azul" onclick="toast('🔵 Estender cena — outpainting (~US$ 0,04)', 'info')">
      🔵 Estender<small>cena nova</small>
    </button>`;
  }
  html += `</div>`;
  return html;
}

function redesenharBbox(camada) {
  const rect = document.querySelector(`.bbox[data-id="${camada.id}"]`);
  if (!rect) return;
  rect.setAttribute("x", camada.bbox.x);
  rect.setAttribute("y", camada.bbox.y);
  rect.setAttribute("width", camada.bbox.w);
  rect.setAttribute("height", camada.bbox.h);
}

function atualizarPreviewFonte(camada) {
  const preview = document.getElementById("fonte-preview");
  if (!preview || !camada.estilo) return;
  const f = todasFontes().find((x) => x.id === camada.estilo.fonte_id);
  if (!f) return;
  preview.className = `fonte-preview ${f.classe}`;
  preview.textContent = (camada.conteudo || "Aa").slice(0, 30);
  preview.style.color = camada.estilo.cor || "#000";
}

function todasFontes() {
  return Object.values(CATALOGO_FONTES).flat();
}

// ============================================================
// HELPERS DE CAMPOS
// ============================================================
function campoTextarea(label, valor, onchange) {
  const id = `c_${Math.random().toString(36).slice(2, 9)}`;
  window["__handler_" + id] = (v) => {
    onchange(v);
    if (document.getElementById("fonte-preview")) {
      const cam = camadas.find(c => c.id === selecionadaId);
      if (cam) atualizarPreviewFonte(cam);
    }
  };
  return `
    <div class="campo">
      <label>${label}</label>
      <textarea oninput="window['__handler_${id}'](this.value)">${escapeHtml(valor)}</textarea>
    </div>
  `;
}

function campoCor(label, valor, onchange) {
  const id = `c_${Math.random().toString(36).slice(2, 9)}`;
  window["__handler_" + id] = (v) => {
    onchange(v);
    if (document.getElementById("fonte-preview") && label.toLowerCase().includes("texto")) {
      document.getElementById("fonte-preview").style.color = v;
    }
  };
  return `
    <div class="campo">
      <label>${label}</label>
      <div class="campo-cor">
        <input type="color" value="${valor}" oninput="window['__handler_${id}'](this.value); this.nextElementSibling.value=this.value">
        <input type="text" value="${valor}" oninput="window['__handler_${id}'](this.value); this.previousElementSibling.value=this.value">
      </div>
    </div>
  `;
}

function campoNumero(label, valor, min, max, onchange, sufixo = "") {
  const id = `c_${Math.random().toString(36).slice(2, 9)}`;
  window["__handler_" + id] = (v) => onchange(Number(v));
  return `
    <div class="campo">
      <label>${label}</label>
      <div class="campo-numero">
        <input type="range" min="${min}" max="${max}" value="${valor}" oninput="window['__handler_${id}'](this.value); this.nextElementSibling.textContent=this.value+'${sufixo}'">
        <span class="valor">${valor}${sufixo}</span>
      </div>
    </div>
  `;
}

function campoSelect(label, valor, opcoes, onchange) {
  const id = `c_${Math.random().toString(36).slice(2, 9)}`;
  window["__handler_" + id] = onchange;
  const opts = opcoes.map(([v, l]) =>
    `<option value="${v}" ${v === valor ? "selected" : ""}>${l}</option>`
  ).join("");
  return `
    <div class="campo">
      <label>${label}</label>
      <select onchange="window['__handler_${id}'](this.value)">${opts}</select>
    </div>
  `;
}

function campoSelectFonte(label, valor, opcoes, onchange) {
  const id = `c_${Math.random().toString(36).slice(2, 9)}`;
  window["__handler_" + id] = (v) => {
    const op = opcoes.find(o => o[0] === v);
    onchange(v, op ? op[2] : "serif");
  };
  const opts = opcoes.map(([v, l]) =>
    `<option value="${v}" ${v === valor ? "selected" : ""}>${l}</option>`
  ).join("");
  return `
    <div class="campo">
      <label>${label}</label>
      <select onchange="window['__handler_${id}'](this.value)">${opts}</select>
    </div>
  `;
}

// ============================================================
// LIVRO ATUAL
// ============================================================
function atualizarCorLivro() {
  const sel = document.getElementById("sel-livro");
  const cor = sel.options[sel.selectedIndex].dataset.cor;
  document.documentElement.style.setProperty("--livro-cor", cor);
  document.getElementById("livro-cor").style.background = cor;
}

// ============================================================
// TOASTS
// ============================================================
function toast(mensagem, tipo = "info") {
  const cont = document.getElementById("toasts");
  const el = document.createElement("div");
  el.className = `toast ${tipo}`;
  el.textContent = mensagem;
  cont.appendChild(el);
  const tempo = tipo === "erro" ? 8000 : 3000;
  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transition = "opacity 300ms";
    setTimeout(() => el.remove(), 300);
  }, tempo);
}
window.toast = toast;

// ============================================================
// EVENTOS GLOBAIS
// ============================================================
document.getElementById("btn-toggle-bbox").addEventListener("click", () => {
  bboxVisivel = !bboxVisivel;
  document.getElementById("grupo-bbox").classList.toggle("escondido", !bboxVisivel);
});

document.getElementById("painel-fechar").addEventListener("click", () => {
  selecionadaId = null;
  document.querySelectorAll(".bbox").forEach((el) => el.classList.remove("selecionada"));
  renderizarPainel();
});

document.getElementById("canvas").addEventListener("click", (e) => {
  if (e.target.id === "img-fundo" || e.target.id === "canvas") {
    selecionadaId = null;
    document.querySelectorAll(".bbox").forEach((el) => el.classList.remove("selecionada"));
    renderizarPainel();
  }
});

document.getElementById("sel-livro").addEventListener("change", () => {
  atualizarCorLivro();
  const livro = document.getElementById("sel-livro").options[document.getElementById("sel-livro").selectedIndex].text;
  toast(`Livro alterado para: ${livro}`, "info");
});

// Atalhos de teclado (desktop)
document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
  if (e.key === "Escape") {
    selecionadaId = null;
    document.querySelectorAll(".bbox").forEach((el) => el.classList.remove("selecionada"));
    renderizarPainel();
  } else if (e.key.toLowerCase() === "z" && !e.ctrlKey && !e.metaKey) {
    bboxVisivel = !bboxVisivel;
    document.getElementById("grupo-bbox").classList.toggle("escondido", !bboxVisivel);
  }
});

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

carregar().catch((err) => {
  toast(`Erro ao carregar: ${err.message}`, "erro");
});
