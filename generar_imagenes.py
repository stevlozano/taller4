#!/usr/bin/env python3
"""Genera los diagramas en PNG (fondo negro, lineas y texto blancos) para el PPT."""
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "img")
os.makedirs(OUT, exist_ok=True)

WHITE = "white"
GRAY = "#9a9a9a"


def newfig(w, h, xlim=100.0):
    H = xlim * h / w
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor("black")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("black")
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax, H


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, facecolor="black", dpi=200)
    plt.close(fig)
    print("ok", path)


def rbox(ax, x, y, w, h, label="", sub=None, fs=13, sub_fs=9, ec=WHITE,
         fc="none", lw=1.4, rounding=1.5, tcolor=WHITE, sub_color=GRAY,
         bold=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%s" % rounding,
                                linewidth=lw, edgecolor=ec, facecolor=fc,
                                mutation_aspect=1))
    if sub:
        ax.text(x + w / 2, y + h * 0.63, label, ha="center", va="center",
                color=tcolor, fontsize=fs,
                fontweight="bold" if bold else "normal")
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center",
                color=sub_color, fontsize=sub_fs)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                color=tcolor, fontsize=fs,
                fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, color=WHITE, lw=1.4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=14))


def hline(ax, x1, x2, y, color="#4a4a4a", lw=1.0, ls="-"):
    ax.plot([x1, x2], [y, y], color=color, lw=lw, ls=ls)


def portada():
    fig, ax, H = newfig(7, 5.5)
    random.seed(7)
    pts = [(random.uniform(6, 94), random.uniform(6, H - 6)) for _ in range(34)]
    for i, (x1, y1) in enumerate(pts):
        for (x2, y2) in pts[i + 1:]:
            d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            if d < 26:
                ax.plot([x1, x2], [y1, y2], color=WHITE, lw=0.5, alpha=0.35)
    for i, (x, y) in enumerate(pts):
        r = 1.6 if i % 7 == 0 else 0.8
        ax.add_patch(Circle((x, y), r, facecolor="white", edgecolor="none",
                            alpha=0.9 if i % 7 == 0 else 0.6))
        if i % 7 == 0:
            ax.add_patch(Circle((x, y), r + 2.2, facecolor="none",
                                edgecolor=WHITE, lw=0.8, alpha=0.7))
    save(fig, "portada.png")


def diag_inicial():
    fig, ax, H = newfig(6, 5.2)
    rbox(ax, 25, 69.5, 50, 11, "INTERNET", fs=13)
    arrow(ax, 50, 69.5, 50, 57)
    rbox(ax, 28, 44, 44, 13, "EC2-01", sub="Servidor único", fs=14)
    arrow(ax, 50, 44, 50, 31)
    rbox(ax, 25, 18, 50, 13, "APLICACIÓN", fs=13)
    hline(ax, 25, 75, 13, color="#4a4a4a", lw=0.8)
    ax.text(50, 8.5, "PUNTO ÚNICO DE FALLO", ha="center", va="center",
            color=WHITE, fontsize=11, fontweight="bold")
    ax.text(50, 3.5, "Si EC2-01 deja de funcionar, la aplicación cae",
            ha="center", va="center", color=GRAY, fontsize=9)
    save(fig, "diag_inicial.png")


def diag_propuesta():
    fig, ax, H = newfig(6.4, 5.4)
    rbox(ax, 27, 70, 46, 10, "INTERNET", fs=12)
    arrow(ax, 50, 70, 50, 62)
    rbox(ax, 15, 50, 70, 12, "LOAD BALANCER", sub="Elastic Load Balancing", fs=13)
    arrow(ax, 35, 50, 24, 41)
    arrow(ax, 65, 50, 76, 41)
    rbox(ax, 6, 28, 36, 13, "EC2-01", fs=13)
    rbox(ax, 58, 28, 36, 13, "EC2-02", fs=13)
    arrow(ax, 24, 28, 40, 19)
    arrow(ax, 76, 28, 60, 19)
    rbox(ax, 25, 6, 50, 13, "APLICACIÓN", fs=13)
    save(fig, "diag_propuesta.png")


def pilares():
    fig, ax, H = newfig(10, 4.6)
    datos = [
        ("Excelencia operativa", "Monitorear y mejorar\ncontinuamente"),
        ("Seguridad", "Proteger usuarios,\nservidores y datos"),
        ("Fiabilidad", "Recuperarse\nde fallos"),
        ("Eficiencia del rendimiento", "Utilizar adecuadamente\nlos recursos"),
        ("Optimización de costos", "Evitar recursos\ninnecesarios"),
        ("Sostenibilidad", "Utilizar eficientemente\nlos recursos"),
    ]
    gap, m = 3.0, 2.0
    bw = (100 - 2 * m - 2 * gap) / 3
    bh = (H - 6 - 4) / 2
    for i, (t, s) in enumerate(datos):
        c, r = i % 3, i // 3
        x = m + c * (bw + gap)
        y = H - 3 - (r + 1) * bh - r * 4
        rbox(ax, x, y, bw, bh, "", rounding=1.2)
        ax.text(x + bw / 2, y + bh * 0.66, t, ha="center", va="center",
                color=WHITE, fontsize=11.5, fontweight="bold")
        ax.text(x + bw / 2, y + bh * 0.30, s, ha="center", va="center",
                color=GRAY, fontsize=9)
    save(fig, "pilares.png")


