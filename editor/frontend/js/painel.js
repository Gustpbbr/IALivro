// Painel de propriedades. Renderiza por tipo + serializa patch pro backend.

import { CATALOGO_FONTES, todasFontes, fontePorId, rotuloClasse } from "./camadas/fontes.js";

let _onMudanca = null;     // callback (cid, patch)
let _onApagar = null;      // callback (cid, modo)

export function inicializarPainel(onMudanca, onApagar) {
  _onMudanca = onMudanca;
  _onApagar = onApagar;
}

export function renderizar(camada) {
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
  if (camada.tipo === "texto") html += renderTexto(camada);
  else if (camada.tipo === "caixa") html += renderCaixa(camada);
  else if (camada.tipo === "icone") html += renderIcone(camada);
  else if (camada.tipo === "cena") html += renderCena(camada);
  else if (camada.tipo === "linha_divisoria") html += renderLinha(camada);

  if (camada.tipo !== "cena") {
    html += `<div class="linha-dupla" style="margin-top: var(--gap-2);">`;
    html += campoNumero("X", camada.bbox.x, 0, 4000, (v) =>
      _onMudanca(camada.id, { bbox: { ...camada.bbox, x: v } })
    , "px");
    html += campoNumero("Y", camada.bbox.y, 0, 6000, (v) =>
      _onMudanca(camada.id, { bbox: { ...camada.bbox, y: v } })
    , "px");
    html += `</div>`;
    html += renderApagar(camada);
  }

  corpo.innerHTML = html;
}

function renderTexto(camada) {
  const estilo = camada.estilo || {};
  let html = campoTextarea("Conteúdo", camada.conteudo || "", (v) =>
    _onMudanca(camada.id, { conteudo: v })
  );

  html += campoCor("Cor do texto", estilo.cor || "#000000", (v) =>
    _onMudanca(camada.id, { estilo: { cor: v } })
  );

  html += campoNumero("Tamanho", estilo.tamanho_px || 16, 8, 120, (v) =>
    _onMudanca(camada.id, { estilo: { tamanho_px: v } })
  , "px");

  const classe = estilo.fonte_classe || "serif";
  const fonteId = estilo.fonte_id || CATALOGO_FONTES[classe][0].id;
  const opcoes = todasFontes().map((f) => {
    const cls = encontrarClasse(f.id);
    return [f.id, `${rotuloClasse(cls)} · ${f.nome}`, cls];
  });

  html += campoSelectFonte("Fonte", fonteId, opcoes, (v, cls) => {
    _onMudanca(camada.id, { estilo: { fonte_id: v, fonte_classe: cls } });
  });

  const fonte = fontePorId(fonteId) || CATALOGO_FONTES.serif[0];
  html += `<div class="fonte-preview ${fonte.classe}" style="color: ${estilo.cor || "#000"}; background: #fff;">
    ${escapeHtml((camada.conteudo || "Aa").slice(0, 30))}
  </div>`;

  html += campoSelect("Peso", estilo.peso || "normal",
    [["normal", "Normal"], ["bold", "Negrito"], ["light", "Fino"]],
    (v) => _onMudanca(camada.id, { estilo: { peso: v } })
  );

  return html;
}

function renderCaixa(camada) {
  let html = campoCor("Cor de fundo", camada.cor_fundo || "#ffffff", (v) =>
    _onMudanca(camada.id, { cor_fundo: v })
  );
  html += campoCor("Cor da borda", camada.cor_borda || "#000000", (v) =>
    _onMudanca(camada.id, { cor_borda: v })
  );
  html += `<div class="linha-dupla">`;
  html += campoNumero("Borda", camada.espessura_borda || 0, 0, 10, (v) =>
    _onMudanca(camada.id, { espessura_borda: v })
  , "px");
  html += campoNumero("Raio canto", camada.raio_canto || 0, 0, 50, (v) =>
    _onMudanca(camada.id, { raio_canto: v })
  , "px");
  html += `</div>`;
  return html;
}

function renderIcone(camada) {
  let html = `<p style="margin-bottom: var(--gap-4); color: var(--texto-fraco); font-size: var(--font-sm);">
    ${escapeHtml(camada.descricao || "Ícone identificado.")}
  </p>`;
  html += `<div class="linha-dupla">`;
  html += campoNumero("Largura", camada.bbox.w, 20, 600, (v) =>
    _onMudanca(camada.id, { bbox: { ...camada.bbox, w: v } })
  , "px");
  html += campoNumero("Altura", camada.bbox.h, 20, 600, (v) =>
    _onMudanca(camada.id, { bbox: { ...camada.bbox, h: v } })
  , "px");
  html += `</div>`;
  return html;
}

