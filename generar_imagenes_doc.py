#!/usr/bin/env python3
"""Diagramas en PNG con fondo blanco (texto negro) para el documento DOCX."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "img_doc")
os.makedirs(OUT, exist_ok=True)

FG = "black"
SUB = "#555555"
GRID = "#999999"


def newfig(w, h, xlim=100.0):
    H = xlim * h / w
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("white")
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax, H


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, facecolor="white", dpi=200)
    plt.close(fig)
    print("ok", path)


def rbox(ax, x, y, w, h, label="", sub=None, fs=13, sub_fs=9, ec=FG,
         fc="white", lw=1.4, rounding=1.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%s" % rounding,
                                linewidth=lw, edgecolor=ec, facecolor=fc,
                                mutation_aspect=1))
    if sub:
        ax.text(x + w / 2, y + h * 0.63, label, ha="center", va="center",
                color=FG, fontsize=fs, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center",
                color=SUB, fontsize=sub_fs)
    else:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                color=FG, fontsize=fs, fontweight="bold")


def arrow(ax, x1, y1, x2, y2, color=FG, lw=1.4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=14))


def hline(ax, x1, x2, y, color=GRID, lw=1.0, ls="-"):
    ax.plot([x1, x2], [y, y], color=color, lw=lw, ls=ls)


def diag_inicial():
    fig, ax, H = newfig(6, 5.0)
    rbox(ax, 10, H - 15, 80, 11, "INTERNET", fs=13)
    arrow(ax, 50, H - 15, 50, H - 28)
    rbox(ax, 18, H - 41, 64, 13, "EC2-01", sub="Servidor único", fs=14)
    arrow(ax, 50, H - 41, 50, H - 54)
    rbox(ax, 10, H - 67, 80, 13, "APLICACIÓN", fs=13)
    hline(ax, 12, 88, 11, color=GRID, lw=0.9)
    ax.text(50, 7, "PUNTO ÚNICO DE FALLO", ha="center", va="center",
            color=FG, fontsize=11, fontweight="bold")
    ax.text(50, 2.5, "Si EC2-01 falla, la aplicación deja de estar disponible",
            ha="center", va="center", color=SUB, fontsize=9.5)
    save(fig, "doc_diag_inicial.png")


def diag_propuesta():
    fig, ax, H = newfig(6.4, 5.4)
    rbox(ax, 27, H - 15, 46, 10, "INTERNET", fs=12)
    arrow(ax, 50, H - 15, 50, H - 26)
    rbox(ax, 13, H - 38, 74, 12, "LOAD BALANCER (ALB)",
         sub="Elastic Load Balancing", fs=13)
    arrow(ax, 33, H - 38, 24, H - 50)
    arrow(ax, 67, H - 38, 76, H - 50)
    rbox(ax, 5, H - 63, 38, 13, "EC2-01", fs=13)
    rbox(ax, 57, H - 63, 38, 13, "EC2-02", fs=13)
    arrow(ax, 24, H - 63, 40, H - 74)
    arrow(ax, 76, H - 63, 60, H - 74)
    rbox(ax, 25, H - 87, 50, 13, "APLICACIÓN", fs=13)
    save(fig, "doc_diag_propuesta.png")


def elb_demo():
    fig, ax, H = newfig(8, 5.0)
    rbox(ax, 14, H - 14, 72, 10, "DNS DEL LOAD BALANCER",
         sub="http://alb-web-123.us-east-1.elb.amazonaws.com", fs=12,
         sub_fs=9)
    arrow(ax, 50, H - 14, 50, H - 23)
    arrow(ax, 50, H - 23, 25, H - 31)
    arrow(ax, 50, H - 23, 75, H - 31)
    rbox(ax, 6, H - 46, 38, 15, "Servidor WEB 01",
         sub="Grupo A  ·  solicitudes 1, 3, 5", fs=12, sub_fs=9)
    rbox(ax, 56, H - 46, 38, 15, "Servidor WEB 02",
         sub="Grupo A  ·  solicitudes 2, 4, 6", fs=12, sub_fs=9)
    hline(ax, 8, 92, 13, color=GRID, lw=0.9)
    ax.text(50, 7.5, "Al refrescar el navegador, las respuestas alternan",
            ha="center", va="center", color=FG, fontsize=10.5)
    ax.text(50, 2.5, "entre los dos servidores", ha="center", va="center",
            color=FG, fontsize=10.5)
    save(fig, "doc_elb_demo.png")


if __name__ == "__main__":
    diag_inicial()
    diag_propuesta()
    elb_demo()
    print("Imágenes de documento generadas en", OUT)