def ec2_launch():
    fig, ax, H = newfig(8, 5.0)
    ax.add_patch(FancyBboxPatch((3, 3), 94, H - 6,
                                boxstyle="round,pad=0,rounding_size=2",
                                linewidth=1.4, edgecolor=WHITE,
                                facecolor="#0d0d0d", mutation_aspect=1))
    ax.text(7, H - 11, "Launch instance", color=WHITE, fontsize=15,
            fontweight="bold", ha="left", va="center")
    rbox(ax, 72, H - 15, 19, 8, "Launch", fs=11, fc=WHITE, ec=WHITE,
         tcolor="black", rounding=1.2)
    hline(ax, 7, 93, H - 19, color="#3f3f3f", lw=1.0)
    filas = [
        ("Nombre", "WEB-SERVER-01"),
        ("AMI", "Amazon Linux 2023"),
        ("Tipo de instancia", "t3.micro  (capa gratuita)"),
        ("Red", "VPC + Security Group"),
        ("Reglas", "HTTP  ·  Puerto 80  ·  0.0.0.0/0"),
    ]
    y = 37
    for etiqueta, valor in filas:
        ax.text(7, y, etiqueta, color=GRAY, fontsize=10, ha="left", va="center")
        ax.text(40, y, valor, color=WHITE, fontsize=11, ha="left",
                va="center", fontweight="bold")
        if y > 8:
            hline(ax, 7, 93, y - 5, color="#2e2e2e", lw=0.8)
        y -= 7.2
    save(fig, "ec2_launch.png")


def pag_web():
    fig, ax, H = newfig(7, 4.2)
    ax.add_patch(FancyBboxPatch((3, 3), 94, H - 6,
                                boxstyle="round,pad=0,rounding_size=2",
                                linewidth=1.4, edgecolor=WHITE,
                                facecolor="#0d0d0d", mutation_aspect=1))
    for dx in (8, 12.5, 17):
        ax.add_patch(Circle((dx, H - 9.5), 1.3, facecolor="#6a6a6a",
                            edgecolor="none"))
    ax.add_patch(FancyBboxPatch((23, H - 13), 68, 7,
                                boxstyle="round,pad=0,rounding_size=1.2",
                                linewidth=0.9, edgecolor="#5a5a5a",
                                facecolor="#161616", mutation_aspect=1))
    ax.text(25, H - 9.5, "http://<ip-publica>/", color=GRAY, fontsize=9.5,
            ha="left", va="center")
    hline(ax, 3, 97, H - 17, color="#3f3f3f", lw=1.0)
    ax.text(50, H * 0.46, "Servidor Web AWS - Grupo 01", color=WHITE,
            fontsize=19, fontweight="bold", ha="center", va="center")
    ax.text(50, H * 0.30, "HTTP 200  ·  funcionando correctamente", color=GRAY,
            fontsize=11, ha="center", va="center")
    save(fig, "pag_web.png")


def elb_demo():
    fig, ax, H = newfig(8, 5.0)
    rbox(ax, 15, H - 14, 70, 10, "DNS del Load Balancer",
         sub="mi-app-<id>.elb.amazonaws.com", fs=12, sub_fs=9)
    arrow(ax, 50, H - 14, 50, H - 23)
    arrow(ax, 50, H - 23, 25, H - 31)
    arrow(ax, 50, H - 23, 75, H - 31)
    rbox(ax, 6, H - 46, 38, 15, "Servidor WEB 01",
         sub="Grupo A  ·  solicitudes 1, 3, 5", fs=12, sub_fs=9)
    rbox(ax, 56, H - 46, 38, 15, "Servidor WEB 02",
         sub="Grupo A  ·  solicitudes 2, 4, 6", fs=12, sub_fs=9)
    hline(ax, 8, 92, 13, color="#3f3f3f", lw=0.8)
    ax.text(50, 7.5, "Al refrescar el navegador, las respuestas alternan",
            ha="center", va="center", color=WHITE, fontsize=10.5)
    ax.text(50, 2.5, "entre los dos servidores", ha="center", va="center",
            color=WHITE, fontsize=10.5)
    save(fig, "elb_demo.png")


