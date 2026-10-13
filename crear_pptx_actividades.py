#!/usr/bin/env python3
"""Presentacion nueva: solo Actividades 1 a 8 del Taller 4 (grupogaray)."""
import os

from pptx import Presentation
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

import crear_pptx as ui

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = ("/home/codeol/Documentos/TECNOLOGÍA_CLOUD _CON_AWS /"
       "grupogaray_martes/Taller-4-AWS-Actividades-1-a-8.pptx")

TOTAL = 21


def foot(slide, n):
    ui.footer(slide, n, TOTAL)


def code_panel(slide, x, y, w, h, lines, size=10.5):
    ui.rect(slide, x, y, w, h, fill=ui.PANEL, line=ui.SOFT, lw=1.0)
    box = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.16),
                                   Inches(w - 0.4), Inches(h - 0.32))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.05
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.name = "Courier New"
        r.font.color.rgb = ui.WHITE


def sub(slide, x, y, w, text, size=15):
    ui.txt(slide, x, y, w, 0.35, text, size=size, bold=True, color=ui.WHITE)


def build():
    prs = Presentation()
    prs.slide_width = Inches(ui.SW)
    prs.slide_height = Inches(ui.SH)
    n = 0

    # ------------------------------------------------------------ 1 portada
    n += 1
    s = ui.new_slide(prs)
    ui.pic(s, "portada.png", 0, 1.7, w=5.7, center_x=10.05)
    ui.txt(s, ui.ML, 1.05, 6.2, 0.35,
           "TALLER 4 · ACTIVIDADES 1 A 8 · PRESENTACIÓN DEL GRUPO",
           size=13, bold=True, color=ui.DGRAY)
    ui.txt(s, ui.ML, 1.55, 6.2, 2.6,
           "Arquitectura AWS segura, disponible y escalable",
           size=36, bold=True, color=ui.WHITE, spacing=1.05)
    ln = ui.rect(s, ui.ML, 4.15, 2.2, 0.045, fill=ui.WHITE)
    ln.line.fill.background()
    ui.txt(s, ui.ML, 4.45, 6.2, 0.7,
           "Cada integrante presenta sus actividades en la consola de AWS\n"
           "Plataforma: AWS Management Console · Lab de 4 horas",
           size=13.5, color=ui.GRAY, spacing=1.3)
    ui.txt(s, ui.ML, 5.55, 6.2, 1.4,
           "Actividades 1 y 2 — Manuel Antonio Garay Rivera\n"
           "Actividades 3 y 4 — Stev Lozano\n"
           "Actividades 5 y 6 — Integrante 3\n"
           "Actividades 7 y 8 — Oswaldo",
           size=13, color=ui.WHITE, spacing=1.4)

    # -------------------------------------------------------------- 2 equipos
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Equipos y recorrido de la presentación",
              "cada integrante presenta sus actividades")
    ui.cards(s, ui.ML, 2.0, ui.CW, 4.6, [
        "Actividades 1 y 2 — Manuel Antonio Garay Rivera\n\n"
        "Los seis pilares del Well-Architected y publicación de un "
        "servidor web en EC2.",
        "Actividades 3 y 4 — Stev Lozano\n\n"
        "Alta disponibilidad y distribución del tráfico con un "
        "Application Load Balancer.",
        "Actividades 5 y 6 — Integrante 3\n\n"
        "Monitoreo en tiempo real con CloudWatch y recomendaciones de "
        "Trusted Advisor.",
        "Actividades 7 y 8 — Oswaldo\n\n"
        "Escalado automático ante una campaña y 5 mejoras a la "
        "arquitectura.",
    ], cols=2, text_size=14)

    # ---------------------------------------------------------- 3 ACT 1 pilares
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Los seis pilares del Well-Architected Framework",
              "actividad 1 · manuel antonio garay rivera", size=26)
    ui.txt(s, ui.ML, 1.85, ui.CW, 0.5,
           "Objetivo: reconocer los principios para construir una "
           "arquitectura AWS segura, eficiente, fiable y optimizada.",
           size=14, color=ui.GRAY)
    x, y, w, h = ui.pic(s, "pilares.png", 0, 2.4, w=9.0, center_x=ui.SW / 2)
    ui.caption(s, x, y + h + 0.2, w, "Aplicación de cada pilar al caso de "
                                     "la empresa")

    # ---------------------------------------------------------- 4 ACT 1 matriz
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Problema → Riesgo → Pilar → Solución",
              "actividad 1 · manuel antonio garay rivera", size=27)
    ui.txt(s, ui.ML, 1.75, ui.CW, 0.35,
           "Los cuatro problemas explícitos del caso y las acciones "
           "propuestas (una acción puede aportar a más de un pilar).",
           size=13.5, color=ui.GRAY)
    data = [
        ["Problema", "Riesgo", "Pilar", "Solución AWS"],
        ["Servidor web único", "Interrupción total del servicio",
         "Fiabilidad", "Load Balancer + 2 instancias"],
        ["Sin monitoreo", "Detección tardía de incidentes",
         "Excelencia operativa", "Métricas y alarmas de CloudWatch"],
        ["Instancia sobredimensionada", "Gasto innecesario",
         "Optimización de costos", "Dimensionar y Auto Scaling"],
        ["Sin mecanismos de recuperación", "Prolongada fuera de servicio",
         "Fiabilidad", "Reemplazo automático y copias probadas"],
    ]
    ui.table(s, data, ui.ML, 2.2, ui.CW, [0.24, 0.27, 0.19, 0.30],
             row_h=0.5, header_h=0.44, font=11.5, header_font=11.5)
    ui.quote(s, ui.ML, 4.85, ui.CW, 1.0,
             "Acciones complementarias: permisos mínimos en IAM, reglas "
             "específicas de Security Groups, cifrado de EBS y HTTPS; "
             "retirar recursos inactivos.", size=13.5)
    ui.txt(s, ui.ML, 6.05, ui.CW, 0.7,
           "Conclusión: la mejora prioritaria es eliminar el punto único "
           "de fallo y detectar incidentes oportunamente; los seis pilares "
           "orientan las decisiones y se revisan con mediciones.",
           size=13, color=ui.GRAY)

    # -------------------------------------------------------- 5 ACT 2 proceso
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Publicar servidores según la carga de trabajo",
              "actividad 2 · manuel antonio garay rivera", size=26)
    ui.txt(s, ui.ML, 1.8, 6.6, 0.4,
           "Objetivo: configurar una instancia EC2 para servir una página "
           "sencilla por HTTP.", size=13.5, color=ui.GRAY)
    ui.numbered(s, ui.ML, 2.35, 6.6, 4.5, [
        "Abrir la región elegida y elegir EC2 → Launch instance.",
        "Nombre WEB-SERVER-01, Amazon Linux 2023 y tipo t3.micro "
        "(revisar costo y elegibilidad de la cuenta).",
        "Key pair: opcional si se usa User data; el puerto 22 no es "
        "necesario para esta práctica.",
        "Network settings: VPC y subred pública, con IP pública "
        "asignada y ruta 0.0.0.0/0 hacia el Internet Gateway.",
        "Crear SG-WEB-LAB: HTTP 80 desde 0.0.0.0/0 (SSH 22 solo desde la "
        "IP del administrador /32, si se requiere).",
        "Volumen EBS cifrado, pegar el script en Advanced details → "
        "Launch instance.",
    ], size=13.5, gap=9)
    x, y, w, h = ui.pic(s, "ec2_launch.png", 0, 2.5, w=5.4, center_x=10.2)
    ui.caption(s, x, y + h + 0.2, w, "Configuración de la instancia")

    # -------------------------------------------------- 6 ACT 2 script/verif
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Script de User data, verificación y errores comunes",
              "actividad 2 · manuel antonio garay rivera", size=25)
    code_panel(s, ui.ML, 1.95, 6.1, 3.0, [
        "#!/bin/bash",
        "set -eu",
        "dnf install -y httpd",
        "cat > /var/www/html/index.html <<'HTML'",
        "<h1>Servidor Web AWS – Grupo 01</h1>",
        "<p>Instancia: WEB-SERVER-01</p>",
        "<p>El servidor web está funcionando.</p>",
        "HTML",
        "systemctl enable --now httpd",
    ], size=11)
    ui.txt(s, ui.ML, 5.1, 6.1, 0.7,
           "Se ejecuta como root en el primer arranque: instala Apache, "
           "crea la página y activa el servicio para futuros reinicios.",
           size=12.5, color=ui.GRAY)
    ui.quote(s, ui.ML, 5.9, 6.1, 1.0,
             "Al terminar el laboratorio: terminar la instancia y eliminar "
             "los recursos propios (volúmenes y IPs reservadas).",
             size=12.5)
    sub(s, ui.ML + 6.6, 1.9, 5.3, "Verificación")
    ui.bullets(s, ui.ML + 6.6, 2.4, 5.3, 1.6, [
        "Esperar Running con Status checks 2/2 (la instalación tarda).",
        "Abrir http://IP_PUBLICA en el navegador.",
        "Comprobar el título “Servidor Web AWS – Grupo 01” y "
        "registrar capturas.",
    ], size=13, gap=7)
    sub(s, ui.ML + 6.6, 4.15, 5.3, "Si la página no responde")
    ui.bullets(s, ui.ML + 6.6, 4.65, 5.3, 2.3, [
        "Revisar la IP actual y el puerto 80 abierto en el SG.",
        "Verificar la ruta al Internet Gateway y las ACL de red.",
        "Comprobar Apache: systemctl status httpd.",
        "Si User data falló: /var/log/cloud-init-output.log.",
        "Las comprobaciones de EC2 no garantizan que HTTP funcione.",
    ], size=13, gap=6)

    # ------------------------------------------------------- 7 ACT 3 diagramas
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Asegurar la fiabilidad y alta disponibilidad",
              "actividad 3 · stev lozano", size=27)
    ui.txt(s, ui.ML, 1.8, ui.CW, 0.35,
           "Objetivo: evitar que la aplicación dependa de un único "
           "servidor (punto único de fallo).", size=13.5, color=ui.GRAY)
    ui.pic(s, "diag_inicial.png", 0, 2.45, h=3.4, center_x=3.65)
    ui.caption(s, 1.4, 2.1, 4.5, "Arquitectura inicial")
    ui.pic(s, "diag_propuesta.png", 0, 2.45, h=3.4, center_x=9.6)
    ui.caption(s, 7.3, 2.1, 4.6, "Propuesta con 2 instancias")
    ui.quote(s, ui.ML, 6.1, ui.CW, 0.8,
             "Pregunta: ¿qué sucede si EC2-01 deja de funcionar? → el ALB "
             "lo marca como no saludable y el tráfico continúa por EC2-02.",
             size=13.5)

    # ---------------------------------------------------- 8 ACT 3 procedimiento
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Crear la segunda instancia y verificar",
              "actividad 3 · stev lozano", size=27)
    sub(s, ui.ML, 1.85, 6.4, "Procedimiento: WEB-SERVER-02")
    ui.numbered(s, ui.ML, 2.35, 6.4, 3.6, [
        "EC2 → Instances → Launch instance, nombre WEB-SERVER-02.",
        "Misma AMI (Amazon Linux 2023) y mismo tipo (t3.micro) para que "
        "los servidores sean equivalentes.",
        "Misma VPC y subred pública con IP pública asignada.",
        "Security Group: reutilizar SG-WEB-LAB (HTTP 80).",
        "User data: el mismo script, pero con el título “Servidor "
        "WEB 02 – Grupo A”.",
        "Launch instance, esperar Running 2/2 y probar su IP individual.",
    ], size=13.5, gap=8)
    sub(s, ui.ML + 6.9, 1.85, 5.1, "Verificación")
    ui.bullets(s, ui.ML + 6.9, 2.35, 5.1, 3.0, [
        "Abrir la app por la IP de EC2-01 en una pestaña y por la de "
        "EC2-02 en otra.",
        "Detener (Stop) EC2-01: su IP deja de responder.",
        "EC2-02 sigue respondiendo normalmente.",
        "Conclusión: ya no hay punto único de fallo.",
    ], size=13, gap=8)
    ui.quote(s, ui.ML + 6.9, 5.35, 5.1, 1.3,
             "Tip: ambas instancias deben quedar con el mismo contenido y "
             "el mismo Security Group para que la demo del balanceo se vea "
             "bien.", size=13)

    # ------------------------------------------------------ 9 ACT 4 conceptos
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Distribuir el tráfico: Application Load Balancer",
              "actividad 4 · stev lozano", size=26)
    ui.txt(s, ui.ML, 1.78, ui.CW, 0.35,
           "Servicio: Elastic Load Balancing — el balanceador es el punto "
           "de entrada único: recibe las peticiones y las reparte entre "
           "los servidores saludables.", size=13.5, color=ui.GRAY)
    ui.quote(s, ui.ML, 2.2, ui.CW, 0.85,
             "Analogía: es el mesero del restaurante — reparte las mesas "
             "disponibles y no sienta a nadie en una mesa caída.",
             size=13.5)
    data = [
        ["Componente", "En palabras simples", "En el taller"],
        ["Load Balancer (ALB)", "Recibe el tráfico de Internet.",
         "Internet-facing en 2 subredes"],
        ["Listener", "Puerta de entrada: protocolo y puerto.",
         "HTTP en el puerto 80"],
        ["Target Group", "Lista de servidores destino.",
         "TG-WEB con EC2-01 y EC2-02"],
        ["Target", "Cada servidor registrado.", "Instancias EC2"],
        ["Health check", "Comprueba si el servidor responde.",
         "HTTP GET a “/” cada 30 s"],
        ["DNS del ALB", "Dirección única del usuario.",
         "…elb.amazonaws.com"],
    ]
    ui.table(s, data, ui.ML, 3.3, ui.CW, [0.24, 0.42, 0.34], row_h=0.42,
             header_h=0.4, font=11, header_font=11)

    # --------------------------------------------------- 10 ACT 4 procedimiento
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Procedimiento en la consola (5 pasos)",
              "actividad 4 · stev lozano", size=27)
    ui.numbered(s, ui.ML, 1.95, 5.9, 4.4, [
        "Target Group: EC2 → Target Groups → Create; Instances; nombre "
        "TG-WEB; HTTP 80; VPC del lab; health check “/”; registrar "
        "EC2-01 y EC2-02.",
        "Load Balancer: EC2 → Load Balancers → Create → Application; "
        "nombre ALB-WEB; Internet-facing; IPv4.",
        "Mapping: elegir al menos 2 subredes distintas (2 zonas de "
        "disponibilidad) para que el balanceador también sea redundante.",
    ], size=13.5, gap=14)
    ui.numbered(s, ui.ML + 6.1, 1.95, 5.9, 3.2, [
        "Security Group: crear SG-ALB con HTTP 80 desde 0.0.0.0/0 (es el "
        "SG del balanceador, no el de las instancias).",
        "Listener: HTTP:80 → acción Forward hacia TG-WEB → Create load "
        "balancer. Esperar estado Active, copiar el DNS y abrir "
        "http://DNS.",
    ], size=13.5, gap=14, start=4)
    ui.quote(s, ui.ML + 6.1, 4.7, 5.9, 1.15,
             "Error clásico: usar el mismo Security Group para el ALB y "
             "las instancias, o no abrir el 80 en el balanceador.",
             size=13)
    ui.txt(s, ui.ML, 6.1, ui.CW, 0.7,
           "Comprobación: en Target Groups → TG-WEB → Targets, las dos "
           "instancias deben quedar en estado healthy (verde) antes de "
           "probar desde el navegador.", size=13, color=ui.GRAY)

    # -------------------------------------------------------- 11 ACT 4 demo
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Demostración: el tráfico se distribuye",
              "actividad 4 · stev lozano", size=27)
    ui.pic(s, "elb_demo.png", ui.ML, 2.1, w=6.3)
    code_panel(s, ui.ML + 6.8, 2.1, 5.2, 1.7, [
        "# En EC2-01",
        "echo '<h1>Servidor WEB 01 - Grupo A</h1>' | sudo tee \\",
        "  /var/www/html/index.html",
    ], size=10.5)
    code_panel(s, ui.ML + 6.8, 4.0, 5.2, 1.7, [
        "# En EC2-02",
        "echo '<h1>Servidor WEB 02 - Grupo A</h1>' | sudo tee \\",
        "  /var/www/html/index.html",
    ], size=10.5)
    ui.bullets(s, ui.ML + 6.8, 5.95, 5.2, 1.0, [
        "Refrescar varias veces: alterna entre WEB 01 y WEB 02.",
        "Detener EC2-01 y seguir recargando: la app sigue en línea.",
    ], size=12.5, gap=6)

    # ------------------------------------------------- 12 ACT 4 troubleshooting
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Si no funciona: solución de problemas",
              "actividad 4 · stev lozano", size=27)
    data = [
        ["Síntoma", "Causa probable", "Solución"],
        ["El navegador no abre el DNS del ALB",
         "El SG del ALB no permite el 80 o aún no está activo.",
         "Agregar HTTP 80 desde 0.0.0.0/0 y esperar 1-2 minutos."],
        ["Error 503 Service Unavailable",
         "Destinos unhealthy o falta el Forward del listener.",
         "Revisar Targets, health check y acción Forward a TG-WEB."],
        ["Error 400 Bad Request",
         "Se usa https:// pero el listener es HTTP.",
         "Escribir http:// delante del DNS."],
        ["Siempre responde el mismo servidor",
         "Ambas instancias muestran el mismo texto.",
         "Cambiar el index.html de un servidor (comando de la demo)."],
        ["Timeout al abrir la página",
         "El SG de las instancias no permite el tráfico del ALB.",
         "Abrir HTTP 80 en el Security Group de las instancias."],
    ]
    ui.table(s, data, ui.ML, 1.85, ui.CW, [0.28, 0.36, 0.36], row_h=0.72,
             header_h=0.44, font=11, header_font=11.5)
    ui.txt(s, ui.ML, 6.0, ui.CW, 0.6,
           "Regla de oro: revisar primero el estado de los targets, luego "
           "los Security Group y por último el listener.",
           size=13, color=ui.GRAY)

    # -------------------------------------------------------- 13 ACT 5 CloudWatch
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Monitorear recursos y aplicaciones en tiempo real",
              "actividad 5 · integrante 3", size=25)
    ui.txt(s, ui.ML, 1.8, ui.CW, 0.35,
           "Servicio: Amazon CloudWatch — supervisar el comportamiento de "
           "las instancias y detectar situaciones anormales.",
           size=13.5, color=ui.GRAY)
    x, y, w, h = ui.pic(s, "cloudwatch.png", ui.ML, 2.4, w=6.3)
    ui.caption(s, x, y + h + 0.18, w, "Métricas y alarma de CPU")
    sub(s, ui.ML + 6.9, 2.3, 5.1, "Qué observar")
    ui.bullets(s, ui.ML + 6.9, 2.8, 5.1, 2.5, [
        "CPU y estado de las instancias.",
        "Tráfico de red y solicitudes.",
        "Estado de los destinos del Load Balancer.",
        "Alarmas configuradas.",
    ], size=14, gap=9)
    ui.quote(s, ui.ML + 6.9, 5.2, 5.1, 1.5,
             "Actividad: crear una alarma de CPU — si el uso supera un "
             "porcentaje durante un periodo establecido, generar una "
             "alerta.", size=13.5)

    # -------------------------------------------------- 14 ACT 5 preguntas
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Preguntas de análisis (Actividad 5)",
              "actividad 5 · integrante 3", size=27)
    data = [
        ["Pregunta", "Respuesta"],
        ["¿Qué recurso presenta mayor utilización?",
         "La instancia EC2 con mayor porcentaje de CPU: es la que "
         "concentra más carga de procesamiento."],
        ["¿Qué ocurre cuando aumenta el tráfico?",
         "Aumentan las solicitudes y, con ellas, CPU, memoria y red; si la "
         "capacidad no alcanza, la aplicación se vuelve lenta."],
        ["¿Cómo sabemos que una instancia presenta problemas?",
         "Con las métricas de CloudWatch, las comprobaciones de estado de "
         "EC2 y el estado de los destinos del ALB; las alarmas detectan "
         "valores anormales."],
        ["¿Qué métrica sería útil para activar el escalado?",
         "CPUUtilization de EC2: por ejemplo, escalar cuando el uso "
         "promedio supera el 70 % durante un periodo determinado."],
    ]
    ui.table(s, data, ui.ML, 1.9, ui.CW, [0.34, 0.66], row_h=0.9,
             header_h=0.45, font=12, header_font=12)
    ui.quote(s, ui.ML, 6.0, ui.CW, 0.85,
             "Pista para la Actividad 7: esa métrica de CPU es la que "
             "disparará el Auto Scaling.", size=13.5)

    # ------------------------------------------------------ 15 ACT 6 Trusted Advisor
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Configurar AWS Trusted Advisor",
              "actividad 6 · integrante 3", size=28)
    ui.txt(s, ui.ML, 1.85, ui.CW, 0.35,
           "Objetivo: utilizar Trusted Advisor para identificar "
           "oportunidades de mejora en la cuenta del laboratorio.",
           size=13.5, color=ui.GRAY)
    x, y, w, h = ui.pic(s, "trusted_advisor.png", ui.ML, 2.5, w=6.3)
    ui.caption(s, x, y + h + 0.2, w, "Recomendaciones por categoría")
    sub(s, ui.ML + 6.9, 2.4, 5.1, "Categorías a revisar")
    ui.bullets(s, ui.ML + 6.9, 2.9, 5.1, 2.4, [
        "Seguridad.",
        "Rendimiento.",
        "Costos.",
        "Tolerancia a fallos.",
        "Límites de servicio.",
    ], size=14, gap=8)
    ui.quote(s, ui.ML + 6.9, 5.35, 5.1, 1.35,
             "Actividad: registrar al menos 3 recomendaciones con su "
             "categoría, riesgo y acción propuesta.", size=13.5)

    # ------------------------------------------------- 16 ACT 6 recomendaciones
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Registro de 3 recomendaciones",
              "actividad 6 · integrante 3", size=27)
    data = [
        ["Recomendación", "Categoría", "Riesgo", "Acción propuesta"],
        ["1. Revisar los permisos de los grupos de seguridad.", "Seguridad",
         "Una regla demasiado abierta podría permitir conexiones no "
         "autorizadas.",
         "Permitir únicamente los puertos necesarios."],
        ["2. Revisar la utilización de los volúmenes EBS.",
         "Optimización de costos",
         "Volúmenes sobredimensionados o sin uso generan gastos evitables.",
         "Analizar el uso y ajustar el tamaño."],
        ["3. Revisar la configuración de los grupos Auto Scaling.",
         "Rendimiento",
         "Una configuración inadecuada dificulta adaptar la capacidad a "
         "la demanda.",
         "Verificar plantilla y políticas de escalado."],
    ]
    ui.table(s, data, ui.ML, 1.85, ui.CW, [0.30, 0.15, 0.30, 0.25],
             row_h=0.85, header_h=0.44, font=10.5, header_font=11)
    ui.txt(s, ui.ML, 5.35, ui.CW, 0.35,
           "¿Por qué Trusted Advisor ayuda a mejorar una arquitectura AWS?",
           size=14.5, bold=True, color=ui.WHITE)
    ui.txt(s, ui.ML, 5.8, ui.CW, 1.0,
           "Porque analiza los recursos de la cuenta y ofrece "
           "recomendaciones para optimizar seguridad, rendimiento, costos "
           "y tolerancia a fallos: permite corregir configuraciones "
           "inadecuadas y aplicar buenas prácticas. Las comprobaciones "
           "disponibles dependen del plan de soporte.",
           size=13, color=ui.GRAY, spacing=1.2)

    # --------------------------------------------------------- 17 ACT 7
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Cómo debe responder la infraestructura a la campaña",
              "actividad 7 · oswaldo", size=25)
    ui.pic(s, "reto.png", ui.ML, 1.95, w=6.1)
    ui.caption(s, ui.ML, 5.35, 6.1, "La demanda sube y las instancias "
                                    "aumentan con ella")
    ui.quote(s, ui.ML, 5.8, 6.1, 1.1,
             "Idea central: subir la capacidad antes del pico, escalar "
             "durante la campaña y volver al mínimo al terminar (pagar "
             "solo lo que se usa).", size=12.5)
    data = [
        ["Parámetro", "Normal", "Campaña"],
        ["Mínimo", "2", "4"],
        ["Deseado", "2", "4"],
        ["Máximo", "4", "8"],
        ["Política", "CPU 60 %", "CPU 60 % + escalado programado"],
    ]
    ui.table(s, data, ui.ML + 6.6, 1.95, 5.4, [0.34, 0.24, 0.42],
             row_h=0.44, header_h=0.42, font=11.5, header_font=11.5)
    ui.txt(s, ui.ML + 6.6, 4.5, 5.4, 0.35, "Antes de la campaña",
           size=14.5, bold=True, color=ui.WHITE)
    ui.bullets(s, ui.ML + 6.6, 4.95, 5.4, 1.9, [
        "Escalado programado: mínimo de 2 a 3 o 4 instancias (tardan "
        "minutos en pasar el health check).",
        "Subir el máximo de 4 a 6 u 8 si el aumento es importante.",
        "Prueba de carga previa (JMeter o Locust) para saber cuántos "
        "usuarios soporta cada EC2.",
    ], size=12, gap=6)

    # --------------------------------------------------------- 18 ACT 7 b
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Durante y después de la campaña",
              "actividad 7 · oswaldo", size=27)
    sub(s, ui.ML, 1.9, 5.9, "Durante la campaña")
    ui.bullets(s, ui.ML, 2.4, 5.9, 3.6, [
        "Política de seguimiento de objetivo (Target Tracking): mantener "
        "la CPU en 60 %, o mejor, RequestCountPerTarget del ALB.",
        "El Auto Scaling lanza instancias desde el Launch Template y el "
        "ALB las registra al pasar el health check.",
        "Escalar hacia afuera rápido y hacia adentro lento (cooldown 300 s) "
        "para no eliminar instancias por una caída breve.",
        "Alarmas de CloudWatch (CPU, latencia, errores 5xx) con "
        "notificación por SNS al equipo.",
    ], size=13.5, gap=9)
    sub(s, ui.ML + 6.3, 1.9, 5.7, "Después de la campaña")
    ui.bullets(s, ui.ML + 6.3, 2.4, 5.7, 2.4, [
        "El Auto Scaling Group reduce la capacidad hasta el mínimo.",
        "Revisar las métricas para ajustar los valores de la próxima "
        "campaña.",
        "Pagar solo la capacidad usada durante el pico.",
    ], size=13.5, gap=9)
    ui.quote(s, ui.ML + 6.3, 5.1, 5.7, 1.6,
             "Pregunta para el equipo: ¿cómo debería responder la "
             "infraestructura si el pico dura toda la noche y no solo "
             "dos horas?", size=14)

    # --------------------------------------------------------- 19 ACT 8
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "5 mejoras adicionales a la arquitectura",
              "actividad 8 · oswaldo", size=27)
    ui.txt(s, ui.ML, 1.8, ui.CW, 0.35,
           "Las cinco mejoras con mayor impacto: disponibilidad, datos, "
           "rendimiento, seguridad y recuperación.", size=13.5,
           color=ui.GRAY)
    ui.numbered(s, ui.ML, 2.3, 5.9, 4.2, [
        "Multi-AZ: distribuir las EC2 y el ALB en al menos dos zonas de "
        "disponibilidad para sobrevivir a la caída de una.",
        "Base de datos administrada con réplica (RDS Multi-AZ): los datos "
        "dejan de ser un punto único de fallo; ElastiCache alivia consultas "
        "repetidas.",
        "CloudFront (CDN) + S3 para contenido estático: imágenes, CSS y "
        "JS salen de la caché y las EC2 reciben menos carga.",
    ], size=13.5, gap=14)
    ui.numbered(s, ui.ML + 6.1, 2.3, 5.9, 4.2, [
        "Seguridad: AWS WAF en el ALB, Security Groups mínimos, instancias "
        "en subredes privadas (solo el ALB es público), HTTPS con "
        "certificado de ACM y roles IAM en lugar de claves.",
        "Backups y recuperación: snapshots automáticos con AWS Backup, "
        "AMIs actualizadas y, si se justifica, un plan de recuperación "
        "ante desastres en otra región.",
    ], size=13.5, gap=14, start=4)
    ui.quote(s, ui.ML, 6.0, ui.CW, 0.85,
             "Cada mejora se justifica con un pilar del Well-Architected: "
             "fiabilidad, seguridad, eficiencia u optimización de costos.",
             size=13.5)

    # ------------------------------------------------------------ 20 resumen
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "Resumen: qué logramos en cada actividad", "cierre")
    data = [
        ["Actividad", "Servicio", "Qué logramos"],
        ["1 · Well-Architected", "6 pilares", "Detectar problemas y "
         "relacionarlos con buenas prácticas."],
        ["2 · Servidor web", "Amazon EC2", "Publicar una página con "
         "Security Group y User data."],
        ["3 · Fiabilidad", "EC2 redundante", "Eliminar el punto único de "
         "fallo con dos instancias."],
        ["4 · Balanceo", "Elastic Load Balancing", "Repartir el tráfico y "
         "detectar servidores caídos."],
        ["5 · Monitoreo", "Amazon CloudWatch", "Ver métricas en tiempo "
         "real y crear alarmas de CPU."],
        ["6 · Optimización", "Trusted Advisor", "Identificar y registrar "
         "recomendaciones de mejora."],
        ["7 · Escalado", "Auto Scaling", "Sumar y quitar instancias según "
         "la demanda de la campaña."],
        ["8 · Mejora", "Multi-AZ, RDS, WAF", "Proponer mejoras de "
         "disponibilidad, seguridad y costos."],
    ]
    ui.table(s, data, ui.ML, 1.85, ui.CW, [0.24, 0.24, 0.52], row_h=0.44,
             header_h=0.42, font=11.5, header_font=11.5)
    ui.txt(s, ui.ML, 6.0, ui.CW, 0.7,
           "Resultado: una arquitectura disponible, monitoreada, "
           "escalable y optimizada. Recordar eliminar todos los recursos "
           "creados al terminar el laboratorio.", size=13, color=ui.GRAY)

    # ------------------------------------------------------------- 21 cierre
    n += 1
    s = ui.new_slide(prs)
    ui.header(s, "¡Gracias!", "fin de la presentación")
    ui.pic(s, "arquitectura_final.png", 0, 1.8, h=4.6, center_x=3.4)
    ui.txt(s, ui.ML + 6.4, 2.0, 5.6, 0.4, "Actividades presentadas:",
           size=15, bold=True, color=ui.WHITE)
    ui.bullets(s, ui.ML + 6.4, 2.55, 5.6, 3.2, [
        "Actividades 1 y 2 — Manuel Antonio Garay Rivera",
        "Actividades 3 y 4 — Stev Lozano",
        "Actividades 5 y 6 — Integrante 3",
        "Actividades 7 y 8 — Oswaldo",
    ], size=14.5, gap=12)
    ui.quote(s, ui.ML + 6.4, 5.1, 5.6, 1.6,
             "Preguntas del público: ¿cuál de las 8 actividades cambió "
             "más la arquitectura y por qué?", size=14)

    for i, slide in enumerate(prs.slides, start=1):
        if i == 1:
            continue
        foot(slide, i)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    prs.save(OUT)
    print("PPT creado:", OUT, "| diapositivas:", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    build()
