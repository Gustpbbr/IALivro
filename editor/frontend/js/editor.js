// Editor IALivro — entrada principal.
// Liga upload + render + painel + persistencia REST.

import * as api from "./api.js";
import { estado, definirDocumento, selecionar, camadaPorId, aplicarPatch, removerCamada } from "./estado.js";
import { renderizarBboxes, marcarSelecionada, atualizarBbox, removerBboxDoCanvas } from "./camadas/comum.js";
import { inicializarPainel, renderizar as renderizarPainel } from "./painel.js";
import { toast } from "./toast.js";


// ============================================================
// FLUXO PRINCIPAL
// ============================================================

async function iniciarSessao(arquivo) {
  try {
    const { sessao_id, documento } = await api.uploadCamadas(arquivo);
    definirDocumento(sessao_id, documento);
    aoEntrarNoEditor();
    toast("Documento carregado.", "sucesso");
  } catch (err) {
    toast(`Erro ao carregar: ${err.message}`, "erro");
  }
}

function aoEntrarNoEditor() {
  document.getElementById("tela-upload").hidden = true;
  document.getElementById("topbar").hidden = false;
  document.getElementById("palco").hidden = false;
  document.getElementById("painel").hidden = false;

  configurarCanvas();
  renderizarBboxes(estado.documento, onSelecionar);
  renderizarPainel(null);
  atualizarCorLivro();
}

function configurarCanvas() {
  const { largura, altura } = estado.documento.dimensoes;
  const svg = document.getElementById("canvas");
  svg.setAttribute("viewBox", `0 0 ${largura} ${altura}`);

  const img = document.getElementById("img-fundo");
  img.setAttribute("width", largura);
  img.setAttribute("height", altura);
  // Sem backend de assets ainda — usa o fundo_limpo do mockup como placeholder.
  img.setAttribute("href", "/static/fundo_demo.png");
}

function onSelecionar(cid) {
  selecionar(cid);
  marcarSelecionada(cid);
  renderizarPainel(camadaPorId(cid));
}

async function onMudancaPainel(cid, patch) {
  // 1. Otimista local
  const camada = aplicarPatch(cid, patch);
  if (!camada) return;
  if (patch.bbox) atualizarBbox(camada);

  // 2. Persiste no backend
  try {
    await api.atualizarCamada(estado.sessaoId, cid, patch);
  } catch (err) {
    toast(`Erro ao salvar: ${err.message}`, "erro");
  }
}

async function onApagar(cid, modo) {
  if (modo !== "simples") {
    toast(`Modo ${modo} ainda em construção (Etapa D).`, "aviso");
    return;
  }
  try {
    await api.apagarCamada(estado.sessaoId, cid, modo);
    removerCamada(cid);
    removerBboxDoCanvas(cid);
    selecionar(null);
    renderizarPainel(null);
    toast("Camada apagada (fundo limpo revelado).", "sucesso");
  } catch (err) {
    toast(`Erro ao apagar: ${err.message}`, "erro");
  }
}

// ============================================================
// UI HELPERS
// ============================================================

function atualizarCorLivro() {
  const sel = document.getElementById("sel-livro");
  const cor = sel.options[sel.selectedIndex].dataset.cor;
  document.documentElement.style.setProperty("--livro-cor", cor);
  document.getElementById("livro-cor").style.background = cor;
}

// ============================================================
// EVENTOS GLOBAIS
// ============================================================

document.getElementById("input-arquivo").addEventListener("change", (e) => {
  const arquivo = e.target.files[0];
  if (arquivo) iniciarSessao(arquivo);
});

document.getElementById("btn-toggle-bbox").addEventListener("click", () => {
  estado.bboxVisivel = !estado.bboxVisivel;
  document.getElementById("grupo-bbox").classList.toggle("escondido", !estado.bboxVisivel);
});

document.getElementById("painel-fechar").addEventListener("click", () => {
  selecionar(null);
  document.querySelectorAll(".bbox").forEach((el) => el.classList.remove("selecionada"));
  renderizarPainel(null);
});

document.getElementById("canvas").addEventListener("click", (e) => {
  if (e.target.id === "img-fundo" || e.target.id === "canvas") {
    selecionar(null);
    document.querySelectorAll(".bbox").forEach((el) => el.classList.remove("selecionada"));
    renderizarPainel(null);
  }
});

document.getElementById("sel-livro").addEventListener("change", () => {
  atualizarCorLivro();
});

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
  if (e.key === "Escape") {
    selecionar(null);
    document.querySelectorAll(".bbox").forEach((el) => el.classList.remove("selecionada"));
    renderizarPainel(null);
  } else if (e.key.toLowerCase() === "z" && !e.ctrlKey && !e.metaKey) {
    estado.bboxVisivel = !estado.bboxVisivel;
    document.getElementById("grupo-bbox").classList.toggle("escondido", !estado.bboxVisivel);
  }
});

inicializarPainel(onMudancaPainel, onApagar);