def cloudwatch():
    fig, ax, H = newfig(8, 5.0)
    ax.text(3, H - 4, "Amazon CloudWatch", color=WHITE, fontsize=13,
            fontweight="bold", ha="left", va="center")
    tiles = [("CPU", "42 %"), ("Red", "1.2 MB/s"), ("Destinos ALB", "2 / 2")]
    tw, gap, m = 30.0, 3.5, 3.0
    for i, (t, v) in enumerate(tiles):
        x = m + i * (tw + gap)
        rbox(ax, x, H - 24, tw, 13, t, sub=v, fs=11, sub_fs=13,
             sub_color=WHITE, rounding=1.2)
    axc = fig.add_axes([(m + 4) / 100, 4 / H, (100 - 2 * m - 4) / 100, (H - 33) / H])
    axc.set_facecolor("black")
    xs = list(range(15))
    cpu = [31, 34, 33, 38, 41, 39, 45, 52, 61, 74, 83, 79, 66, 55, 47]
    axc.plot(xs, cpu, color=WHITE, lw=1.8)
    axc.axhline(70, color="#ff5f5f", lw=1.2, ls="--")
    axc.text(14.4, 72, "Alarma CPU > 70%", color="#ff5f5f", fontsize=8.5,
             ha="right", va="bottom")
    axc.set_ylim(0, 100)
    axc.set_xlim(0, 14)
    axc.tick_params(colors=GRAY, labelsize=7.5)
    for s in axc.spines.values():
        s.set_color("#4a4a4a")
    axc.set_ylabel("CPU %", color=GRAY, fontsize=8)
    axc.grid(color="#242424", lw=0.6)
    save(fig, "cloudwatch.png")


def trusted_advisor():
    fig, ax, H = newfig(8, 4.4)
    ax.add_patch(FancyBboxPatch((3, 3), 94, H - 6,
                                boxstyle="round,pad=0,rounding_size=2",
                                linewidth=1.4, edgecolor=WHITE,
                                facecolor="#0d0d0d", mutation_aspect=1))
    ax.text(7, H - 9, "AWS Trusted Advisor", color=WHITE, fontsize=14,
            fontweight="bold", ha="left", va="center")
    hline(ax, 7, 93, H - 14, color="#3f3f3f", lw=1.0)
    items = [("Seguridad", "ok", "Revisar reglas de acceso"),
             ("Rendimiento", "!", "Sugerencias disponibles"),
             ("Costos", "ok", "Optimizar recursos"),
             ("Tolerancia a fallos", "!", "Verificar respaldo"),
             ("Límites de servicio", "ok", "Dentro del límite")]
    y = H - 22
    for nombre, estado, nota in items:
        if estado == "ok":
            ax.add_patch(Rectangle((8, y - 2.4), 5, 5, facecolor="#1f7a1f",
                                   edgecolor="none"))
            ax.text(10.5, y, "v", color=WHITE, fontsize=9, ha="center",
                    va="center", fontweight="bold")
        else:
            ax.add_patch(Rectangle((8, y - 2.4), 5, 5, facecolor="#a86a00",
                                   edgecolor="none"))
            ax.text(10.5, y, "!", color=WHITE, fontsize=9, ha="center",
                    va="center", fontweight="bold")
        ax.text(17, y, nombre, color=WHITE, fontsize=11, ha="left",
                va="center", fontweight="bold")
        ax.text(45, y, nota, color=GRAY, fontsize=9.5, ha="left", va="center")
        y -= 6.4
    save(fig, "trusted_advisor.png")


def autoscaling():
    fig, ax, H = newfig(6.5, 6.2)
    rbox(ax, 30, H - 11, 40, 8, "USUARIOS", fs=12)
    arrow(ax, 50, H - 11, 50, H - 20)
    rbox(ax, 15, H - 31, 70, 11, "LOAD BALANCER", fs=13)
    arrow(ax, 35, H - 31, 32, H - 41)
    arrow(ax, 65, H - 31, 68, H - 41)
    rbox(ax, 14, H - 53, 33, 12, "EC2", fs=13)
    rbox(ax, 53, H - 53, 33, 12, "EC2", fs=13)
    arrow(ax, 32, H - 53, 44, H - 64)
    arrow(ax, 68, H - 53, 56, H - 64)
    rbox(ax, 18, H - 75, 64, 11, "AUTO SCALING GROUP", fs=13)
    arrow(ax, 50, H - 75, 50, 10.5)
    rbox(ax, 15, 0.5, 70, 10, "NUEVAS EC2", sub="según la demanda", fs=13)
    save(fig, "autoscaling.png")


