export const integrantes = [
  { n: 1, nombre: "Manuel Antonio Garay Rivera", act: [1, 2] },
  { n: 2, nombre: "Stev Lozano", act: [3, 4] },
  { n: 3, nombre: "Integrante 3", act: [5, 6] },
  { n: 4, nombre: "Oswaldo", act: [7, 8] },
];

export const actividades = [
  {
    id: 1,
    area: "Arquitectura segura",
    titulo: "Los seis pilares del Well-Architected Framework",
    integrante: "Manuel Antonio Garay Rivera",
    objetivo:
      "Reconocer los principios para construir una arquitectura AWS segura, eficiente, fiable y optimizada.",
    pilares: [
      [
        "Excelencia operativa",
        "Monitorear y mejorar continuamente",
        "No alcanza con dejar corriendo: hay que medir. Se aplica con CloudWatch (métricas y alarmas) y revisando los procesos después de cada cambio.",
      ],
      [
        "Seguridad",
        "Proteger usuarios, servidores y datos",
        "Permisos mínimos en IAM, Security Groups que solo abren lo necesario (puerto 80 en el lab) y cifrado de los volúmenes EBS.",
      ],
      [
        "Fiabilidad",
        "Recuperarse de fallos",
        "Que un fallo no deje a todos sin servicio: dos instancias detrás de un Load Balancer y reemplazo automático de lo que se cae.",
      ],
      [
        "Eficiencia del rendimiento",
        "Utilizar adecuadamente los recursos",
        "El tamaño correcto en el momento correcto: instancias t3.micro en el laboratorio y Auto Scaling para subir o bajar según la demanda.",
      ],
      [
        "Optimización de costos",
        "Evitar recursos innecesarios",
        "Pagar solo lo que se usa: terminar lo que no funciona, dimensionar bien y actuar sobre las recomendaciones de Trusted Advisor.",
      ],
      [
        "Sostenibilidad",
        "Utilizar eficientemente los recursos",
        "Mismo principio que costos, pero mirando el impacto: evitar infraestructura ociosa que consume energía sin necesidad.",
      ],
    ],
    tabla: {
      cols: ["Problema", "Riesgo", "Pilar", "Solución AWS"],
      rows: [
        ["Servidor web único", "Interrupción total del servicio", "Fiabilidad", "Load Balancer + 2 instancias"],
        ["Sin monitoreo", "Detección tardía de incidentes", "Excelencia operativa", "Métricas y alarmas de CloudWatch"],
        ["Instancia sobredimensionada", "Gasto innecesario", "Optimización de costos", "Dimensionar y Auto Scaling"],
        ["Sin mecanismos de recuperación", "Prolongada fuera de servicio", "Fiabilidad", "Reemplazo automático y copias probadas"],
      ],
    },
    nota: "Acciones complementarias: permisos mínimos en IAM, reglas específicas de Security Groups, cifrado de EBS y HTTPS; retirar recursos inactivos.",
    cierre:
      "La mejora prioritaria es eliminar el punto único de fallo y detectar incidentes oportunamente; los seis pilares orientan las decisiones y se revisan con mediciones.",
    img: [
      {
        src: "/img/pilares.png",
        caption: "Los seis pilares",
        desc: "Los seis pilares del Well-Architected Framework. Cada tarjeta resume de qué se encarga el pilar; sirve para revisar con el equipo cuáles aplican al caso: por ejemplo, el servidor único toca Fiabilidad y el monitoreo toca Excelencia operativa.",
      },
    ],
  },
  {
    id: 2,
    area: "Implementación",
    titulo: "Publicar servidores según la carga de trabajo",
    integrante: "Manuel Antonio Garay Rivera",
    objetivo: "Configurar una instancia EC2 para servir una página sencilla por HTTP.",
    pasos: [
      "Abrir la región elegida y elegir EC2 → Launch instance.",
      "Nombre WEB-SERVER-01, Amazon Linux 2023 y tipo t3.micro (revisar costo y elegibilidad de la cuenta).",
      "Key pair: opcional si se usa User data; el puerto 22 no es necesario para esta práctica.",
      "Network settings: VPC y subred pública, con IP pública asignada y ruta 0.0.0.0/0 hacia el Internet Gateway.",
      "Crear SG-WEB-LAB: HTTP 80 desde 0.0.0.0/0 (SSH 22 solo desde la IP del administrador /32, si se requiere).",
      "Volumen EBS cifrado, pegar el script en Advanced details → Launch instance.",
    ],
    codigo: `#!/bin/bash
set -eu
dnf install -y httpd
cat > /var/www/html/index.html <<'HTML'
<h1>Servidor Web AWS - Grupo 01</h1>
<p>Instancia: WEB-SERVER-01</p>
<p>El servidor web está funcionando.</p>
HTML
systemctl enable --now httpd`,
    puntos: [
      "Esperar Running con Status checks 2/2 (la instalación tarda).",
      "Abrir http://IP_PUBLICA en el navegador.",
      'Comprobar el título "Servidor Web AWS – Grupo 01" y registrar capturas.',
    ],
    puntos2: [
      "Revisar la IP actual y el puerto 80 abierto en el SG.",
      "Verificar la ruta al Internet Gateway y las ACL de red.",
      "Verificar Apache: systemctl status httpd.",
      "Si User data falló: /var/log/cloud-init-output.log.",
      "Las comprobaciones de EC2 no garantizan que HTTP funcione.",
    ],
    tituloPuntos2: "Si la página no responde",
    nota: "Al terminar el laboratorio: terminar la instancia y eliminar los recursos propios (volúmenes e IPs reservadas).",
    img: [
      {
        src: "/img/ec2_launch.png",
        caption: "Configuración de la instancia",
        desc: "El formulario Launch instance con la configuración del taller: nombre WEB-SERVER-01, Amazon Linux 2023, tipo t3.micro (gratuito), VPC con subred pública y Security Group que solo abre el puerto 80. El script de User data se pega en Advanced details para que la página se publique sola al primer arranque.",
      },
      {
        src: "/img/pag_web.png",
        caption: "Página publicada en EC2",
        desc: "Resultado esperado: al abrir http://IP_PUBLICA en el navegador aparece la página con el título “Servidor Web AWS – Grupo 01”. Si no carga, revisar la IP, el puerto 80 en el Security Group y el log de User data (/var/log/cloud-init-output.log).",
      },
    ],
  },
  {
    id: 3,
    area: "Fiabilidad",
    titulo: "Asegurar la fiabilidad y alta disponibilidad",
    integrante: "Stev Lozano",
    objetivo:
      "Evitar que la aplicación dependa de un único servidor (punto único de fallo).",
    pasos: [
      "EC2 → Instances → Launch instance, nombre WEB-SERVER-02.",
      "Misma AMI (Amazon Linux 2023) y mismo tipo (t3.micro) para que los servidores sean equivalentes.",
      "Misma VPC y subred pública con IP pública asignada.",
      "Security Group: reutilizar SG-WEB-LAB (HTTP 80).",
      'User data: el mismo script, pero con el título "Servidor WEB 02 – Grupo A".',
      "Launch instance, esperar Running 2/2 y probar su IP individual.",
    ],
    puntos: [
      "Abrir la app por la IP de EC2-01 en una pestaña y por la de EC2-02 en otra.",
      "Detener (Stop) EC2-01: su IP deja de responder.",
      "EC2-02 sigue respondiendo normalmente.",
      "Conclusión: ya no hay punto único de fallo.",
    ],
    nota: "Tip: ambas instancias deben quedar con el mismo contenido y el mismo Security Group para que la demo del balanceo se vea bien.",
    pregunta: "¿Qué sucede si EC2-01 deja de funcionar? → el ALB lo marca como no saludable y el tráfico continúa por EC2-02.",
    img: [
      {
        src: "/img/diag_inicial.png",
        caption: "Arquitectura inicial",
        desc: "Punto de partida: Internet llega a una sola instancia (EC2-01) y de ahí a la aplicación. Es el punto único de fallo — si esa instancia se detiene o pierde la conexión, la aplicación deja de responder para todos los usuarios.",
      },
      {
        src: "/img/diag_propuesta.png",
        caption: "Propuesta con 2 instancias",
        desc: "Propuesta: el Load Balancer recibe todo el tráfico y lo reparte entre EC2-01 y EC2-02. Si una cae, el ALB la marca como no saludable y sigue enviando peticiones a la otra; por eso la aplicación se mantiene en línea. Ese es exactamente el ejercicio de la actividad.",
      },
    ],
  },
  {
    id: 4,
    area: "Distribución de tráfico",
    titulo: "Distribuir el tráfico: Application Load Balancer",
    integrante: "Stev Lozano",
    objetivo:
      "Comprender y configurar un ALB: punto de entrada único que recibe las peticiones y las reparte entre los servidores saludables.",
    analogia: "Analogía: es el mesero del restaurante — reparte las mesas disponibles y no sienta a nadie en una mesa caída.",
    tabla: {
      cols: ["Componente", "En palabras simples", "En el taller"],
      rows: [
        ["Load Balancer (ALB)", "Recibe el tráfico de Internet.", "Internet-facing en 2 subredes"],
        ["Listener", "Puerta de entrada: protocolo y puerto.", "HTTP en el puerto 80"],
        ["Target Group", "Lista de servidores destino.", "TG-WEB con EC2-01 y EC2-02"],
        ["Target", "Cada servidor registrado.", "Instancias EC2"],
        ["Health check", "Comprueba si el servidor responde.", 'HTTP GET a "/" cada 30 s'],
        ["DNS del ALB", "Dirección única del usuario.", "…elb.amazonaws.com"],
      ],
    },
    pasos: [
      "Target Group: EC2 → Target Groups → Create; Instances; nombre TG-WEB; HTTP 80; VPC del lab; health check \"/\"; registrar EC2-01 y EC2-02.",
      "Load Balancer: EC2 → Load Balancers → Create → Application; nombre ALB-WEB; Internet-facing; IPv4.",
      "Mapping: elegir al menos 2 subredes distintas (2 zonas de disponibilidad) para que el balanceador también sea redundante.",
      "Security Group: crear SG-ALB con HTTP 80 desde 0.0.0.0/0 (es el SG del balanceador, no el de las instancias).",
      "Listener: HTTP 80 → acción Forward hacia TG-WEB → Create load balancer. Esperar estado Active, copiar el DNS y abrir http://DNS.",
    ],
    tituloTabla2: "Si no funciona: solución de problemas",
    tabla2: {
      cols: ["Síntoma", "Causa probable", "Solución"],
      rows: [
        ["El navegador no abre el DNS del ALB", "El SG del ALB no permite el 80 o aún no está activo.", "Agregar HTTP 80 desde 0.0.0.0/0 y esperar 1-2 minutos."],
        ["Error 503 Service Unavailable", "Destinos unhealthy o falta el Forward del listener.", "Revisar Targets, health check y acción Forward a TG-WEB."],
        ["Error 400 Bad Request", "Se usa https:// pero el listener es HTTP.", "Escribir http:// delante del DNS."],
        ["Siempre responde el mismo servidor", "Ambas instancias muestran el mismo texto.", "Cambiar el index.html de un servidor (comando de la demo)."],
        ["Timeout al abrir la página", "El SG de las instancias no permite el tráfico del ALB.", "Abrir HTTP 80 en el Security Group de las instancias."],
      ],
    },
    demo: [
      "# En EC2-01",
      "echo '<h1>Servidor WEB 01 - Grupo A</h1>' | sudo tee /var/www/html/index.html",
      "# En EC2-02",
      "echo '<h1>Servidor WEB 02 - Grupo A</h1>' | sudo tee /var/www/html/index.html",
    ],
    puntos: [
      "Refrescar varias veces: alterna entre WEB 01 y WEB 02.",
      "Detener EC2-01 y seguir recargando: la app sigue en línea.",
    ],
    nota: "Regla de oro: revisar primero el estado de los targets, luego los Security Group y por último el listener.",
    img: [
      {
        src: "/img/elb_demo.png",
        caption: "Demostración: el tráfico se distribuye",
        desc: "El navegador siempre consulta la misma dirección (el DNS del ALB), pero las respuestas alternan entre el Servidor WEB 01 y el WEB 02. En la demo se refresca la página varias veces para verlo y luego se detiene EC2-01 para comprobar que la app sigue en línea.",
      },
    ],
  },
  {
    id: 5,
    area: "Monitoreo",
    titulo: "Monitorear recursos y aplicaciones en tiempo real",
    integrante: "Integrante 3",
    objetivo:
      "Supervisar el comportamiento de las instancias y detectar situaciones anormales con Amazon CloudWatch.",
    puntos: [
      "CPU y estado de las instancias.",
      "Tráfico de red y solicitudes.",
      "Estado de los destinos del Load Balancer.",
      "Alarmas configuradas.",
    ],
    tabla: {
      cols: ["Pregunta", "Respuesta"],
      rows: [
        ["¿Qué recurso presenta mayor utilización?", "La instancia EC2 con mayor porcentaje de CPU: es la que concentra más carga de procesamiento."],
        ["¿Qué ocurre cuando aumenta el tráfico?", "Aumentan las solicitudes y, con ellas, CPU, memoria y red; si la capacidad no alcanza, la aplicación se vuelve lenta."],
        ["¿Cómo sabemos que una instancia presenta problemas?", "Con las métricas de CloudWatch, las comprobaciones de estado de EC2 y el estado de los destinos del ALB: las alarmas detectan valores anormales."],
        ["¿Qué métrica sería útil para activar el escalado?", "CPUUtilization de EC2: por ejemplo, escalar cuando el uso promedio supera el 70 % durante un periodo determinado."],
      ],
    },
    nota: "Actividad: crear una alarma de CPU — si el uso supera un porcentaje durante un periodo establecido, generar una alerta. Esa métrica es la que disparará el Auto Scaling de la Actividad 7.",
    img: [
      {
        src: "/img/cloudwatch.png",
        caption: "Métricas y alarma de CPU",
        desc: "Curva de CPU de la instancia en CloudWatch durante 14 minutos: sube hasta ~80 % y la línea roja punteada es la alarma configurada al 70 %. Cuando el uso supera el umbral durante el periodo definido, CloudWatch genera la alerta — y esa misma métrica será la que dispare el Auto Scaling en la Actividad 7.",
      },
    ],
  },
  {
    id: 6,
    area: "Optimización",
    titulo: "Configurar AWS Trusted Advisor",
    integrante: "Integrante 3",
    objetivo:
      "Utilizar Trusted Advisor para identificar oportunidades de mejora en la cuenta del laboratorio.",
    puntos: ["Seguridad.", "Rendimiento.", "Costos.", "Tolerancia a fallos.", "Límites de servicio."],
    tituloPuntos: "Categorías a revisar",
    tabla: {
      cols: ["Recomendación", "Categoría", "Riesgo", "Acción propuesta"],
      rows: [
        ["1. Revisar los permisos de los grupos de seguridad.", "Seguridad", "Una regla demasiado abierta podría permitir conexiones no autorizadas.", "Permitir únicamente los puertos necesarios."],
        ["2. Revisar la utilización de los volúmenes EBS.", "Optimización de costos", "Volúmenes sobredimensionados o sin uso generan gastos evitables.", "Analizar el uso y ajustar el tamaño."],
        ["3. Revisar la configuración de los grupos Auto Scaling.", "Rendimiento", "Una configuración inadecuada dificulta adaptar la capacidad a la demanda.", "Verificar plantilla y políticas de escalado."],
      ],
    },
    preguntaResp:
      "Porque analiza los recursos de la cuenta y ofrece recomendaciones para optimizar seguridad, rendimiento, costos y tolerancia a fallos; permite corregir configuraciones inadecuadas y aplicar buenas prácticas. Las comprobaciones disponibles dependen del plan de soporte.",
    pregunta: "¿Por qué Trusted Advisor ayuda a mejorar una arquitectura AWS?",
    nota: "Actividad: registrar al menos 3 recomendaciones con su categoría, riesgo y acción propuesta.",
    img: [
      {
        src: "/img/trusted_advisor.png",
        caption: "Recomendaciones por categoría",
        desc: "Trusted Advisor resumiendo el estado de la cuenta por categoría: verde significa sin problemas y amarillo que hay sugerencias pendientes. El objetivo de la actividad es abrir estas categorías y registrar al menos 3 recomendaciones con su categoría, riesgo y acción propuesta.",
      },
    ],
  },
  {
    id: 7,
    area: "Escalado automático",
    titulo: "Cómo debe responder la infraestructura a la campaña",
    integrante: "Oswaldo",
    objetivo:
      "Planificar la capacidad antes, durante y después de una campaña de ventas con Auto Scaling.",
    tabla: {
      cols: ["Parámetro", "Normal", "Campaña"],
      rows: [
        ["Mínimo", "2", "4"],
        ["Deseado", "2", "4"],
        ["Máximo", "4", "8"],
        ["Política", "CPU 60 %", "CPU 60 % + escalado programado"],
      ],
    },
    puntos: [
      "Escalado programado: mínimo de 2 a 3 o 4 instancias (tardan minutos en pasar el health check).",
      "Subir el máximo de 4 a 6 u 8 si el aumento es importante.",
      "Prueba de carga previa (JMeter o Locust) para saber cuántos usuarios soporta cada EC2.",
    ],
    tituloPuntos: "Antes de la campaña",
    puntos2: [
      "Política de seguimiento de objetivo (Target Tracking): mantener la CPU en 60 %, o mejor, RequestCountPerTarget del ALB.",
      "El Auto Scaling lanza instancias desde el Launch Template y el ALB las registra al pasar el health check.",
      "Escalar hacia afuera rápido y hacia adentro lento (cooldown 300 s) para no eliminar instancias por una caída breve.",
      "Alarmas de CloudWatch (CPU, latencia, errores 5xx) con notificación por SNS al equipo.",
    ],
    tituloPuntos2: "Durante la campaña",
    puntos3: [
      "El Auto Scaling Group reduce la capacidad hasta el mínimo.",
      "Revisar las métricas para ajustar los valores de la próxima campaña.",
      "Pagar solo la capacidad usada durante el pico.",
    ],
    tituloPuntos3: "Después de la campaña",
    nota: "Idea central: subir la capacidad antes del pico, escalar durante la campaña y volver al mínimo al terminar (pagar solo lo que se usa).",
    pregunta: "Pregunta para el equipo: ¿cómo debería responder la infraestructura si el pico dura toda la noche y no solo dos horas?",
    img: [
      {
        src: "/img/reto.png",
        caption: "La demanda sube y las instancias aumentan con ella",
        desc: "La curva blanca es la cantidad de usuarios y la línea verde el número de instancias EC2. La banda gris es el fin de semana de campaña: la capacidad sube por escalones justo antes del pico (de 2 a 4, o hasta 8 en campaña) y vuelve al mínimo al terminar; así solo se paga por lo que se usa.",
      },
      {
        src: "/img/antes_despues.png",
        caption: "Antes: una sola instancia · Después: ALB + Auto Scaling",
        desc: "A la izquierda la arquitectura original: Internet llega a una EC2 única que sirve la aplicación, con 1 punto de fallo si esa instancia se cae. A la derecha la propuesta: el ALB reparte el tráfico entre EC2-01 y EC2-02, y Auto Scaling + CloudWatch añaden o quitan instancias según la demanda, de modo que una caída no deja el servicio fuera.",
      },
      {
        src: "/img/autoscaling.png",
        caption: "Cómo se reparte y escala la carga",
        desc: "Los usuarios llegan al Load Balancer, que reparte las peticiones entre las EC2 del Auto Scaling Group. Si la demanda crece, el grupo lanza nuevas EC2 “según la demanda” desde el Launch Template y el ALB las registra al pasar el health check; cuando la demanda baja, las termina. Así se respeta el mínimo y el máximo configurados (2–4 normal, 4–8 en campaña) con la meta de CPU del 60 %.",
      },
    ],
  },
  {
    id: 8,
    area: "Mejoras",
    titulo: "5 mejoras adicionales a la arquitectura",
    integrante: "Oswaldo",
    objetivo:
      "Proponer las cinco mejoras con mayor impacto: disponibilidad, datos, rendimiento, seguridad y recuperación.",
    pasos: [
      "Multi-AZ: distribuir las EC2 y el ALB en al menos dos zonas de disponibilidad para sobrevivir a la caída de una.",
      "Base de datos administrada con réplica (RDS Multi-AZ): los datos dejan de ser un punto único de fallo; ElasticCache alivia consultas repetidas.",
      "CloudFront (CDN) + S3 para contenido estático: imágenes, CSS y JS salen de la caché y las EC2 reciben menos carga.",
      "Seguridad: AWS WAF en el ALB, Security Groups mínimos, instancias en subredes privadas (solo el ALB es público), HTTPS con certificado de ACM y roles IAM en lugar de claves.",
      "Backups y recuperación: snapshots automáticos con AWS Backup, AMIs actualizadas y, si se justifica, un plan de recuperación ante desastres en otra región.",
    ],
    tituloPasos: "Las cinco mejoras con mayor impacto",
    nota: "Cada mejora se justifica con un pilar del Well-Architected: fiabilidad, seguridad, eficiencia u optimización de costos.",
    img: [
      {
        src: "/img/arquitectura_final.png",
        caption: "Arquitectura final propuesta",
        desc: "El reto era resolver disponibilidad, datos, rendimiento y seguridad con los servicios del taller; esta es la propuesta de cierre: usuarios → Internet → Application Load Balancer → dos instancias EC2 dentro de un Auto Scaling Group, con CloudWatch monitoreando y alarmas avisando. Cada componente corresponde a un pilar del Well-Architected (fiabilidad, seguridad, eficiencia y costos). Buen momento para preguntar al grupo qué agregarían ellos.",
      },
    ],
  },
];
