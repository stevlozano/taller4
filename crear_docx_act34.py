#!/usr/bin/env python3
"""Genera el DOCX de las Actividades 3 y 4 (fiabilidad y distribucion de trafico)."""
import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img_doc")
DEST = ("/home/codeol/Documentos/TECNOLOGÍA_CLOUD _CON_AWS /"
        "grupogaray_martes/Actividades 3 y 4 Fiabilidad y distribucion de "
        "trafico en AWS.docx")

BLACK = RGBColor(0, 0, 0)
GRAY = RGBColor(0x44, 0x44, 0x44)


# ----------------------------------------------------------------- utilidades
def setup_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)
    normal.font.color.rgb = BLACK
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Arial")
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.15

    conf = {"Title": (22, True), "Heading 1": (15, True),
            "Heading 2": (12.5, True), "Heading 3": (11.5, True)}
    for name, (size, bold) in conf.items():
        st = doc.styles[name]
        st.font.name = "Arial"
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.color.rgb = BLACK
        st.paragraph_format.space_before = Pt(14 if name != "Title" else 0)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.keep_with_next = True
        pPr = st.element.get_or_add_pPr()
        for bdr in pPr.findall(qn("w:pBdr")):
            pPr.remove(bdr)


def rich(doc, chunks, style=None, size=None, align=None, space_after=None):
    """chunks: lista de (texto, bold) o texto plano."""
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    if isinstance(chunks, str):
        chunks = [(chunks, False)]
    for text, bold in chunks:
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
    return p


def bullets(doc, items, size=11):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        if isinstance(it, str):
            it = [(it, False)]
        for text, bold in it:
            r = p.add_run(text)
            r.bold = bold
            r.font.size = Pt(size)
    return doc


def numlist(doc, items, size=11):
    for i, it in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.paragraph_format.space_after = Pt(4)
        r0 = p.add_run("%d.  " % i)
        r0.bold = True
        r0.font.size = Pt(size)
        if isinstance(it, str):
            it = [(it, False)]
        for text, bold in it:
            r = p.add_run(text)
            r.bold = bold
            r.font.size = Pt(size)


def shade_paragraph(p, fill="F2F2F2"):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def code(doc, lines):
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        shade_paragraph(p)
        r = p.add_run(line)
        r.font.name = "Courier New"
        r.font.size = Pt(9.5)


