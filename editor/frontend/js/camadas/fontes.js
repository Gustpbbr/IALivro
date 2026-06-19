// Catalogo de fontes oferecidas pelo editor.
// Reflete ETAPA_C_DESIGN.md §4.

export const CATALOGO_FONTES = {
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

export function todasFontes() {
  return Object.values(CATALOGO_FONTES).flat();
}

export function fontePorId(id) {
  return todasFontes().find((f) => f.id === id);
}

export function fontesDaClasse(classe) {
  return CATALOGO_FONTES[classe] || CATALOGO_FONTES.serif;
}

export function rotuloClasse(classe) {
  return classe === "sans_serif" ? "Sans"
    : classe.charAt(0).toUpperCase() + classe.slice(1);
}
