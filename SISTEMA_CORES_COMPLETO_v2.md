# SISTEMA DE CORES COMPLETO — v2
## Paleta de marca dos 11 livros · cores de apoio, texto e pop-ups · escalas tonais
### Atual e canônico — maio/2026

> **Fonte dos hex:** `05_UNIVERSO_MANUAL_ESTILO_EDITORIAL.md` (§4, §12-13) + `04_GUIA_NARRATIVO_11_LIVROS_v2.md` (§2.4, pop-ups). **RGB derivado** dos hex (conversão exata). **CMYK/Pantone:** pendência de pré-impressão (ver §5).
> Regra: por livro, a única variável é a cor (principal + secundária + escala tonal). O **dourado de apoio** é transversal aos 11 livros.

---

# 1. PALETA DE MARCA — 11 LIVROS

| # | Livro | Principal (hex) | Principal (RGB) | Secundária (hex) | Secundária (RGB) |
|---|---|---|---|---|---|
| 1 | **Constitucional** | `#B8860B` | 184, 134, 11 | `#F5EFD6` | 245, 239, 214 |
| 2 | **Administrativo** | `#1B305B` | 27, 48, 91 | `#D6DFEA` | 214, 223, 234 |
| 3 | **AFO** | `#2A6199` | 42, 97, 153 | `#D6E3F1` | 214, 227, 241 |
| 4 | **Civil** | `#284703` | 40, 71, 3 | `#EDE8D0` | 237, 232, 208 |
| 5 | **Proc. Civil** | `#88B257` | 136, 178, 87 | `#E6F2D8` | 230, 242, 216 |
| 6 | **Penal** | `#6B1100` | 107, 17, 0 | `#3D3232` | 61, 50, 50 |
| 7 | **Proc. Penal** | `#FF1F1F` | 255, 31, 31 | `#5C4A4A` | 92, 74, 74 |
| 8 | **Trabalho** | `#E85D04` | 232, 93, 4 | `#E8D5B5` | 232, 213, 181 |
| 9 | **Adm. Geral** | `#3891D6` | 56, 145, 214 | `#E8EFF5` | 232, 239, 245 |
| 10 | **Ética** | `#4B2FA8` | 75, 47, 168 | `#E8E0F0` | 232, 224, 240 |
| 11 | **Dir. Humanos** | `#FA55A4` | 250, 85, 164 | `#FFF0F5` | 255, 240, 245 |

---

# 2. CORES DE APOIO E TEXTO (transversais)

| Uso | Nome | Hex | RGB |
|---|---|---|---|
| Ornamentos, selos, brasões, filetes | **Dourado de apoio** | `#C9972B` | 201, 151, 43 |
| Corpo de texto principal | Preto suave | `#1A1A1A` | 26, 26, 26 |
| Legendas, notas, texto secundário | Cinza-escuro | `#4A4A4A` | 74, 74, 74 |
| Texto sobre fundo escuro (badges, cabeçalho de tabela) | Branco | `#FFFFFF` | 255, 255, 255 |
| Cor identitária do Leônidas (dialoga com o Livro 1) | Ouro Leônidas | `#DAA520` | 218, 165, 32 |

---

# 3. QUARTETO POP-UP (cartoon — quebra a 4ª parede)

| Personagem | Disciplina | Fundo (hex/RGB) | Borda (hex/RGB) | Texto (hex/RGB) |
|---|---|---|---|---|
| 🦗 **Veríssimo** | Português | `#E8F5E9` · 232,245,233 | `#4CAF50` · 76,175,80 | `#2E7D32` · 46,125,50 |
| 🐞 **Lúcia** | Raciocínio Lógico | `#FFEBEE` · 255,235,238 | `#F44336` · 244,67,54 | `#C62828` · 198,40,40 |
| 🔥 **Lúmen** | Ética | `#FFF8E1` · 255,248,225 | `#FFC107` · 255,193,7 | `#F57F17` · 245,127,23 |
| 🕷️ **Nexus** | Informática | `#E3F2FD` · 227,242,253 | `#2196F3` · 33,150,243 | `#1565C0` · 21,101,192 |

---

# 4. ESCALAS TONAIS (por livro)

O Manual de Estilo (§12) define a escala tonal da **cor principal** em **80% / 60% / 40% / 20%** para usos específicos:

| Nível | Uso |
|---|---|
| **80%** | subtítulos (H3), ícones secundários |
| **60%** | bordas de boxes, separadores |
| **40%** | fundo de cabeçalho de tabela (alternativa clara) |
| **20%** | fundo de boxes, linhas alternadas, fundos de destaque |

> ⚙️ **Método de geração (a fixar):** as porcentagens são **tints** (mistura da cor principal com branco). Fórmula proposta (tint linear): `canal_resultante = principal + (255 − principal) × (1 − fração)`, onde fração ∈ {0.8, 0.6, 0.4, 0.2}. Assim que você confirmar a fórmula, eu **gero os hex/RGB exatos** das 44 variações (11 livros × 4 níveis).

---

# 5. CMYK / PANTONE — pendência de pré-impressão ⚠️

**Ainda não definidos.** Observações técnicas:
- **RGB → CMYK não é determinístico** sem um **perfil de cor** (depende do papel/impressora — ex.: ISO Coated v2, Fogra). Precisa ser gerado na pré-impressão ou fornecido pela gráfica.
- **Pantone** exige **correspondência manual** (não há conversão automática fiel).
- **Recomendação:** definir CMYK/Pantone só na etapa de fechamento de arte, com a gráfica. Até lá, **hex + RGB** atendem todo o fluxo digital.

---

# 6. PALETA DE CENÁRIO (direção de arte) — referência

Cores de **ambiente/materiais** (não de marca) estão em `GUIA_DIRECAO_ARTE_CENARIOS_CENAS.md` §6 — ex.: Verde República `#1F3D2E`, Ouro Antigo `#B08D3A`, Mármore/Pedra Clara `#E6E2D8`, Bronze `#906A3A`.

---

> **Versão:** 2.0 (atual) | **Data:** maio/2026 | hex+RGB completos; CMYK/Pantone pendentes (§5); escalas tonais a gerar após confirmação da fórmula (§4).
