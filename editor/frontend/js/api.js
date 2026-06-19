// Wrapper REST do backend FastAPI.

const BASE = "/api";

export async function uploadCamadas(arquivo, fundo = null) {
  const form = new FormData();
  form.append("arquivo", arquivo);
  if (fundo) form.append("fundo", fundo);
  const resp = await fetch(`${BASE}/sessao/upload`, { method: "POST", body: form });
  if (!resp.ok) throw new Error(await mensagemErro(resp));
  return resp.json();
}

export async function exportar(sid, formato = "png") {
  const resp = await fetch(`${BASE}/sessao/${sid}/exportar?formato=${formato}`, {
    method: "POST",
  });
  if (!resp.ok) throw new Error(await mensagemErro(resp));
  const blob = await resp.blob();
  const nome = (resp.headers.get("Content-Disposition") || "").match(/filename="([^"]+)"/)?.[1]
    || `documento_editado.${formato}`;
  return { blob, nome };
}

export async function obterSessao(sid) {
  const resp = await fetch(`${BASE}/sessao/${sid}`);
  if (!resp.ok) throw new Error(await mensagemErro(resp));
  return resp.json();
}

export async function atualizarCamada(sid, cid, patch) {
  const resp = await fetch(`${BASE}/sessao/${sid}/camada/${cid}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(patch),
  });
  if (!resp.ok) throw new Error(await mensagemErro(resp));
  return resp.json();
}

export async function apagarCamada(sid, cid, modo = "simples") {
  const resp = await fetch(`${BASE}/sessao/${sid}/camada/${cid}?modo=${modo}`, {
    method: "DELETE",
  });
  if (!resp.ok) throw new Error(await mensagemErro(resp));
  return resp.json();
}

async function mensagemErro(resp) {
  try {
    const dados = await resp.json();
    return dados.detail || resp.statusText;
  } catch {
    return resp.statusText;
  }
}
