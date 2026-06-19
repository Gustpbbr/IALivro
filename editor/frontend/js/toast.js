// Notificacoes toast.

export function toast(mensagem, tipo = "info") {
  const cont = document.getElementById("toasts");
  if (!cont) return;
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
