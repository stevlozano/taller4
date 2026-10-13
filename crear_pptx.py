#!/usr/bin/env python3
"""Crea el PPT minimalista (fondo negro, texto blanco) del taller de arquitectura AWS."""
import os

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
from pptx.util import Emu, Inches, Pt

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
OUT = os.path.join(BASE, "Taller_Arquitectura_AWS_Segura_Escalable.pptx")

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
GRAY = RGBColor(0xB3, 0xB3, 0xB3)
DGRAY = RGBColor(0x8A, 0x8A, 0x8A)
PANEL = RGBColor(0x10, 0x10, 0x10)
LINE = RGBColor(0x66, 0x66, 0x66)
SOFT = RGBColor(0x33, 0x33, 0x33)
FONT = "Arial"

SW, SH = 13.333, 7.5
ML = 0.7
CW = SW - 2 * ML

FOOT = "TALLER PRÁCTICO · ARQUITECTURA AWS SEGURA, DISPONIBLE Y ESCALABLE"


# ----------------------------------------------------------------- utilidades
def new_slide(prs, dark=True):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fill = s.background.fill
    fill.solid()
    fill.fore_color.rgb = BLACK if dark else WHITE
    return s


def txt(slide, x, y, w, h, text, size=16, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0, italic=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lines = text.split("\n") if isinstance(text, str) else list(text)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
        r.font.name = FONT
    return box


def _pPr(p):
    return p._p.get_or_add_pPr()


def bullets(slide, x, y, w, h, items, size=16, color=WHITE, gap=8,
            marker="•   ", spacing=1.05, bold_first=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = spacing
        p.space_after = Pt(gap)
        pPr = _pPr(p)
        pPr.set("marL", str(int(Inches(0.26))))
        pPr.set("indent", str(int(-Inches(0.26))))
        r = p.add_run()
        r.text = marker + item
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.name = FONT
        r.font.bold = bold_first and i == 0
    return box


def numbered(slide, x, y, w, h, items, size=16, color=WHITE, gap=8,
             num_color=DGRAY, spacing=1.05, start=1):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = spacing
        p.space_after = Pt(gap)
        pPr = _pPr(p)
        pPr.set("marL", str(int(Inches(0.42))))
        pPr.set("indent", str(int(-Inches(0.42))))
        r1 = p.add_run()
        r1.text = "%02d   " % (i + start)
        r1.font.size = Pt(size)
        r1.font.bold = True
        r1.font.color.rgb = num_color
        r1.font.name = FONT
        r2 = p.add_run()
        r2.text = item
        r2.font.size = Pt(size)
        r2.font.color.rgb = color
        r2.font.name = FONT
    return box


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0,
         shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    sh.text_frame.word_wrap = True
    return sh


def header(slide, title, eyebrow=None, size=30, line_w=1.6):
    top = 0.5
    if eyebrow:
        txt(slide, ML, 0.42, CW, 0.3, eyebrow.upper(), size=11.5, bold=True,
            color=DGRAY)
        top = 0.78
    txt(slide, ML, top, CW, 0.9, title, size=size, bold=True, color=WHITE)
    ln = rect(slide, ML, top + 0.72, line_w, 0.04, fill=WHITE)
    ln.line.fill.background()
    return top + 0.72


def footer(slide, n, total=30):
    txt(slide, ML, 7.05, 9.5, 0.3, FOOT, size=8.5, color=DGRAY)
    txt(slide, SW - ML - 1.6, 7.05, 1.6, 0.3, "%02d / %d" % (n, total),
        size=8.5, color=DGRAY, align=PP_ALIGN.RIGHT)


def img_wh(name):
    with Image.open(os.path.join(IMG, name)) as im:
        w, h = im.size
    return w, h


def pic(slide, name, x, y, w=None, h=None, center_x=None):
    pw, ph = img_wh(name)
    ratio = ph / pw
    if w is None:
        w = h / ratio
    else:
        h = w * ratio
    if center_x is not None:
        x = center_x - w / 2
    slide.shapes.add_picture(os.path.join(IMG, name), Inches(x), Inches(y),
                             width=Inches(w))
    return x, y, w, h


def caption(slide, x, y, w, text, align=PP_ALIGN.CENTER, size=13, color=GRAY):
    txt(slide, x, y, w, 0.35, text, size=size, color=color, align=align,
        bold=True)


# ------------------------------------------------------------------- tablas
def set_cell_border(cell, color=LINE, width_pt=0.75, edges="LRTB"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    order = [t for t in ("a:lnL", "a:lnR", "a:lnT", "a:lnB")
             if t[-1] in edges]
    for tag in order:
        for old in tcPr.findall(qn(tag)):
            tcPr.remove(old)
    for i, tag in enumerate(order):
        frag = parse_xml(
            '<%s xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'w="%d" cap="flat" cmpd="sng" algn="ctr">'
            '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>'
            '<a:prstDash val="solid"/></%s>'
            % (tag, int(width_pt * 12700), str(color), tag)
        )
        tcPr.insert(i, frag)


def table(slide, data, x, y, w, col_fracs, row_h=0.42, header_h=0.44,
          font=11, header_font=11, aligns=None, header=True):
    rows, cols = len(data), len(data[0])
    total_h = header_h + (rows - 1) * row_h if header else rows * row_h
    gf = slide.shapes.add_table(rows, cols, Inches(x), Inches(y),
                                Inches(w), Inches(total_h))
    tbl = gf.table
    tbl._tbl.tblPr.set("firstRow", "0")
    tbl._tbl.tblPr.set("bandRow", "0")
    for el in tbl._tbl.tblPr.findall(qn("a:tableStyleId")):
        tbl._tbl.tblPr.remove(el)
    sid = parse_xml(
        '<a:tableStyleId xmlns:a="http://schemas.openxmlformats.org/'
        'drawingml/2006/main">{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
        '</a:tableStyleId>')
    tbl._tbl.tblPr.append(sid)

    for j, frac in enumerate(col_fracs):
        tbl.columns[j].width = Emu(int(Inches(w) * frac))
    for i in range(rows):
        tbl.rows[i].height = Inches(header_h if (header and i == 0) else row_h)

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = Inches(0.09)
            cell.margin_right = Inches(0.07)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            is_head = header and i == 0
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if is_head else PANEL
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (aligns[j] if aligns else PP_ALIGN.LEFT)
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(header_font if is_head else font)
            r.font.bold = is_head
            r.font.color.rgb = BLACK if is_head else WHITE
            r.font.name = FONT
            set_cell_border(cell, color=RGBColor(0x88, 0x88, 0x88) if is_head
                            else LINE)
    return gf


def quote(slide, x, y, w, h, text, size=17, color=WHITE, sub=None):
    rect(slide, x, y, w, h, fill=PANEL, line=SOFT, lw=1.0)
    inner = h - 0.5 - (0.4 if sub else 0)
    txt(slide, x + 0.35, y + 0.28, w - 0.7, inner, text, size=size,
        color=color, spacing=1.15)
    if sub:
        txt(slide, x + 0.35, y + h - 0.5, w - 0.7, 0.3, sub, size=12,
            color=DGRAY, bold=True)


def cards(slide, x, y, w, h, items, cols=2, num_size=22, text_size=13.5,
          gap_x=0.3, gap_y=0.3):
    rows = (len(items) + cols - 1) // cols
    cw = (w - gap_x * (cols - 1)) / cols
    ch = (h - gap_y * (rows - 1)) / rows
    for i, item in enumerate(items):
        c, r = i % cols, i // cols
        cx = x + c * (cw + gap_x)
        cy = y + r * (ch + gap_y)
        rect(slide, cx, cy, cw, ch, fill=PANEL, line=SOFT, lw=1.0)
        txt(slide, cx + 0.25, cy + 0.18, cw - 0.5, 0.35, "%02d" % (i + 1),
            size=num_size, bold=True, color=DGRAY)
        txt(slide, cx + 0.25, cy + 0.62, cw - 0.5, ch - 0.8, item,
            size=text_size, color=WHITE, spacing=1.1)


def check_list(slide, x, y, w, items, size=15, gap=9, color=WHITE):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(5))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        pPr = _pPr(p)
        pPr.set("marL", str(int(Inches(0.34))))
        pPr.set("indent", str(int(-Inches(0.34))))
        r1 = p.add_run()
        r1.text = "✓   "
        r1.font.size = Pt(size)
        r1.font.bold = True
        r1.font.color.rgb = WHITE
        r1.font.name = FONT
        r2 = p.add_run()
        r2.text = item
        r2.font.size = Pt(size)
        r2.font.color.rgb = color
        r2.font.name = FONT
    return box


# ------------------------------------------------------------------ contenidos
def build():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    n = 0

    # ------------------------------------------------------------- 1 portada
    n += 1
    s = new_slide(prs)
    pic(s, "portada.png", 0, 1.7, w=5.7, center_x=10.05)
    txt(s, ML, 1.05, 6.1, 0.35,
        "TALLER PRÁCTICO · 4 HORAS · LABORATORIO AWS", size=13, bold=True,
        color=DGRAY)
    txt(s, ML, 1.55, 6.1, 2.6,
        "Implementación de una arquitectura AWS segura, fiable y escalable",
        size=34, bold=True, color=WHITE, spacing=1.05)
    ln = rect(s, ML, 4.35, 2.2, 0.045, fill=WHITE)
    ln.line.fill.background()
    txt(s, ML, 4.65, 6.1, 0.9,
        "Modalidad práctica en laboratorio · Nivel técnico / intermedio\n"
        "Plataforma: AWS Management Console · Equipos de 3–4 estudiantes",
        size=13.5, color=GRAY, spacing=1.25)
    txt(s, ML, 5.75, 6.1, 0.4,
        "Presenta: Stev Lozano — Actividades 3 y 4", size=15, bold=True,
        color=WHITE)
    txt(s, ML, 6.25, 6.1, 1.0,
        "Integrante 1 — Actividades 1 y 2 · Integrante 2 — Actividades 3 y 4\n"
        "Integrante 3 — Actividades 5 y 6 · Integrante 4 — Actividades 7 y 8",
        size=12.5, color=DGRAY, spacing=1.3)

    # ---------------------------------------------------------- 2 contenido
    n += 1
    s = new_slide(prs)
    header(s, "Contenido", "índice del taller")
    items_l = ["Datos generales", "Situación problemática",
               "Propósito del taller", "Competencias y resultados",
               "Recursos necesarios",
               "Actividad 1 · Marco Well-Architected  (Integrante 1)",
               "Actividad 2 · Publicar servidores EC2  (Integrante 1)",
               "Actividad 3 · Fiabilidad y disponibilidad  (Integrante 2)",
               "Actividad 4 · Distribuir el tráfico ELB  (Integrante 2)"]
    items_r = ["Actividad 5 · Monitoreo con CloudWatch  (Integrante 3)",
               "Actividad 6 · AWS Trusted Advisor  (Integrante 3)",
               "Actividad 7 · Auto Scaling  (Integrante 4)",
               "Actividad 8 · Mejorar la arquitectura  (Integrante 4)",
               "Reto final del taller",
               "Producto final: diagrama, tabla e informe",
               "Evaluación mediante rúbrica",
               "Preguntas de reflexión final",
               "Evidencias y conclusión"]
    numbered(s, ML, 1.9, 5.9, 4.8, items_l, size=14.5, gap=11)
    numbered(s, ML + 6.1, 1.9, 5.9, 4.8, items_r, size=14.5, gap=11,
             start=10)

    # ----------------------------------------------------- 3 datos generales
    n += 1
    s = new_slide(prs)
    header(s, "1. Datos generales", "información del taller")
    data = [["Aspecto", "Descripción"],
            ["Título", "Implementación de una arquitectura AWS segura, "
                       "fiable y escalable"],
            ["Duración", "4 horas"],
            ["Modalidad", "Práctica en laboratorio"],
            ["Nivel", "Técnico / Intermedio"],
            ["Plataforma", "AWS Management Console"],
            ["Trabajo", "Equipos de 3–4 estudiantes"],
            ["Producto final", "Arquitectura AWS funcional y documentada"],
            ["Caso", "Plataforma web de una empresa que recibe tráfico variable"]]
    table(s, data, ML, 1.95, CW, [0.24, 0.76], row_h=0.5, header_h=0.48,
          font=13, header_font=13)

    # ------------------------------------------------ 4 situación problemática
    n += 1
    s = new_slide(prs)
    header(s, "2. Situación problemática", "punto de partida")
    txt(s, ML, 1.95, 6.0, 2.2,
        "Una empresa tiene una aplicación web que actualmente funciona en un "
        "único servidor. Durante las horas de mayor demanda, el servidor "
        "presenta lentitud y, si falla, la aplicación deja de estar "
        "disponible.",
        size=15.5, color=GRAY, spacing=1.3)
    quote(s, ML, 4.35, 6.0, 2.35,
          "“La empresa solicita al equipo diseñar una solución en AWS "
          "que permita mejorar la arquitectura actual.”",
          size=15, sub="CASO DE ESTUDIO")
    txt(s, ML + 6.5, 1.95, 5.4, 0.4, "La solución debe permitir:",
        size=15, bold=True, color=WHITE)
    bullets(s, ML + 6.5, 2.5, 5.4, 4.2, [
        "Mantener la aplicación disponible ante fallos",
        "Distribuir el tráfico entre varios servidores",
        "Monitorear los recursos en tiempo real",
        "Escalar los servidores según la demanda",
        "Detectar problemas de configuración",
        "Mejorar progresivamente la arquitectura",
        "Aplicar las buenas prácticas del AWS Well-Architected Framework",
    ], size=14.5, gap=9)

    # --------------------------------------------------------- 5 propósito
    n += 1
    s = new_slide(prs)
    header(s, "3. Propósito del taller", "objetivo de aprendizaje")
    quote(s, ML, 2.25, CW, 2.0,
          "Al finalizar el taller, el estudiante será capaz de diseñar, "
          "implementar, monitorear y mejorar una arquitectura básica en AWS, "
          "aplicando principios de fiabilidad, alta disponibilidad, "
          "escalabilidad, balanceo de carga, monitoreo y optimización.",
          size=18, sub="PROPÓSITO")
    etiquetas = ["Diseñar", "Implementar", "Monitorear", "Mejorar"]
    bw = (CW - 3 * 0.3) / 4
    for i, e in enumerate(etiquetas):
        x = ML + i * (bw + 0.3)
        rect(s, x, 4.75, bw, 1.0, fill=PANEL, line=SOFT, lw=1.0)
        txt(s, x, 5.05, bw, 0.4, e, size=17, bold=True, color=WHITE,
            align=PP_ALIGN.CENTER)
    txt(s, ML, 6.15, CW, 0.4,
        "Arquitectura segura · fiable · escalable · optimizada", size=14,
        color=DGRAY, align=PP_ALIGN.CENTER, bold=True)

    # --------------------------------------------------- 6 competencias
    n += 1
    s = new_slide(prs)
    header(s, "4. Competencias y resultados de aprendizaje",
           "el estudiante podrá")
    comp_l = [
        "Describir los principios del AWS Well-Architected Framework.",
        "Implementar mecanismos básicos de fiabilidad y alta disponibilidad.",
        "Identificar recomendaciones mediante AWS Trusted Advisor.",
        "Distribuir tráfico mediante Elastic Load Balancing.",
    ]
    comp_r = [
        "Monitorear recursos utilizando Amazon CloudWatch.",
        "Seleccionar y publicar servidores de acuerdo con las cargas de "
        "trabajo.",
        "Implementar mecanismos de escalado automático.",
        "Analizar una arquitectura e identificar oportunidades de mejora.",
    ]
    numbered(s, ML, 2.0, 5.9, 4.4, comp_l, size=15.5, gap=18)
    numbered(s, ML + 6.1, 2.0, 5.9, 4.4, comp_r, size=15.5, gap=18,
             start=5)

    # --------------------------------------------------------- 7 recursos
    n += 1
    s = new_slide(prs)
    header(s, "5. Recursos necesarios", "cuenta y herramientas AWS")
    bullets(s, ML, 2.0, 5.6, 4.4, [
        "AWS Management Console",
        "Amazon EC2",
        "Elastic Load Balancing",
        "Auto Scaling",
        "Amazon CloudWatch",
        "AWS Trusted Advisor",
        "Amazon VPC",
        "Security Groups",
        "IAM",
    ], size=16, gap=11)
    quote(s, ML + 6.3, 2.0, 5.6, 2.4,
          "Utilizar recursos incluidos en la capa gratuita o los de menor "
          "costo disponibles en la cuenta del laboratorio.",
          size=15, sub="IMPORTANTE · CAPA GRATUITA")
    quote(s, ML + 6.3, 4.65, 5.6, 1.9,
          "Al finalizar, los estudiantes deben eliminar los recursos creados "
          "para evitar cargos.",
          size=15, sub="AL FINALIZAR EL LABORATORIO")

    # ------------------------------------------------- 8 ACTIVIDAD 1 pilares
    n += 1
    s = new_slide(prs)
    header(s, "Marco de Buena Arquitectura de AWS",
           "actividad 1 · integrante 1", size=28)
    txt(s, ML, 1.85, CW, 0.5,
        "Objetivo: reconocer los principios que permiten construir una "
        "arquitectura AWS segura, eficiente, fiable y optimizada.",
        size=14.5, color=GRAY)
    x, y, w, h = pic(s, "pilares.png", 0, 2.4, w=9.0, center_x=SW / 2)
    caption(s, x, y + h + 0.2, w, "Los seis pilares del AWS Well-Architected "
                                  "Framework")

    # ------------------------------------------- 9 ACTIVIDAD 1 práctica
    n += 1
    s = new_slide(prs)
    header(s, "Actividad práctica · Problema → Pilar",
           "actividad 1 · integrante 1", size=28)
    quote(s, ML, 1.9, CW, 1.15,
          "“La empresa tiene un servidor web único, no posee monitoreo, "
          "utiliza una instancia sobredimensionada y no tiene mecanismos de "
          "recuperación.”", size=15)
    txt(s, ML, 3.3, CW, 0.35,
        "Identificar: Problema → Riesgo → Pilar relacionado → Solución AWS",
        size=14.5, bold=True, color=WHITE)
    data = [["Problema", "Riesgo", "Pilar", "Solución AWS"],
            ["Servidor web único", "Indisponibilidad total", "Fiabilidad",
             "ALB + Auto Scaling"],
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "", ""]]
    table(s, data, ML, 3.8, CW, [0.26, 0.26, 0.2, 0.28], row_h=0.58,
          header_h=0.46, font=13, header_font=13)

    # ------------------------------------------------ 10 ACTIVIDAD 2 EC2
    n += 1
    s = new_slide(prs)
    header(s, "Publicar servidores según la carga de trabajo",
           "actividad 2 · integrante 1", size=27)
    txt(s, ML, 1.85, 6.6, 0.4,
        "Objetivo: crear una instancia EC2 adecuada para una aplicación web.",
        size=14, color=GRAY)
    numbered(s, ML, 2.4, 6.6, 4.4, [
        "Ingresar a Amazon EC2.",
        "Seleccionar Launch instance.",
        "Asignar un nombre: WEB-SERVER-01.",
        "Seleccionar una AMI apropiada.",
        "Seleccionar un tipo de instancia adecuado al laboratorio.",
        "Configurar la red.",
        "Crear o seleccionar un Security Group.",
        "Permitir HTTP por el puerto 80.",
        "Iniciar la instancia y obtener la IP pública.",
        "Acceder desde un navegador web.",
    ], size=14, gap=6)
    x, y, w, h = pic(s, "ec2_launch.png", 0, 2.55, w=5.5, center_x=10.15)
    caption(s, x, y + h + 0.2, w, "Configuración de la instancia")

    # -------------------------------------------- 11 ACTIVIDAD 2 producto
    n += 1
    s = new_slide(prs)
    header(s, "Producto esperado", "actividad 2 · integrante 1", size=28)
    x, y, w, h = pic(s, "pag_web.png", ML, 2.35, w=6.4)
    caption(s, x, y + h + 0.2, w, "Página de prueba servida por WEB-SERVER-01")
    txt(s, ML + 7.0, 2.1, 5.0, 0.4, "¿Qué debe comprobarse?", size=16,
        bold=True, color=WHITE)
    bullets(s, ML + 7.0, 2.7, 5.0, 3.4, [
        "Una página web sencilla responde por HTTP.",
        "La IP pública es accesible desde el navegador.",
        "El Security Group permite el puerto 80.",
        "Capturar la pantalla como evidencia del taller.",
    ], size=14.5, gap=11)
    quote(s, ML + 7.0, 5.3, 5.0, 1.3,
          "“Servidor Web AWS – Grupo 01”", size=16,
          sub="TÍTULO DE EJEMPLO")

    # --------------------------------------------- 12 ACTIVIDAD 3 fiabilidad
    n += 1
    s = new_slide(prs)
    header(s, "Asegurar la fiabilidad y alta disponibilidad",
           "actividad 3 · integrante 2", size=27)
    txt(s, ML, 1.8, CW, 0.35,
        "Objetivo: evitar que la aplicación dependa de un único servidor.",
        size=14, color=GRAY)
    ix, iy, iw, ih = pic(s, "diag_inicial.png", 0, 2.5, h=3.5,
                         center_x=3.65)
    caption(s, ix, 2.15, iw, "Arquitectura inicial")
    px, py, pw, ph = pic(s, "diag_propuesta.png", 0, 2.5, h=3.5,
                         center_x=9.6)
    caption(s, px, 2.15, pw, "Propuesta con 2 o más instancias")
    quote(s, ML, 6.15, CW, 0.75,
          "¿Qué sucede si EC2-01 deja de funcionar?  ·  Punto único de fallo "
          "→ se elimina con Load Balancer y múltiples instancias.",
          size=14.5)

    # ---------------------------------------------- 14 ACTIVIDAD 4 ... (13)
    n += 1
    s = new_slide(prs)
    header(s, "Distribuir el tráfico entre las instancias",
           "actividad 4 · integrante 2", size=27)
    txt(s, ML, 1.85, CW, 0.4,
        "Servicio: Elastic Load Balancing — Application Load Balancer   |   "
        "Objetivo: distribuir las solicitudes de los usuarios entre las "
        "instancias EC2.", size=13.5, color=GRAY)
    numbered(s, ML, 2.5, 5.9, 4.2, [
        "Crear un Target Group.",
        "Registrar las instancias EC2.",
        "Configurar el puerto HTTP.",
        "Crear un Application Load Balancer.",
        "Configurar el Listener HTTP.",
    ], size=15, gap=14)
    numbered(s, ML + 6.1, 2.5, 5.9, 4.2, [
        "Asociar el Target Group.",
        "Obtener el DNS del Load Balancer.",
        "Acceder mediante el navegador.",
        "Comprobar que la aplicación responde.",
    ], size=15, gap=14, start=6)

    # ------------------------------------------ 15 ACTIVIDAD 4 demostración
    n += 1
    s = new_slide(prs)
    header(s, "Demostración: el tráfico se distribuye",
           "actividad 4 · integrante 2", size=27)
    x, y, w, h = pic(s, "elb_demo.png", ML, 2.15, w=6.5)
    txt(s, ML + 7.1, 2.0, 4.9, 0.4, "Modificar cada servidor:", size=15,
        bold=True, color=WHITE)
    rect(s, ML + 7.1, 2.55, 4.9, 1.0, fill=PANEL, line=SOFT)
    txt(s, ML + 7.35, 2.85, 4.4, 0.4, "EC2-01  →  Servidor WEB 01 – Grupo A",
        size=14, color=WHITE, bold=True)
    rect(s, ML + 7.1, 3.75, 4.9, 1.0, fill=PANEL, line=SOFT)
    txt(s, ML + 7.35, 4.05, 4.4, 0.4, "EC2-02  →  Servidor WEB 02 – Grupo A",
        size=14, color=WHITE, bold=True)
    quote(s, ML + 7.1, 5.0, 4.9, 1.65,
          "Al realizar varias solicitudes se observa que el tráfico puede ser "
          "atendido por diferentes servidores.", size=14)

    # ---------------------------------------------- 16 ACTIVIDAD 5 CloudWatch
    n += 1
    s = new_slide(prs)
    header(s, "Monitorear recursos y aplicaciones en tiempo real",
           "actividad 5 · integrante 3", size=25)
    txt(s, ML, 1.8, CW, 0.35,
        "Servicio: Amazon CloudWatch   |   Objetivo: supervisar el "
        "comportamiento de las instancias y detectar situaciones anormales.",
        size=13.5, color=GRAY)
    x, y, w, h = pic(s, "cloudwatch.png", ML, 2.4, w=6.4)
    caption(s, x, y + h + 0.18, w, "Panel de métricas y alarma de CPU")
    txt(s, ML + 7.0, 2.3, 5.0, 0.4, "Qué deben observar:", size=16, bold=True,
        color=WHITE)
    bullets(s, ML + 7.0, 2.85, 5.0, 2.6, [
        "CPU y estado de las instancias",
        "Tráfico de red y solicitudes",
        "Estado de los destinos del Load Balancer",
        "Alarmas configuradas",
    ], size=14.5, gap=10)
    quote(s, ML + 7.0, 5.3, 5.0, 1.35,
          "Crear una alarma: si la CPU supera un porcentaje durante un "
          "periodo establecido, generar una alerta.", size=13.5,
          sub="ACTIVIDAD")

    # ------------------------------------------- 17 ACTIVIDAD 5 preguntas
    n += 1
    s = new_slide(prs)
    header(s, "Preguntas de análisis de monitoreo",
           "actividad 5 · integrante 3", size=27)
    cards(s, ML, 2.1, CW, 4.5, [
        "¿Qué recurso presenta mayor utilización?",
        "¿Qué ocurre cuando aumenta el tráfico?",
        "¿Cómo sabemos que una instancia presenta problemas?",
        "¿Qué métrica sería útil para activar el escalado?",
    ], cols=2, text_size=16)

    # ------------------------------------------ 18 ACTIVIDAD 6 Trusted Advisor
    n += 1
    s = new_slide(prs)
    header(s, "Configurar AWS Trusted Advisor",
           "actividad 6 · integrante 3", size=28)
    txt(s, ML, 1.85, CW, 0.35,
        "Objetivo: utilizar Trusted Advisor para identificar oportunidades "
        "de mejora en la cuenta del laboratorio.", size=14, color=GRAY)
    x, y, w, h = pic(s, "trusted_advisor.png", ML, 2.5, w=6.4)
    caption(s, x, y + h + 0.2, w, "Recomendaciones por categoría")
    txt(s, ML + 7.0, 2.4, 5.0, 0.4, "Categorías a revisar:", size=16,
        bold=True, color=WHITE)
    bullets(s, ML + 7.0, 2.95, 5.0, 2.5, [
        "Seguridad",
        "Rendimiento",
        "Costos",
        "Tolerancia a fallos",
        "Límites de servicio",
    ], size=15, gap=9)
    quote(s, ML + 7.0, 5.2, 5.0, 1.5,
          "Registrar al menos 3 recomendaciones encontradas.",
          size=14.5, sub="ACTIVIDAD")

    # ------------------------------------------ 19 ACTIVIDAD 6 tabla
    n += 1
    s = new_slide(prs)
    header(s, "Registro de recomendaciones", "actividad 6 · integrante 3",
           size=28)
    data = [["Recomendación", "Categoría", "Riesgo", "Acción propuesta"],
            ["Recomendación 1", "", "", ""],
            ["Recomendación 2", "", "", ""],
            ["Recomendación 3", "", "", ""]]
    table(s, data, ML, 1.95, CW, [0.28, 0.18, 0.22, 0.32], row_h=0.72,
          header_h=0.5, font=13, header_font=13)
    quote(s, ML, 5.35, CW, 1.25,
          "¿Por qué Trusted Advisor ayuda a mejorar una arquitectura AWS?",
          size=17, sub="PREGUNTA PARA EL EQUIPO")

    # --------------------------------------------- 20 ACTIVIDAD 7 Auto Scaling
    n += 1
    s = new_slide(prs)
    header(s, "Realizar tareas de escalado", "actividad 7 · integrante 4",
           size=28)
    txt(s, ML, 1.85, CW, 0.35,
        "Objetivo: implementar Auto Scaling para adaptar automáticamente la "
        "capacidad a la demanda.", size=14, color=GRAY)
    x, y, w, h = pic(s, "autoscaling.png", 0, 2.35, h=4.35, center_x=3.3)
    txt(s, ML + 6.2, 2.35, 5.7, 0.4, "Configurar:", size=16, bold=True,
        color=WHITE)
    bullets(s, ML + 6.2, 2.9, 5.7, 2.2, [
        "Launch Template",
        "Auto Scaling Group",
        "Capacidad mínima / deseada / máxima",
        "Política de escalado",
    ], size=15, gap=10)
    rect(s, ML + 6.2, 5.15, 5.7, 1.5, fill=PANEL, line=SOFT)
    txt(s, ML + 6.5, 5.4, 5.1, 1.1,
        "Ejemplo:\nMínimo: 2 instancias   ·   Deseado: 2 instancias   ·   "
        "Máximo: 4 instancias", size=14, color=WHITE, spacing=1.25)

    # ---------------------------------------- 21 ACTIVIDAD 7 situación práctica
    n += 1
    s = new_slide(prs)
    header(s, "Situación práctica de escalado",
           "actividad 7 · integrante 4", size=28)
    x, y, w, h = pic(s, "reto.png", ML, 2.5, w=6.4)
    caption(s, x, y + h + 0.2, w, "La demanda sube y las instancias aumentan")
    quote(s, ML + 7.0, 2.15, 5.0, 2.5,
          "“La empresa tendrá una campaña promocional y se espera un "
          "aumento importante de usuarios.”", size=16, sub="PLANTEAMIENTO")
    quote(s, ML + 7.0, 4.8, 5.0, 1.95,
          "¿Cómo debería responder la infraestructura ante ese aumento "
          "de tráfico?", size=15, sub="PREGUNTA PARA EL EQUIPO")

    # ----------------------------------------------- 22 ACTIVIDAD 8 mejora
    n += 1
    s = new_slide(prs)
    header(s, "Mejorar la arquitectura", "actividad 8 · integrante 4",
           size=28)
    x, y, w, h = pic(s, "antes_despues.png", ML, 1.9, w=7.2)
    caption(s, x, y + h + 0.15, w, "Comparación: arquitectura inicial vs. "
                                   "arquitectura mejorada")
    txt(s, ML + 8.1, 1.95, 4.0, 0.7, "Reto:", size=17, bold=True,
        color=WHITE)
    txt(s, ML + 8.1, 2.4, 4.1, 1.0,
        "Cada grupo debe identificar 5 mejoras adicionales que podría "
        "implementar.", size=14, color=GRAY, spacing=1.2)
    for i in range(5):
        yy = 3.7 + i * 0.55
        txt(s, ML + 8.1, yy, 0.5, 0.35, "%02d" % (i + 1), size=13, bold=True,
            color=DGRAY)
        ln = rect(s, ML + 8.7, yy + 0.3, 3.3, 0.02, fill=SOFT)
        ln.line.fill.background()

    # ------------------------------------------------------- 23 reto final
    n += 1
    s = new_slide(prs)
    header(s, "14. Reto final del taller", "diseño de arquitectura AWS")
    quote(s, ML, 1.9, 6.2, 3.6,
          "Una empresa de comercio electrónico realizará una campaña de "
          "ventas durante un fin de semana. Se espera que el número de "
          "usuarios aumente considerablemente. La empresa no puede permitirse "
          "que la aplicación deje de funcionar y necesita conocer el "
          "comportamiento de sus servidores en tiempo real.",
          size=15, sub="ESCENARIO — CADA EQUIPO")
    txt(s, ML + 6.6, 2.0, 5.3, 0.4,
        "Diseñar una solución que incluya como mínimo:", size=14.5,
        bold=True, color=WHITE)
    check_list(s, ML + 6.6, 2.55, 5.3, [
        "EC2", "Load Balancer", "Auto Scaling", "CloudWatch",
        "Trusted Advisor", "VPC", "Security Groups", "Alta disponibilidad",
        "Monitoreo", "Estrategia de escalamiento",
    ], size=15, gap=7)

    # ----------------------------------------------- 24 producto final diagrama
    n += 1
    s = new_slide(prs)
    header(s, "15. Producto final — A. Diagrama de arquitectura",
           "entrega por equipo", size=26)
    pic(s, "arquitectura_final.png", 0, 1.85, h=5.0, center_x=3.6)
    txt(s, ML + 6.5, 2.0, 5.4, 0.4, "Cada grupo presentará:", size=16,
        bold=True, color=WHITE)
    numbered(s, ML + 6.5, 2.6, 5.4, 3.8, [
        "A. Diagrama de arquitectura completo.",
        "B. Tabla de configuración de servicios.",
        "C. Informe de mejoras con respuestas.",
        "Evidencias capturadas durante el laboratorio.",
    ], size=15, gap=22)

    # ------------------------------------------ 25 producto final tabla
    n += 1
    s = new_slide(prs)
    header(s, "15. Producto final — B. Tabla de configuración",
           "entrega por equipo", size=26)
    data = [["Servicio", "Configuración", "Propósito"],
            ["EC2", "Servidores web", "Ejecutar la aplicación"],
            ["ALB", "Distribución de tráfico", "Balanceo de carga"],
            ["Auto Scaling", "Mín / Deseado / Máx", "Escalabilidad"],
            ["CloudWatch", "Métricas y alarmas", "Monitoreo"],
            ["Trusted Advisor", "Recomendaciones", "Optimización"],
            ["VPC", "Red", "Aislamiento"],
            ["Security Group", "Reglas de tráfico", "Seguridad"]]
    table(s, data, ML, 2.0, CW, [0.26, 0.37, 0.37], row_h=0.52,
          header_h=0.5, font=13.5, header_font=13.5)

    # ---------------------------------------- 26 producto final informe
    n += 1
    s = new_slide(prs)
    header(s, "15. Producto final — C. Informe de mejoras",
           "entrega por equipo", size=26)
    preg_l = [
        "¿Cuál era el principal problema de la arquitectura inicial?",
        "¿Cómo se mejoró la disponibilidad?",
        "¿Cómo se distribuye el tráfico?",
        "¿Cómo se controla el crecimiento de la demanda?",
    ]
    preg_r = [
        "¿Cómo se monitorean los recursos?",
        "¿Qué recomendaciones encontró Trusted Advisor?",
        "¿Qué mejoras adicionales implementarían?",
        "¿Qué pilar del Well-Architected aplicaron y por qué?",
    ]
    numbered(s, ML, 2.1, 5.9, 4.3, preg_l, size=15.5, gap=22)
    numbered(s, ML + 6.1, 2.1, 5.9, 4.3, preg_r, size=15.5, gap=22,
             start=5)

    # ------------------------------------------------------------ 27 rúbrica
    n += 1
    s = new_slide(prs)
    header(s, "16. Evaluación mediante rúbrica", "criterios y niveles",
           size=28)
    data = [
        ["Criterio", "Excelente 4", "Bueno 3", "En proceso 2", "Inicio 1"],
        ["Well-Architected", "Explica y aplica los pilares",
         "Explica la mayoría", "Dificultades", "No los identifica"],
        ["EC2", "Configura correctamente", "Configura con poca ayuda",
         "Requiere apoyo", "No logra configurarlo"],
        ["Alta disponibilidad", "Implementa correctamente",
         "Implementa parcialmente", "Presenta errores", "No implementa"],
        ["Load Balancer", "Distribuye correctamente",
         "Funciona con pequeños errores", "Requiere ayuda", "No funciona"],
        ["CloudWatch", "Monitorea y crea alarmas", "Monitorea correctamente",
         "Configuración parcial", "No configura"],
        ["Trusted Advisor", "Identifica y analiza", "Identifica recomendaciones",
         "Análisis limitado", "No utiliza"],
        ["Auto Scaling", "Configura y demuestra", "Configuración adecuada",
         "Configuración incompleta", "No configura"],
        ["Mejora de arquitectura", "Propone mejoras justificadas",
         "Propone mejoras", "Pocas propuestas", "No propone"],
        ["Trabajo en equipo", "Excelente participación",
         "Buena participación", "Participación irregular", "Baja"],
        ["Presentación", "Clara y técnica", "Clara", "Poco organizada",
         "No explica"],
    ]
    table(s, data, ML, 1.85, CW, [0.2, 0.22, 0.2, 0.2, 0.18], row_h=0.44,
          header_h=0.42, font=9.5, header_font=10.5)

    # ------------------------------------------------------- 28 puntaje
    n += 1
    s = new_slide(prs)
    header(s, "Puntaje y criterio de logro", "evaluación del taller")
    niveles = [("36 – 40", "Excelente"), ("31 – 35", "Logro destacado"),
               ("25 – 30", "Logro esperado"), ("20 – 24", "En proceso"),
               ("0 – 19", "En inicio")]
    bw = (CW - 4 * 0.25) / 5
    for i, (rango, nombre) in enumerate(niveles):
        x = ML + i * (bw + 0.25)
        rect(s, x, 2.3, bw, 2.1, fill=PANEL, line=SOFT)
        txt(s, x, 2.65, bw, 0.5, rango, size=21, bold=True, color=WHITE,
            align=PP_ALIGN.CENTER)
        ln = rect(s, x + bw / 2 - 0.35, 3.3, 0.7, 0.03, fill=DGRAY)
        ln.line.fill.background()
        txt(s, x, 3.55, bw, 0.6, nombre, size=14, color=GRAY,
            align=PP_ALIGN.CENTER)
    quote(s, ML, 4.9, CW, 1.4,
          "Puntaje máximo: 40 puntos, distribuidos en 10 criterios "
          "evaluados con la rúbrica.", size=16, sub="TOTAL")

    # --------------------------------------------------------- 29 reflexión
    n += 1
    s = new_slide(prs)
    header(s, "17. Preguntas de reflexión final", "cierre del taller")
    ref_l = [
        "¿Por qué no es recomendable depender de una sola instancia EC2?",
        "¿Qué función cumple un Load Balancer?",
        "¿Qué diferencia existe entre alta disponibilidad y escalabilidad?",
        "¿Para qué sirve CloudWatch?",
    ]
    ref_r = [
        "¿Qué información proporciona Trusted Advisor?",
        "¿Qué sucede cuando la demanda aumenta y se utiliza Auto Scaling?",
        "¿Qué pilar del Well-Architected es más importante para este caso?",
        "¿Qué mejoras implementarías si la empresa duplicara sus usuarios?",
    ]
    numbered(s, ML, 2.1, 5.9, 4.3, ref_l, size=15, gap=20)
    numbered(s, ML + 6.1, 2.1, 5.9, 4.3, ref_r, size=15, gap=20,
             start=5)

    # -------------------------------------------------------- 30 evidencias
    n += 1
    s = new_slide(prs)
    header(s, "18. Evidencias que debe entregar el estudiante",
           "checklist de entrega", size=26)
    ev_l = [
        "Capturas de pantalla de la instancia EC2.",
        "Evidencia del Load Balancer.",
        "Evidencia del Target Group.",
        "Evidencia de CloudWatch.",
        "Evidencia de Trusted Advisor.",
    ]
    ev_r = [
        "Evidencia del Auto Scaling Group.",
        "Diagrama final de arquitectura.",
        "Tabla de problemas y soluciones.",
        "Conclusiones individuales.",
    ]
    check_list(s, ML, 2.2, 5.9, ev_l, size=15.5, gap=16)
    check_list(s, ML + 6.1, 2.2, 5.9, ev_r, size=15.5, gap=16)
    quote(s, ML, 5.5, CW, 1.15,
          "Recordar eliminar todos los recursos creados en AWS al finalizar "
          "el laboratorio para evitar cargos.", size=15, sub="IMPORTANTE")

    # ------------------------------------------------------- 31 conclusión
    n += 1
    s = new_slide(prs)
    header(s, "Conclusión esperada", "cierre del taller")
    quote(s, ML, 2.1, CW, 3.0,
          "Una arquitectura AWS debe diseñarse considerando no solo el "
          "funcionamiento de la aplicación, sino también su disponibilidad, "
          "seguridad, monitoreo, escalabilidad, rendimiento y costos. "
          "Mediante EC2, Elastic Load Balancing, Auto Scaling, CloudWatch y "
          "Trusted Advisor es posible construir una infraestructura más "
          "resistente y adaptable a las necesidades de una organización.",
          size=17, sub="CONCLUSIÓN")
    txt(s, ML, 5.4, CW, 0.5, "¡Gracias!", size=30, bold=True, color=WHITE,
        align=PP_ALIGN.CENTER)
    txt(s, ML, 6.05, CW, 0.8,
        "Presenta: Stev Lozano — Actividades 3 y 4\n"
        "Integrante 1 — Actividades 1 y 2  ·  Integrante 2 — Actividades 3 y 4\n"
        "Integrante 3 — Actividades 5 y 6  ·  Integrante 4 — Actividades 7 y 8",
        size=12.5, color=DGRAY, align=PP_ALIGN.CENTER, spacing=1.3)

    # pie de página en todas menos la portada
    for i, slide in enumerate(prs.slides, start=1):
        if i == 1:
            continue
        footer(slide, i)

    prs.save(OUT)
    print("PPT creado:", OUT, "| diapositivas:", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    build()
