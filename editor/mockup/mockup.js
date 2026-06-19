// Mockup interativo da Etapa C — IALivro
// Carrega camadas_demo.json, renderiza bboxes clicáveis em cima da imagem
// e simula o painel de propriedades + ações de apagar.
//
// É só simulação. Não chama backend. As mudanças vivem na memória até reload.

const SVG_NS = "http://www.w3.org/2000/svg";
let camadas = [];
let selecionadaId = null;
let bboxVisivel = true;

async function carregar() {
  const resp = await fetch("camadas_demo.json");
  const dados = await resp.json();
  camadas = dados.camadas;
  renderizarBboxes();
  document.getElementById("painel-titulo").textContent =
    `${camadas.length} camadas detectadas`;
}

function renderizarBboxes() {
  const grupo = document.getElementById("grupo-bbox");
  grupo.innerHTML = "";

  // Renderiza primeiro cena (maior), depois caixas, depois textos/ícones
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
    html += campoTextarea("Conteúdo", camada.conteudo || "", (v) => {
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
    html += campoSelect("Família de fonte",
      estilo.fonte_classe || camada.fonte_classe || "serif",
      [
        ["serif", "Serif (clássica)"],
        ["sans_serif", "Sans-serif (limpa)"],
        ["display", "Display (decorativa)"],
      ],
      (v) => {
        camada.estilo = camada.estilo || {};
        camada.estilo.fonte_classe = v;
      });
    html += campoSelect("Peso", estilo.peso || "normal",
      [["normal", "Normal"], ["bold", "Negrito"], ["light", "Fino"]],
      (v) => {
        camada.estilo = camada.estilo || {};
        camada.estilo.peso = v;
      });
  } else if (camada.tipo === "caixa") {
    html += campoCor("Cor de fundo", camada.cor_fundo || "#ffffff", (v) => {
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
  } else if (camada.tipo === "icone") {
    html += `<p style="margin-bottom: 14px; color: rgba(232,224,208,0.7); font-size: 14px;">
      ${camada.observacoes || "Ícone identificado."}
    </p>`;
    html += campoNumero("Largura", camada.bbox.w, 20, 400, (v) => {
      camada.bbox.w = v;
    }, "px");
  } else if (camada.tipo === "cena") {
    html += `<p style="color: rgba(232,224,208,0.7); font-size: 14px; line-height: 1.5;">
      <strong>Cena central</strong> — esta é a ilustração principal. Edição da cena em si é feita re-gerando no ChatGPT.
      Aqui você só pode mover ou redimensionar.
    </p>`;
  } else if (camada.tipo === "linha_divisoria") {
    html += campoCor("Cor", camada.cor || "#888888", (v) => { camada.cor = v; });
    html += campoNumero("Espessura", camada.espessura || 1, 1, 10, (v) => {
      camada.espessura = v;
    }, "px");
  }

  // Posição (todos)
  html += `<div class="linha-dupla" style="margin-top: 8px;">`;
  html += campoNumero("X", camada.bbox.x, 0, 1024, (v) => { camada.bbox.x = v; redesenharBbox(camada); }, "px");
  html += campoNumero("Y", camada.bbox.y, 0, 1536, (v) => { camada.bbox.y = v; redesenharBbox(camada); }, "px");
  html += `</div>`;

  // Apagar
  if (camada.tipo !== "cena") {
    html += `<div class="acoes-apagar">`;
    html += `<button class="btn-apagar verde" onclick="alert('🟢 Apagar simples — revelaria fundo_limpo.png (grátis, instantâneo)')">
      🟢 Apagar<small>fundo limpo</small>
    </button>`;
    if (camada.tipo === "caixa" || camada.tipo === "texto" || camada.tipo === "icone") {
      html += `<button class="btn-apagar amarelo" onclick="alert('🟡 Apagar + refazer fundo — chamaria inpainting com prompt (~US$ 0,02)')">
        🟡 Refazer<small>+ prompt</small>
      </button>`;
    }
    if (camada.tipo === "caixa") {
      html += `<button class="btn-apagar azul" onclick="alert('🔵 Apagar + estender cena — outpainting (~US$ 0,04)')">
        🔵 Estender<small>cena nova</small>
      </button>`;
    }
    html += `</div>`;
  }

  corpo.innerHTML = html;
  ligarCampos(camada);
}

function redesenharBbox(camada) {
  const rect = document.querySelector(`.bbox[data-id="${camada.id}"]`);
  if (!rect) return;
  rect.setAttribute("x", camada.bbox.x);
  rect.setAttribute("y", camada.bbox.y);
  rect.setAttribute("width", camada.bbox.w);
  rect.setAttribute("height", camada.bbox.h);
}

// ----- helpers de campos -----

function campoTextarea(label, valor, onchange) {
  const id = `c_${Math.random().toString(36).slice(2, 9)}`;
  window["__handler_" + id] = onchange;
  return `
    <div class="campo">
      <label>${label}</label>
      <textarea oninput="window['__handler_${id}'](this.value)">${escapeHtml(valor)}</textarea>
    </div>
  `;
}

function campoCor(label, valor, onchange) {
  const id = `c_${Math.random().toString(36).slice(2, 9)}`;
  window["__handler_" + id] = onchange;
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

function ligarCampos(camada) {
  // hooks futuros pra preview ao vivo
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ----- eventos globais -----

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

carregar().catch((err) => {
  document.getElementById("painel-titulo").textContent = "Erro ao carregar";
  document.getElementById("painel-corpo").innerHTML =
    `<p style="color: var(--vermelho); padding: 14px;">${err.message}</p>`;
});