function renderCena(camada) {
  return `<p style="color: var(--texto-fraco); font-size: var(--font-sm); line-height: 1.5;">
    <strong style="color: var(--texto);">Cena central.</strong>
    A edição da cena em si é feita re-gerando no ChatGPT.
    Aqui só posição/escala.
  </p>`;
}

function renderLinha(camada) {
  let html = campoCor("Cor", camada.cor || "#888888", (v) =>
    _onMudanca(camada.id, { cor: v })
  );
  html += campoNumero("Espessura", camada.espessura || 1, 1, 10, (v) =>
    _onMudanca(camada.id, { espessura: v })
  , "px");
  return html;
}

function renderApagar(camada) {
  let html = `<div class="acoes-apagar">`;
  html += `<button class="btn-apagar verde" onclick="window.__apagar('${camada.id}', 'simples')">
    🟢 Apagar<small>fundo limpo</small>
  </button>`;
  if (["caixa", "texto", "icone"].includes(camada.tipo)) {
    html += `<button class="btn-apagar amarelo" onclick="window.__apagar('${camada.id}', 'refazer')">
      🟡 Refazer<small>+ prompt</small>
    </button>`;
  }
  if (camada.tipo === "caixa") {
    html += `<button class="btn-apagar azul" onclick="window.__apagar('${camada.id}', 'estender')">
      🔵 Estender<small>cena nova</small>
    </button>`;
  }
  html += `</div>`;
  return html;
}

window.__apagar = (cid, modo) => _onApagar(cid, modo);

// ============================================================
// HELPERS
// ============================================================
function encontrarClasse(fonteId) {
  for (const [cls, fontes] of Object.entries(CATALOGO_FONTES)) {
    if (fontes.some((f) => f.id === fonteId)) return cls;
  }
  return "serif";
}

let _seq = 0;
function novoId() { return `c_${++_seq}`; }

function campoTextarea(label, valor, onchange) {
  const id = novoId();
  window["__h_" + id] = onchange;
  return `<div class="campo">
    <label>${label}</label>
    <textarea oninput="window['__h_${id}'](this.value)">${escapeHtml(valor)}</textarea>
  </div>`;
}

function campoCor(label, valor, onchange) {
  const id = novoId();
  window["__h_" + id] = onchange;
  return `<div class="campo">
    <label>${label}</label>
    <div class="campo-cor">
      <input type="color" value="${valor}" oninput="window['__h_${id}'](this.value); this.nextElementSibling.value=this.value">
      <input type="text" value="${valor}" oninput="window['__h_${id}'](this.value); this.previousElementSibling.value=this.value">
    </div>
  </div>`;
}

function campoNumero(label, valor, min, max, onchange, sufixo = "") {
  const id = novoId();
  window["__h_" + id] = (v) => onchange(Number(v));
  return `<div class="campo">
    <label>${label}</label>
    <div class="campo-numero">
      <input type="range" min="${min}" max="${max}" value="${valor}" oninput="window['__h_${id}'](this.value); this.nextElementSibling.textContent=this.value+'${sufixo}'">
      <span class="valor">${valor}${sufixo}</span>
    </div>
  </div>`;
}

function campoSelect(label, valor, opcoes, onchange) {
  const id = novoId();
  window["__h_" + id] = onchange;
  const opts = opcoes.map(([v, l]) =>
    `<option value="${v}" ${v === valor ? "selected" : ""}>${l}</option>`
  ).join("");
  return `<div class="campo">
    <label>${label}</label>
    <select onchange="window['__h_${id}'](this.value)">${opts}</select>
  </div>`;
}

function campoSelectFonte(label, valor, opcoes, onchange) {
  const id = novoId();
  window["__h_" + id] = (v) => {
    const op = opcoes.find((o) => o[0] === v);
    onchange(v, op ? op[2] : "serif");
  };
  const opts = opcoes.map(([v, l]) =>
    `<option value="${v}" ${v === valor ? "selected" : ""}>${l}</option>`
  ).join("");
  return `<div class="campo">
    <label>${label}</label>
    <select onchange="window['__h_${id}'](this.value)">${opts}</select>
  </div>`;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