def picture(doc, name, width, caption):
    doc.add_picture(os.path.join(IMG, name), width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(caption)
    r.italic = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = GRAY


def shade_cell(cell, fill="E6E6E6"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def table(doc, header, rows, widths=None, size=10):
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    t.style = "Table Grid"
    t.autofit = True
    for j, text in enumerate(header):
        cell = t.cell(0, j)
        cell.text = ""
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(size)
        r.font.name = "Arial"
        shade_cell(cell)
    for i, row in enumerate(rows, 1):
        for j, text in enumerate(row):
            cell = t.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.size = Pt(size)
            r.font.name = "Arial"
    if widths:
        for j, w in enumerate(widths):
            for row in t.rows:
                row.cells[j].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def callout(doc, title, text):
    p = doc.add_paragraph()
    shade_paragraph(p, "EFEFEF")
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(title + " ")
    r.bold = True
    r.font.size = Pt(10.5)
    r2 = p.add_run(text)
    r2.font.size = Pt(10.5)


# ------------------------------------------------------------------ documento
def build():
    doc = Document()
    setup_styles(doc)

    doc.add_paragraph(
        "Actividades 3 y 4: Fiabilidad, alta disponibilidad y distribución "
        "de tráfico en AWS", style="Title")
    rich(doc, [("Taller 4 • Actividades 3 y 4 • Integrante 2", True)],
         size=11, space_after=2)
    rich(doc, [("Estudiante: ", True), ("Stev Lozano", False),
               ("  ·  Integrante 2 (Actividades 3 y 4)", False)],
         size=11, space_after=10)

    rich(doc, [
        ("Esta guía desarrolla dos actividades del taller. En la ", False),
        ("Actividad 3", True),
        (" eliminamos el punto único de fallo de la aplicación y logramos "
         "alta disponibilidad. En la ", False),
        ("Actividad 4", True),
        (" usamos Elastic Load Balancing (Application Load Balancer) para "
         "repartir las peticiones de los usuarios entre los servidores. "
         "Cada sección incluye el procedimiento paso a paso en la consola, "
         "las preguntas para el salón con sus respuestas y las soluciones "
         "a los errores más comunes.", False)])

    # ------------------------------------------------- plan de explicación
    doc.add_heading("Plan de explicación en el aula (25 minutos)", level=1)
    table(doc, ["Momento", "Qué hacer", "Tiempo"], [
        ["Presentación", "Mostrar los dos diagramas y explicar el punto "
         "único de fallo.", "5 min"],
        ["Pregunta al salón", "“¿Qué pasa si se apaga EC2-01?” "
         "escuchar 2 o 3 respuestas.", "3 min"],
        ["Actividad 4: conceptos", "Explicar Load Balancer, Listener, "
         "Target Group y health check con una analogía.", "5 min"],
        ["Consola en vivo", "Crear el Target Group y el ALB paso a paso "
         "proyectado.", "7 min"],
        ["Demo y cierre", "Alternar las páginas de cada servidor y "
         "responder preguntas.", "5 min"],
    ], widths=[1.4, 4.6, 1.0])

    # -------------------------------------------------------- ACTIVIDAD 3
    doc.add_heading("1. Actividad 3: Asegurar la fiabilidad y la alta "
                    "disponibilidad", level=1)

    doc.add_heading("1.1 Objetivo", level=2)
    rich(doc, "Evitar que la aplicación dependa de un único servidor: si un "
              "servidor falla, otro debe seguir atendiendo a los usuarios.")

    doc.add_heading("1.2 El problema: todo depende de un solo servidor",
                    level=2)
    rich(doc, [
        ("La empresa tiene la aplicación en una sola instancia EC2. Ese "
         "servidor es un ", False),
        ("punto único de fallo", True),
        (": si se apaga, se cae por mantenimiento o presenta una falla, la "
         "página web deja de existir para todos los usuarios. Además, cuando "
         "llegan muchas personas al mismo tiempo, un solo servidor se vuelve "
         "lento.", False)])
    callout(doc, "Analogía para el salón:",
            "es como un negocio con un solo cajero. Si el cajero se enferma, "
            "nadie puede comprar; y si llega mucha gente a la vez, la fila "
            "no avanza. La solución es tener varios cajeros y alguien que "
            "reparta la fila entre ellos.")

    doc.add_heading("1.3 Conceptos clave (explicación rápida)", level=2)
    table(doc, ["Concepto", "Definición fácil", "Ejemplo en el caso"], [
        ["Punto único de fallo", "Un componente cuyo fallo deja todo "
         "parado.", "La instancia EC2-01."],
        ["Alta disponibilidad", "El servicio sigue funcionando aunque un "
         "componente falle.", "Dos servidores atendiendo a la vez."],
        ["Zona de disponibilidad", "Centro de datos independiente dentro de "
         "una región.", "EC2-01 en us-east-1a y EC2-02 en us-east-1b."],
        ["Redundancia", "Tener copias de lo importante para usarlas si una "
         "falla.", "Dos instancias con la misma aplicación."],
        ["Health check", "Comprobación automática de que el servidor "
         "responde.", "El ALB hace un HTTP GET a la página cada pocos "
         "segundos."],
        ["Alta disponibilidad vs. escalabilidad", "La primera aguanta "
         "fallos; la segunda crece con la demanda.", "HA = no caerse · "
         "Escalabilidad = añadir servidores cuando llegan más usuarios."],
    ], widths=[1.6, 2.6, 2.8])

    doc.add_heading("1.4 Arquitectura inicial (con punto único de fallo)",
                    level=2)
    picture(doc, "doc_diag_inicial.png", 5.2,
            "Figura 1. Arquitectura inicial: un solo servidor para toda la "
            "aplicación.")
    bullets(doc, [
        "Una sola instancia concentra todo el tráfico.",
        "Si EC2-01 falla, no hay respaldo: la aplicación queda fuera de "
        "servicio.",
        "No se puede repartir la carga ni dar mantenimiento sin caída.",
    ])

    doc.add_heading("1.5 Arquitectura propuesta (con redundancia)", level=2)
    picture(doc, "doc_diag_propuesta.png", 5.6,
            "Figura 2. Propuesta: dos servidores detrás de un Load Balancer.")
    bullets(doc, [
        [("Dos instancias", True),
         (" (EC2-01 y EC2-02) con la misma aplicación: si una falla, la "
          "otra sigue atendiendo.", False)],
        [("Load Balancer", True),
         (" en el centro: recibe el tráfico y lo reparte entre los "
          "servidores que estén saludables.", False)],
        [("Comprobación de salud", True),
         (": el balanceador detecta automáticamente un servidor caído y "
          "deja de enviarle peticiones.", False)],
        [("Misma configuración", True),
         (": AMI, tipo de instancia, Security Group y página iguales en "
          "ambos servidores.", False)],
    ])

    doc.add_heading("1.6 Pregunta para el salón y respuesta esperada",
                    level=2)
    callout(doc, "Pregunta:",
            "¿Qué sucede si EC2-01 deja de funcionar?")
    bullets(doc, [
        "El health check del ALB falla dos veces seguidas y marca a EC2-01 "
        "como “unhealthy” (no saludable).",
        "El balanceador deja de enviarle peticiones y las redirige todas "
        "hacia EC2-02.",
        "El usuario no nota la falla: la página sigue respondiendo porque "
        "EC2-02 continúa trabajando.",
        "Cuando EC2-01 vuelva a responder, el balanceador lo vuelve a "
        "incluir en la lista de destinos.",
        "Lección: se eliminó el punto único de fallo gracias a la "
        "redundancia.",
    ])

    doc.add_heading("1.7 Procedimiento: crear la segunda instancia", level=2)
    numlist(doc, [
        [("Abrir ", False), ("Amazon EC2 → Instances → Launch instance", True),
         (".", False)],
        [("Nombre: ", True), ("WEB-SERVER-02", False),
         (" (la primera era WEB-SERVER-01).", False)],
        [("Seleccionar la ", False), ("misma AMI", True),
         (" (Amazon Linux 2023) y el ", False),
         ("mismo tipo de instancia", True),
         (" (t3.micro) para que ambos servidores sean equivalentes.", False)],
        [("Red: ", True),
         ("misma VPC y subred pública, con IP pública asignada "
          "(Auto-assign public IP).", False)],
        [("Security Group: ", True),
         ("seleccionar el grupo existente ", False),
         ("SG-WEB-LAB", True),
         (" que ya permite HTTP 80 (o crear uno idéntico).", False)],
        [("User data: ", True),
         ("pegar el mismo script de Apache, pero cambiando el título por ", False),
         ("“Servidor WEB 02 – Grupo A”", True),
         (" para distinguirlo en la demostración.", False)],
        [("Launch instance", True),
         (" y esperar a que la instancia esté ", False),
         ("Running", True), (" con los ", False),
         ("Status checks: 2/2 checks passed", True), (".", False)],
        [("Probar la IP pública individual de EC2-02", True),
         (" en el navegador antes de continuar.", False)],
    ])
    callout(doc, "Tip importante:",
            "las dos instancias deben quedar con el mismo contenido y el "
            "mismo Security Group; si no, la demostración del balanceo no "
            "se verá bien.")

    doc.add_heading("1.8 Verificación: ya no hay punto único de fallo",
                    level=2)
    numlist(doc, [
        "Abrir la aplicación por la IP pública de EC2-01 y dejarla en una "
        "pestaña; abrir otra pestaña con la IP de EC2-02.",
        "Detener (Stop) la instancia EC2-01 desde la consola.",
        "Recargar la pestaña de EC2-01: la página dejará de responder "
        "(esa IP murió con la instancia).",
        "Recargar la pestaña de EC2-02: la página sigue respondiendo "
        "normalmente.",
        "Conclusión: la aplicación ya no depende de un solo servidor.",
    ])

    doc.add_heading("1.9 Conclusión de la actividad 3", level=2)
    rich(doc, "Con dos instancias y un punto de entrada central eliminamos "
              "el punto único de fallo: la aplicación se recupera ante la "
              "caída de un servidor y puede recibir mantenimiento sin "
              "interrumpir el servicio. En la siguiente actividad "
              "conectamos ese punto de entrada (el Load Balancer) para que "
              "reparta el tráfico de verdad.")

    # -------------------------------------------------------- ACTIVIDAD 4
    doc.add_heading("2. Actividad 4: Distribuir el tráfico entre las "
                    "instancias (Elastic Load Balancing)", level=1)

    doc.add_heading("2.1 Objetivo", level=2)
    rich(doc, "Configurar un Application Load Balancer (ALB) que reciba "
              "todas las peticiones de los usuarios y las reparta entre "
              "EC2-01 y EC2-02.")

    doc.add_heading("2.2 ¿Qué es un Load Balancer?", level=2)
    rich(doc, [
        ("Un ", False), ("balanceador de carga", True),
        (" (Load Balancer) es el punto de entrada único de la aplicación: "
         "recibe todas las peticiones y las envía a uno de los servidores "
         "disponibles, evitando que un servidor se sature mientras otro "
         "está ocioso. Con Elastic Load Balancing de AWS lo montamos en "
         "minutos y sin comprar hardware.", False)])
    callout(doc, "Analogía para el salón:",
            "es el mesero del restaurante. Los clientes (usuarios) no eligen "
            "mesa: el mesero reparte las mesas (servidores) disponibles, "
            "observa cuáles están ocupadas y no sienta a nadie en una mesa "
            "que esté sucia o rota (servidor caído).")

    doc.add_heading("2.3 Componentes que debemos conocer", level=2)
    table(doc, ["Componente", "Qué es en palabras simples",
                "Configuración del taller"], [
        ["Load Balancer (ALB)", "El mesero: recibe el tráfico de Internet.",
         "Internet-facing, en 2 subredes."],
        ["Listener", "La puerta por donde entra: protocolo y puerto.",
         "HTTP en el puerto 80."],
        ["Target Group", "La lista de mesas disponibles a las que se "
         "reparte el tráfico.", "TG-WEB con EC2-01 y EC2-02."],
        ["Target (destino)", "Cada servidor registrado en ese grupo.",
         "Instancias EC2-01 y EC2-02."],
        ["Health check", "La revisión automática del mesero: ¿responde "
         "esta mesa?", "HTTP GET a “/” cada 30 segundos."],
        ["DNS del ALB", "La dirección única que comparten los usuarios.",
         "alb-web-xxxx.us-east-1.elb.amazonaws.com"],
    ], widths=[1.5, 2.7, 2.8])

    doc.add_heading("2.4 ¿Por qué Application Load Balancer?", level=2)
    bullets(doc, [
        "Está pensado para tráfico HTTP/HTTPS de aplicaciones web, que es "
        "exactamente nuestro caso.",
        "Entiende direcciones web (por ejemplo, /tienda o /api) y puede "
        "dirigir cada una a servidores diferentes.",
        "Trabaja con Target Groups y health checks automáticos.",
        "Hay balanceadores de red (NLB) para tráfico muy exigente y "
        "orientado a puertos; para este taller el ALB es el indicado.",
    ])

    doc.add_heading("2.5 Procedimiento paso a paso en la consola", level=2)

    doc.add_heading("Paso 1. Crear el Target Group", level=3)
    numlist(doc, [
        "Ir a EC2 → Target Groups → Create target group.",
        "Choose target type: Instances.",
        "Target group name: TG-WEB.",
        "Protocol: HTTP · Port: 80 · VPC: la del laboratorio.",
        "Health check: HTTP, ruta “/”, umbral de 2 respuestas "
        "incorrectas antes de marcar el destino como no saludable.",
        "Next → registrar EC2-01 y EC2-02 → Create target group.",
        "Verificar en la pestaña Targets que ambas aparezcan con estado "
        "“unhealthy” o “unused” al principio (se pondrán "
        "“healthy” en el paso 3).",
    ])

    doc.add_heading("Paso 2. Crear el Application Load Balancer", level=3)
    numlist(doc, [
        "Ir a EC2 → Load Balancers → Create Load Balancer → Application "
        "Load Balancer.",
        "Load balancer name: ALB-WEB.",
        "Scheme: Internet-facing · IP address type: IPv4.",
        [("Mapping: seleccionar ", False),
         ("al menos 2 subredes distintas", True),
         (" (idealmente en 2 zonas de disponibilidad) para que el propio "
          "balanceador también sea redundante.", False)],
        [("Security groups: crear uno nuevo (por ejemplo SG-ALB) que "
          "permita ", False), ("HTTP, puerto 80, desde 0.0.0.0/0", True),
         (" (es el SG del balanceador, no el de las instancias).", False)],
        [("Listeners and rules: mantener el listener ", False),
         ("HTTP:80", True), (" y como acción Forward hacia ", False),
         ("TG-WEB", True), (".", False)],
        "Create load balancer.",
    ])
    callout(doc, "Error clásico:",
            "usar el mismo Security Group para el ALB y para las instancias, "
            "o no abrir el puerto 80 en el grupo del ALB. Si eso pasa, el "
            "navegador no podrá contactar al balanceador.")

    doc.add_heading("Paso 3. Esperar y copiar el DNS", level=3)
    numlist(doc, [
        "Esperar a que el ALB pase de “Active” a estado "
        "disponible (1 o 2 minutos).",
        "Seleccionar ALB-WEB → Details → DNS name → copiar la dirección.",
        [("Abrir ", False), ("http://DNS_DEL_ALB", True),
         (" en el navegador (con http, porque el listener es HTTP).",
          False)],
    ])

    doc.add_heading("Paso 4. Comprobar la salud de los destinos", level=3)
    numlist(doc, [
        "Ir a Target Groups → TG-WEB → pestaña Targets.",
        [("Esperar a que EC2-01 y EC2-02 aparezcan con estado ", False),
         ("healthy", True), (" (verde).", False)],
        "Si algún destino queda “unhealthy”, revisar: puerto 80 "
        "abierto en el SG de las instancias, Apache activo (systemctl "
        "status httpd) y ruta del health check (“/”).",
    ])

    doc.add_heading("Paso 5. Probar desde el navegador", level=3)
    numlist(doc, [
        "Abrir el DNS del ALB y recargar la página varias veces.",
        "La página debe responder siempre, sin importar qué servidor la "
        "atienda.",
        "Registrar la captura de pantalla: DNS visible en la barra de "
        "direcciones.",
    ])

    doc.add_heading("2.6 Demostración en el salón: el tráfico se reparte",
                    level=2)
    rich(doc, [("Para que los estudiantes ", False), ("vean", True),
               (" el balanceo, cada servidor mostrará un texto "
                "diferente. Ejecutar en cada instancia (con SSH o EC2 "
                "Instance Connect):", False)])
    code(doc, [
        "# En EC2-01",
        "echo '<h1>Servidor WEB 01 - Grupo A</h1>' | sudo tee "
        "/var/www/html/index.html",
        "",
        "# En EC2-02",
        "echo '<h1>Servidor WEB 02 - Grupo A</h1>' | sudo tee "
        "/var/www/html/index.html",
    ])
    picture(doc, "doc_elb_demo.png", 6.0,
            "Figura 3. El DNS del ALB reparte las peticiones entre los dos "
            "servidores.")
    bullets(doc, [
        "Recargar el navegador varias veces: alternará entre “Servidor "
        "WEB 01” y “Servidor WEB 02”.",
        "El usuario solo conoce una dirección (la del ALB); los servidores "
        "pueden cambiar sin que él se entere.",
        "Prueba avanzada: detener EC2-01 y seguir recargando; el tráfico "
        "continuará llegando a EC2-02.",
    ])

    doc.add_heading("2.7 Preguntas para el salón (con respuestas)", level=2)
    table(doc, ["Pregunta", "Respuesta esperada"], [
        ["¿Para qué sirve el Load Balancer?",
         "Recibe todas las peticiones y las reparte entre los servidores "
         "saludables, evitando sobrecargar uno solo y ocultando los fallos."],
        ["¿Qué pasa si se apaga una instancia?",
         "El health check la marca como no saludable y el ALB deja de "
         "enviarle tráfico; las peticiones van a la otra instancia."],
        ["¿Por qué el ALB necesita 2 subredes?",
         "Para que el balanceador también sobreviva a la caída de una zona "
         "de disponibilidad."],
        ["¿El usuario debe conocer las IPs de las EC2?",
         "No. Solo usa el DNS del ALB; las IPs de las instancias pueden "
         "cambiar sin afectar a los usuarios."],
        ["¿Qué falta para estar realmente listos?",
         "Monitoreo con alarmas (Actividad 5), revisión con Trusted Advisor "
         "(Actividad 6) y Auto Scaling (Actividad 7)."],
    ], widths=[2.6, 4.4])

    doc.add_heading("2.8 Si no funciona: solución de problemas", level=2)
    table(doc, ["Síntoma", "Causa probable", "Solución"], [
        ["El navegador no abre el DNS del ALB",
         "El SG del balanceador no permite el puerto 80 o el ALB aún no "
         "está activo.",
         "Agregar regla HTTP 80 desde 0.0.0.0/0 al SG del ALB y esperar "
         "1-2 minutos."],
        ["Error 503 Service Unavailable",
         "Los destinos están unhealthy o el Target Group no está asociado "
         "al listener.",
         "Revisar Targets en TG-WEB, el health check y la acción Forward "
         "del listener."],
        ["Error 400 Bad Request",
         "Se está usando https:// pero el listener es HTTP.",
         "Escribir http:// delante del DNS."],
        ["Siempre responde el mismo servidor",
         "Ambas instancias muestran exactamente el mismo texto.",
         "Cambiar el index.html de un servidor (usar el comando de la "
         "demostración)."],
        ["La página no carga pero la IP individual sí",
         "Falta el listener o la ruta del health check es incorrecta.",
         "Revisar listener HTTP:80 → Forward → TG-WEB y la ruta “/”."],
        ["Timeout al abrir la página",
         "El SG de las instancias no permite el tráfico desde el ALB.",
         "Abrir HTTP 80 en el SG de las instancias (origen 0.0.0.0/0 o el "
         "rango de la VPC)."],
    ], widths=[2.0, 2.5, 2.5])

    doc.add_heading("2.9 Resumen de la configuración", level=2)
    table(doc, ["Servicio", "Configuración", "Propósito"], [
        ["EC2", "WEB-SERVER-01 y WEB-SERVER-02 (t3.micro), SG con HTTP 80",
         "Ejecutar la aplicación de forma redundante."],
        ["Target Group", "TG-WEB, protocolo HTTP, puerto 80, health check “/”",
         "Agrupar destinos y comprobar su salud."],
        ["Application Load Balancer", "ALB-WEB, Internet-facing, 2 subredes, "
         "listener HTTP:80", "Punto de entrada único y distribución "
         "de tráfico."],
        ["Security Group", "SG-ALB con HTTP 80 desde Internet",
         "Permitir el acceso de los usuarios al balanceador."],
        ["Amazon VPC", "VPC del laboratorio con subredes públicas",
         "Aislar y conectar los recursos."],
    ], widths=[1.6, 3.0, 2.4])

    doc.add_heading("2.10 Conclusión de la actividad 4", level=2)
    rich(doc, "El Application Load Balancer convierte varios servidores en "
              "una sola dirección para el usuario: reparte la carga, "
              "detecta fallos automáticamente y permite crecer sumando "
              "instancias nuevas sin cambiar la URL. Combinado con la "
              "redundancia de la Actividad 3, la aplicación deja de depender "
              "de una sola máquina.")

    # ---------------------------------------------------------------- cierre
    doc.add_heading("3. Cierre de la explicación", level=1)

    doc.add_heading("3.1 Cinco ideas para no olvidar", level=2)
    numlist(doc, [
        [("Un solo servidor es un punto único de fallo", True),
         ("; con dos instancias la aplicación sobrevive a la caída de una.",
          False)],
        [("El Load Balancer es el punto de entrada único", True),
         (": el usuario solo conoce el DNS del ALB.", False)],
        [("Los health checks", True),
         (" hacen el trabajo pesado: marcan quién está sano y quién no, sin "
          "intervención manual.", False)],
        [("El ALB necesita 2 subredes", True),
         (" y su propio Security Group con el puerto 80 abierto.", False)],
        [("Alta disponibilidad ≠ escalabilidad", True),
         (": la primera aguanta fallos; la segunda agrega servidores cuando "
          "sube la demanda (Actividad 7).", False)],
    ])

    doc.add_heading("3.2 Evidencias que debemos entregar", level=2)
    bullets(doc, [
        "Captura de EC2 con WEB-SERVER-01 y WEB-SERVER-02 en estado Running.",
        "Captura del Target Group TG-WEB con los dos destinos “healthy”.",
        "Captura del Load Balancer ALB-WEB con su DNS visible.",
        "Captura de la página abierta por el DNS del ALB (con la dirección "
        "en el navegador).",
        "Captura de la demostración: página 01 y página 02 alternando.",
        "Captura de EC2-01 detenida y la aplicación respondiendo igual.",
    ])

    doc.add_heading("3.3 Reto rápido para el salón (5 minutos)", level=2)
    callout(doc, "Reto:",
            "en equipos, detengan una de sus instancias y comprueben que la "
            "página siga respondiendo por el DNS del ALB. Luego respondan: "
            "¿qué pasaría si se cayeran las dos instancias al mismo tiempo? "
            "(Respuesta: no habría a dónde enrutar el tráfico; por eso en "
            "las actividades siguientes usamos alarmas y Auto Scaling.)")

    doc.add_heading("3.4 Conclusión general", level=2)
    rich(doc, "Con EC2-01, EC2-02, un Target Group y un Application Load "
              "Balancer pasamos de una arquitectura frágil —un solo "
              "servidor— a una arquitectura disponible: las peticiones se "
              "reparten, los fallos se detectan solos y la aplicación "
              "sigue en línea. Estos son los cimientos sobre los que se "
              "apoyan el monitoreo, el escalado automático y la mejora "
              "continua que veremos en las siguientes actividades.")

    doc.add_heading("Fuentes oficiales", level=1)
    fuentes = [
        "Elastic Load Balancing — Conceptos básicos: "
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html",
        "Application Load Balancers — Configuración: "
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html",
        "Target Groups — Health checks: "
        "https://docs.aws.amazon.com/elasticloadbalancing/latest/target-group/health-checks.html",
        "AWS Well-Architected Framework (pilar Fiabilidad): "
        "https://docs.aws.amazon.com/wellarchitected/latest/framework/rel.html",
        "Amazon EC2 — Security Groups: "
        "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html",
    ]
    for f in fuentes:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f)
        r.font.size = Pt(9.5)

    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    doc.save(DEST)
    print("DOCX creado:", DEST)


if __name__ == "__main__":
    build()
