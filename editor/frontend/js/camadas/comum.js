// Renderizacao SVG de camadas no canvas + helpers de painel.

const SVG_NS = "http://www.w3.org/2000/svg";

const ORDEM_RENDER = ["cena", "caixa", "linha_divisoria", "icone", "texto"];

export function renderizarBboxes(documento, onSelect) {
  const grupo = document.getElementById("grupo-bbox");
  grupo.innerHTML = "";

  const ordenadas = [...documento.camadas].sort(
    (a, b) => ORDEM_RENDER.indexOf(a.tipo) - ORDEM_RENDER.indexOf(b.tipo)
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
      onSelect(c.id);
    });
    grupo.appendChild(rect);
  }
}

export function marcarSelecionada(cid) {
  document.querySelectorAll(".bbox").forEach((el) => {
    el.classList.toggle("selecionada", el.dataset.id === cid);
  });
}

export function atualizarBbox(camada) {
  const rect = document.querySelector(`.bbox[data-id="${camada.id}"]`);
  if (!rect) return;
  rect.setAttribute("x", camada.bbox.x);
  rect.setAttribute("y", camada.bbox.y);
  rect.setAttribute("width", camada.bbox.w);
  rect.setAttribute("height", camada.bbox.h);
}

export function removerBboxDoCanvas(cid) {
  const rect = document.querySelector(`.bbox[data-id="${cid}"]`);
  if (rect) rect.remove();
}
