"""Renderizacao do documento (camadas.json + fundo) em PNG/PDF.

Sub-etapa C9 do ETAPA_C_ARQUITETURA.md. Backend renderiza pra garantir
qualidade e fontes identicas independente do dispositivo do autor.
"""

import io
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw

from modelos import Camada, Documento
from servicos import fontes


Formato = Literal["png", "pdf"]


def renderizar(documento: Documento, fundo: Image.Image | None = None) -> Image.Image:
    """Compoe imagem final: fundo + camadas em ordem de empilhamento."""
    largura, altura = documento.dimensoes.largura, documento.dimensoes.altura

    if fundo is None:
        canvas = Image.new("RGBA", (largura, altura), "white")
    else:
        canvas = fundo.convert("RGBA").resize((largura, altura), Image.LANCZOS)

    # Ordem de render (mais ao fundo primeiro):
    # cena -> caixa -> linha_divisoria -> icone -> texto
    ordem = ["cena", "caixa", "linha_divisoria", "icone", "texto"]
    ordenadas = sorted(
        documento.camadas, key=lambda c: ordem.index(c.tipo) if c.tipo in ordem else 99
    )

    for camada in ordenadas:
        if camada.tipo == "cena":
            continue  # ja esta no fundo
        elif camada.tipo == "caixa":
            _renderizar_caixa(canvas, camada)
        elif camada.tipo == "linha_divisoria":
            _renderizar_linha(canvas, camada)
        elif camada.tipo == "icone":
            _renderizar_icone(canvas, camada)
        elif camada.tipo == "texto":
            _renderizar_texto(canvas, camada)

    return canvas.convert("RGB")


def exportar_bytes(canvas: Image.Image, formato: Formato) -> bytes:
    buf = io.BytesIO()
    if formato == "png":
        canvas.save(buf, format="PNG", optimize=True)
    elif formato == "pdf":
        canvas.save(buf, format="PDF", resolution=150.0)
    else:
        raise ValueError(f"Formato nao suportado: {formato}")
    return buf.getvalue()


# ============================================================
# RENDER POR TIPO
# ============================================================


def _renderizar_caixa(canvas: Image.Image, camada: Camada) -> None:
    bbox = camada.bbox
    x1, y1 = bbox.x, bbox.y
    x2, y2 = x1 + bbox.w, y1 + bbox.h

    cor_fundo = _hex_para_rgba(camada.cor_fundo) if camada.cor_fundo else None
    cor_borda = _hex_para_rgba(camada.cor_borda) if camada.cor_borda else None
    espessura = camada.espessura_borda or 0
    raio = camada.raio_canto or 0

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if raio > 0:
        draw.rounded_rectangle(
            [x1, y1, x2, y2],
            radius=raio,
            fill=cor_fundo,
            outline=cor_borda,
            width=espessura,
        )
    else:
        draw.rectangle(
            [x1, y1, x2, y2],
            fill=cor_fundo,
            outline=cor_borda,
            width=espessura,
        )

    canvas.alpha_composite(overlay)


def _renderizar_linha(canvas: Image.Image, camada: Camada) -> None:
    bbox = camada.bbox
    cor = _hex_para_rgba(camada.cor or "#888888")
    espessura = camada.espessura or 1

    draw = ImageDraw.Draw(canvas)
    # Linha horizontal se largura > altura, vertical caso contrario
    if bbox.w >= bbox.h:
        y = bbox.y + bbox.h // 2
        draw.line([(bbox.x, y), (bbox.x + bbox.w, y)], fill=cor, width=espessura)
    else:
        x = bbox.x + bbox.w // 2
        draw.line([(x, bbox.y), (x, bbox.y + bbox.h)], fill=cor, width=espessura)


def _renderizar_icone(canvas: Image.Image, camada: Camada) -> None:
    if not camada.arquivo_recorte:
        return
    arquivo = Path(camada.arquivo_recorte)
    if not arquivo.exists():
        return
    icone = Image.open(arquivo).convert("RGBA")
    icone = icone.resize((camada.bbox.w, camada.bbox.h), Image.LANCZOS)
    canvas.alpha_composite(icone, (camada.bbox.x, camada.bbox.y))


def _renderizar_texto(canvas: Image.Image, camada: Camada) -> None:
    estilo = camada.estilo
    if not estilo or not camada.conteudo:
        return

    fonte = fontes.carregar(
        estilo.fonte_id or "inter", estilo.tamanho_px or 16, estilo.peso or "normal"
    )
    cor = _hex_para_rgba(estilo.cor or "#000000")

    draw = ImageDraw.Draw(canvas)

    linhas = camada.conteudo.split("\n")
    y = camada.bbox.y
    altura_linha = estilo.tamanho_px or 16
    for linha in linhas:
        x = _alinhar_x(draw, linha, fonte, camada.bbox, estilo.alinhamento or "left")
        draw.text((x, y), linha, fill=cor, font=fonte)
        y += int(altura_linha * 1.2)


def _alinhar_x(draw, linha, fonte, bbox, alinhamento) -> int:
    if alinhamento == "left":
        return bbox.x
    try:
        l, _, r, _ = draw.textbbox((0, 0), linha, font=fonte)
        largura_texto = r - l
    except Exception:
        return bbox.x
    if alinhamento == "center":
        return bbox.x + (bbox.w - largura_texto) // 2
    if alinhamento == "right":
        return bbox.x + bbox.w - largura_texto
    return bbox.x


def _hex_para_rgba(hex_cor: str, alpha: int = 255) -> tuple[int, int, int, int]:
    h = hex_cor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return (0, 0, 0, alpha)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)
