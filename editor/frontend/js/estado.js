// Store de estado do editor (em memoria).

export const estado = {
  sessaoId: null,
  documento: null,       // Documento (esquema v1)
  selecionadaId: null,
  bboxVisivel: true,
  historico: [],         // pilha pra undo (versoes do documento)
  livroAtual: 1,
};

export function definirDocumento(sid, documento) {
  estado.sessaoId = sid;
  estado.documento = documento;
  estado.historico = [];
}

export function camadaPorId(cid) {
  return estado.documento?.camadas.find((c) => c.id === cid) || null;
}

export function selecionar(cid) {
  estado.selecionadaId = cid;
}

export function aplicarPatch(cid, patch) {
  const camada = camadaPorId(cid);
  if (!camada) return null;
  if (patch.estilo) {
    camada.estilo = { ...(camada.estilo || {}), ...patch.estilo };
  }
  for (const [k, v] of Object.entries(patch)) {
    if (k === "estilo") continue;
    if (v !== undefined && v !== null) camada[k] = v;
  }
  return camada;
}

export function removerCamada(cid) {
  if (!estado.documento) return false;
  const antes = estado.documento.camadas.length;
  estado.documento.camadas = estado.documento.camadas.filter((c) => c.id !== cid);
  return estado.documento.camadas.length < antes;
}
