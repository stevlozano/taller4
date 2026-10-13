# taller4

Sitio de presentación del **Taller 4 — Arquitectura AWS segura, disponible y escalable**.

Las 8 actividades del taller, una por ruta:

| Ruta | Actividad | Integrante |
|------|-----------|------------|
| `/actividades/1` | Los seis pilares del Well-Architected Framework | Manuel Antonio Garay Rivera |
| `/actividades/2` | Publicar servidores según la carga de trabajo | Manuel Antonio Garay Rivera |
| `/actividades/3` | Asegurar la fiabilidad y alta disponibilidad | Stev Lozano |
| `/actividades/4` | Distribuir el tráfico: Application Load Balancer | Stev Lozano |
| `/actividades/5` | Monitorear recursos y aplicaciones en tiempo real | Integrante 3 |
| `/actividades/6` | Configurar AWS Trusted Advisor | Integrante 3 |
| `/actividades/7` | Cómo debe responder la infraestructura a la campaña | Oswaldo |
| `/actividades/8` | 5 mejoras adicionales a la arquitectura | Oswaldo |

## Stack

- [Next.js 15](https://nextjs.org) (App Router) + React 19
- [HeroUI v3](https://heroui.com) (tablas ordenables) + Tailwind CSS v4
- Tipografía **Manrope** e iconos **Material Symbols Rounded** (Google), auto-hospedados

## Desarrollo

```bash
npm install
npm run dev        # http://localhost:3000
```

## Producción

```bash
npm run build
npm start
```

## Estructura

```
app/                  # páginas (portada + /actividades/[id])
components/           # DataTable (HeroUI)
data/actividades.js   # contenido de las 8 actividades
public/img/           # diagramas
public/fonts/         # Material Symbols Rounded
```
