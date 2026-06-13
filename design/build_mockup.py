"""Gera mockups (PNG) da interface mobile-first do Orquestrador, a partir de SVG.
Não é o app — é a maquete visual para o autor aprovar a UX antes da Etapa 4.
python design/build_mockup.py
"""
import cairosvg
from pathlib import Path

CREAM="#F5F1E8"; NAVY="#1E2F4D"; GOLD="#C9972B"; INK="#2A2A2A"
MUTED="#8A8270"; CARD="#FFFFFF"; LINE="#E3DCCB"; NAVY2="#B9C2D0"; GREEN="#4F7942"
W=430
SERIF="Georgia, 'Times New Roman', serif"; SANS="Helvetica, Arial, sans-serif"

def rrect(x,y,w,h,r,fill,stroke="none",sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def txt(x,y,s,size=14,fill=INK,font=SANS,anchor="start",weight="normal"):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'

def header(sub):
    return (rrect(0,0,W,92,0,NAVY)
        + f'<circle cx="32" cy="44" r="15" fill="none" stroke="{GOLD}" stroke-width="2"/>'
        + f'<path d="M32 34 L40 52 L24 52 Z" fill="{GOLD}"/>'
        + txt(58,40,"Orquestrador Visual",19,"#FFFFFF",SERIF,weight="bold")
        + txt(58,63,sub,12,NAVY2,SANS))

def screen1():
    e=[rrect(0,0,W,900,0,CREAM), header("IALivro · estúdio de ilustração")]
    # toggle de modo
    e+=[rrect(16,112,197,40,20,NAVY), txt(114,138,"Trecho do capítulo",13,"#FFFFFF",SANS,"middle",weight="bold"),
        rrect(217,112,197,40,20,CARD,LINE,1.5), txt(315,138,"Pedido dirigido",13,MUTED,SANS,"middle")]
    # campo de texto
    e+=[rrect(16,168,398,118,14,CARD,LINE,1.5),
        txt(32,198,"Cole o trecho do capítulo…",13.5,MUTED,SANS),
        txt(32,220,"“João sobe ao Templo e encontra o",12.5,"#B7AE99",SANS),
        txt(32,238,"Leão guardião da Constituição…”",12.5,"#B7AE99",SANS)]
    # personagens
    e+=[txt(18,312,"PERSONAGENS EM CENA",11,MUTED,SANS,weight="bold")]
    def chip(x,label,w):
        return rrect(x,324,w,32,16,"#EFE7D4",LINE,1)+txt(x+16,345,label,12.5,INK,SANS)
    e+=[chip(16,"João   x",78), chip(102,"Leônidas   x",104),
        rrect(214,324,104,32,16,"none",GOLD,1.5)+txt(266,345,"+ adicionar",12,GOLD,SANS,"middle")]
    # enquadramento
    e+=[txt(18,392,"ENQUADRAMENTO",11,MUTED,SANS,weight="bold")]
    frames=[("Tela cheia","10:16",30,52,True),("Meia pág.","16:10",52,32,False),
            ("Bloco","1:1",42,42,False),("Vinheta","3:1",58,20,False)]
    x=16
    for name,ratio,tw,th,active in frames:
        cardc = "#FBF7EE" if not active else "#FFF"
        bord = GOLD if active else LINE
        e+=[rrect(x,406,93,96,12,cardc,bord,2 if active else 1.2)]
        e+=[rrect(x+46-tw//2,420,tw,th,3,"#D8CDB3","none")]
        e+=[txt(x+46,476,name,11.5,INK,SANS,"middle",weight="bold" if active else "normal")]
        e+=[txt(x+46,492,ratio,10,MUTED,SANS,"middle")]
        x+=99
    # peso do estilo + variações
    e+=[txt(18,540,"PESO DO ESTILO",11,MUTED,SANS,weight="bold"),
        rrect(16,552,260,6,3,LINE), rrect(16,552,180,6,3,GOLD),
        f'<circle cx="196" cy="555" r="10" fill="{GOLD}"/>',
        txt(300,540,"VARIAÇÕES",11,MUTED,SANS,weight="bold"),
        rrect(300,548,114,34,17,CARD,LINE,1.5),
        txt(316,570,"–",16,MUTED,SANS), txt(357,570,"2",15,INK,SANS,"middle",weight="bold"), txt(398,570,"+",16,GOLD,SANS,"middle")]
    # botão gerar
    e+=[rrect(16,612,398,54,14,GOLD), txt(215,645,"Gerar  ·  2 variações",17,"#FFFFFF",SANS,"middle",weight="bold")]
    e+=[txt(215,690,"≈ US$ 0,05 nesta geração",11.5,MUTED,SANS,"middle")]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="720" viewBox="0 0 {W} 720">'+''.join(e)+'</svg>'

def screen2():
    e=[rrect(0,0,W,900,0,CREAM), header("Resultado · escolha a melhor")]
    e+=[txt(16,124,"‹  voltar",13,MUTED,SANS),
        txt(16,150,"Cap. 6 — João e Leônidas no plenário",14.5,INK,SERIF,weight="bold")]
    # 2 variações
    for i,(x,sel) in enumerate([(16,True),(223,False)]):
        e+=[rrect(x,166,191,250,12,"#D8CDB3",GOLD if sel else LINE, 3 if sel else 1.2)]
        # silhueta de cena placeholder
        e+=[f'<path d="M{x+40} 360 L{x+95} 250 L{x+150} 360 Z" fill="#C2B696"/>',
            f'<rect x="{x+74}" y="300" width="42" height="60" fill="#A99B7C"/>',
            f'<circle cx="{x+150}" cy="240" r="18" fill="#E9C77A"/>']
        e+=[txt(x+95,400,f"Variação {i+1}",12,"#5C5340",SANS,"middle")]
        if sel: e+=[f'<circle cx="{x+170}" cy="186" r="13" fill="{GREEN}"/>',
            f'<path d="M{x+164} 186 l4 5 l8 -10" stroke="#FFF" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>']
    # ações
    e+=[rrect(16,432,191,48,12,GOLD)+txt(111,462,"Aprovar",15,"#FFF",SANS,"middle",weight="bold"),
        rrect(223,432,191,48,12,"none",NAVY,1.5)+txt(318,462,"Corrigir",15,NAVY,SANS,"middle",weight="bold")]
    # corrigir (inpainting) hint
    e+=[rrect(16,496,398,44,12,CARD,LINE,1.2),
        txt(32,523,"Descreva a correção  (ex.: a gravata era bordô)",12.5,MUTED,SANS)]
    # ajustes finos
    e+=[txt(18,572,"AJUSTES FINOS (sem re-gerar)",11,MUTED,SANS,weight="bold")]
    for j,(lab) in enumerate(["Brilho","Saturação","Temperatura"]):
        y=590+j*30
        e+=[txt(18,y+9,lab,12,INK,SANS), rrect(150,y+2,200,6,3,LINE), rrect(150,y+2,90+j*30,6,3,NAVY),
            f'<circle cx="{150+90+j*30}" cy="{y+5}" r="8" fill="{NAVY}"/>']
    # feedback + exportar
    e+=[rrect(16,690,150,40,20,"none",LINE,1.2)+txt(91,715,"Gostei   ·   Não",13,INK,SANS,"middle"),
        rrect(294,690,120,40,20,NAVY)+txt(354,715,"Exportar 2×",13,"#FFF",SANS,"middle",weight="bold")]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="760" viewBox="0 0 {W} 760">'+''.join(e)+'</svg>'

Path("design").mkdir(exist_ok=True)
for nome,svg in [("mockup_1_geracao",screen1()),("mockup_2_resultado",screen2())]:
    (Path("design")/f"{nome}.svg").write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f"design/{nome}.png",output_width=W*2,scale=2)
    print(f"OK: design/{nome}.png")