def antes_despues():
    fig, ax, H = newfig(10, 6.2)
    ax.plot([50, 50], [3, H - 7], color="#3f3f3f", lw=1.2, ls="--")
    ax.text(25, H - 4, "ANTES", ha="center", va="center", color=WHITE,
            fontsize=13, fontweight="bold")
    ax.text(75, H - 4, "DESPUÉS", ha="center", va="center", color=WHITE,
            fontsize=13, fontweight="bold")
    rbox(ax, 8, 47, 34, 9, "INTERNET", fs=11)
    arrow(ax, 25, 47, 25, 41)
    rbox(ax, 8, 31, 34, 10, "EC2", sub="única instancia", fs=12)
    arrow(ax, 25, 31, 25, 25)
    rbox(ax, 8, 15, 34, 10, "APLICACIÓN", fs=11)
    ax.text(25, 7, "1 punto de fallo", ha="center", va="center", color=GRAY,
            fontsize=10.5)
    rbox(ax, 63, 47, 26, 9, "INTERNET", fs=10)
    arrow(ax, 76, 47, 76, 41)
    rbox(ax, 58, 31, 36, 10, "ALB", sub="Load Balancer", fs=12, sub_fs=8.5)
    arrow(ax, 66, 31, 63, 25)
    arrow(ax, 86, 31, 87, 25)
    rbox(ax, 52, 16, 22, 9, "EC2-01", fs=11)
    rbox(ax, 76, 16, 22, 9, "EC2-02", fs=11)
    arrow(ax, 63, 16, 68, 12)
    arrow(ax, 87, 16, 82, 12)
    rbox(ax, 52, 4, 46, 8, "AUTO SCALING  +  CLOUDWATCH", fs=10)
    save(fig, "antes_despues.png")


def reto():
    fig, ax, H = newfig(8, 4.4)
    ax.text(3, H - 4, "Campaña de ventas: demanda e instancias",
            color=WHITE, fontsize=12.5, fontweight="bold", ha="left",
            va="center")
    axc = fig.add_axes([0.11, 0.14, 0.84, 0.64])
    axc.set_facecolor("black")
    xs = list(range(13))
    usuarios = [20, 22, 25, 30, 34, 40, 62, 88, 96, 92, 70, 45, 30]
    instancias = [2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 3, 2, 2]
    axc.plot(xs, usuarios, color=WHITE, lw=2.0, label="Usuarios")
    axc.step(xs, [i * 24 for i in instancias], color="#7fd47f", lw=1.6,
             where="mid", label="Instancias EC2")
    axc.axvspan(5.5, 10.5, color="#ffffff", alpha=0.06)
    axc.text(8, 6, "fin de semana de campaña", color=GRAY, fontsize=8.5,
             ha="center")
    axc.set_ylim(0, 110)
    axc.set_xlim(0, 12)
    axc.tick_params(colors=GRAY, labelsize=7.5)
    for s in axc.spines.values():
        s.set_color("#4a4a4a")
    axc.grid(color="#242424", lw=0.6)
    leg = axc.legend(facecolor="black", edgecolor="#5a5a5a", fontsize=8,
                     loc="upper left")
    for t in leg.get_texts():
        t.set_color(WHITE)
    save(fig, "reto.png")


def arquitectura_final():
    fig, ax, H = newfig(6.4, 7.0)
    rbox(ax, 32, 99.4, 36, 7, "USUARIOS", fs=11)
    arrow(ax, 50, 99.4, 50, 93.8)
    rbox(ax, 30, 85.2, 40, 8.5, "INTERNET", fs=11)
    arrow(ax, 50, 85.2, 50, 79.6)
    rbox(ax, 15, 68.6, 70, 11, "APPLICATION LB", sub="Elastic Load Balancing",
         fs=12, sub_fs=8.5)
    arrow(ax, 34, 68.6, 26, 63)
    arrow(ax, 66, 68.6, 74, 63)
    rbox(ax, 6, 51, 40, 12, "EC2-01", fs=12)
    rbox(ax, 54, 51, 40, 12, "EC2-02", fs=12)
    arrow(ax, 26, 51, 42, 45.3)
    arrow(ax, 74, 51, 58, 45.3)
    rbox(ax, 18, 34.3, 64, 11, "AUTO SCALING", sub="min 2 / max 4", fs=12,
         sub_fs=8.5)
    arrow(ax, 50, 34.3, 50, 28.7)
    rbox(ax, 22, 17.7, 56, 11, "CLOUDWATCH", sub="métricas y alarmas", fs=12,
         sub_fs=8.5)
    arrow(ax, 50, 17.7, 50, 12)
    rbox(ax, 15, 1, 70, 11, "ALARMAS / MONITOREO", fs=11.5)
    save(fig, "arquitectura_final.png")


if __name__ == "__main__":
    portada()
    diag_inicial()
    diag_propuesta()
    pilares()
    ec2_launch()
    pag_web()
    elb_demo()
    cloudwatch()
    trusted_advisor()
    autoscaling()
    antes_despues()
    reto()
    arquitectura_final()
    print("Imagenes generadas en", OUT)
