// Wrapper REST do backend FastAPI.

const BASE = "/api";

export async function uploadCamadas(arquivo) {
  const form = new FormData();
  form.append("arquivo", arquivo);
  const resp = await fetch(`${BASE}/sessao/upload`, { method: "POST", body: form });
  if (!resp.ok) throw new Error(await mensagemErro(resp));
  return resp.json();
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
