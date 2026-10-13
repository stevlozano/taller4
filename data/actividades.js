export const integrantes = [
  { n: 1, nombre: "Manuel Antonio Garay Rivera", act: [1, 2] },
  { n: 2, nombre: "Stev Lozano", act: [3, 4] },
  { n: 3, nombre: "Alejandro", act: [5, 6] },
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
        caption: "Esquema: qué vamos a configurar",
        desc: "Antes de tocar la consola, el resumen de lo que se va a montar: nombre WEB-SERVER-01, Amazon Linux 2023, tipo t3.micro (gratis), VPC con subred pública y Security Group que solo abre el puerto 80. El script de User data se pega en Advanced details para que la página se publique sola al primer arranque.",
      },
      {
        src: "/img/garay1.png",
        caption: "1. Buscar EC2 en la consola",
        desc: "En la barra superior de la consola de AWS se escribe EC2 y se elige el servicio: “Servidores virtuales en la nube”. También se puede entrar por Todos los servicios.",
      },
      {
        src: "/img/garay2.png",
        caption: "2. Panel de EC2",
        desc: "Pantalla inicial de EC2 en la región us-east-2 (Ohio). El bloque “Lanzar la instancia” es el punto de partida; a la derecha se ve el costo del plan gratuito (créditos restantes) — conviene revisarlo antes de crear recursos.",
      },
      {
        src: "/img/garay3.png",
        caption: "3. Formulario Launch an instance",
        desc: "El formulario de lanzamiento. Aquí se elige el sistema operativo (Amazon Linux 2023, marcado como Free tier eligible) y el tipo de instancia (t3.micro). El panel de la derecha (Summary) resume AMI, tipo, firewall y almacenamiento antes de lanzar.",
      },
      {
        src: "/img/garay4.png",
        caption: "4. Nombre y sistema operativo",
        desc: "En Name and tags se escribe el nombre de la instancia y en Application and OS Images se confirma el SO elegido. Ojo: si se cambia el SO (en esta captura se ve Windows Server), el resto del taller —el script de User data— no aplica; para la práctica web hay que dejar Amazon Linux.",
      },
      {
        src: "/img/garay5.png",
        caption: "5. Crear el par de claves",
        desc: "Modal “Crear par de claves”: nombre clave_test, tipo RSA y formato .pem (para OpenSSH). El archivo se descarga automáticamente y hay que guardarlo en un lugar seguro: es la única forma de conectarse por SSH a la instancia.",
      },
      {
        src: "/img/garay6.png",
        caption: "6. Clave y configuración de red",
        desc: "Se selecciona el par de claves creado y se revisa Configuraciones de red: VPC por defecto, IP pública habilitada y un grupo de seguridad (launch-wizard-1) con RDP abierto a 0.0.0.0/0. La advertencia amarilla recuerda que 0.0.0./0 permite el acceso desde cualquier IP: para el taller web tocaría abrir HTTP 80 y acotar SSH a la IP del administrador.",
      },
      {
        src: "/img/garay7.png",
        caption: "7. Primera instancia en ejecución",
        desc: "Resultado en Instances: la instancia “test” aparece “En ejecución” con comprobación 3/3, tipo t3.micro en us-east-2c y su DNS/IP público (3.15.205.7). Con esa IP se prueba el acceso individual de la instancia.",
      },
      {
        src: "/img/garay8.png",
        caption: "8. La segunda instancia arranca",
        desc: "Se repite el lanzamiento para la segunda instancia (“test2”): aparece en la lista junto a la primera, todavía “Inicializando” (las comprobaciones tardan unos minutos). Las dos quedan en zonas de disponibilidad distintas (us-east-2a y us-east-2c).",
      },
      {
        src: "/img/garay9.png",
        caption: "9. Detalles de las dos instancias",
        desc: "Columna Details de la tabla: “test2” corre Linux/UNIX y “test” corre Windows; cada una tiene su IP pública y su par de claves (clavetest2 y clave_test). Al desplazar la tabla se ven también la hora de lanzamiento y el estado de administración.",
      },
      {
        src: "/img/pag_web.png",
        caption: "Resultado esperado",
        desc: "Al abrir http://IP_PUBLICA en el navegador debe aparecer la página con el título “Servidor Web AWS – Grupo 01”. Si no carga, revisar la IP, el puerto 80 en el Security Group y el log de User data (/var/log/cloud-init-output.log).",
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
    intro:
      "Partimos de WEB-SERVER-01, la instancia que quedó publicada en la Actividad 2. El objetivo es crear un segundo servidor idéntico para que, si uno cae, la aplicación siga viva en el otro.",
    pasos: [
      "EC2 → Instances → Launch instance, nombre WEB-SERVER-02.",
      "Misma AMI (Amazon Linux 2023), mismo tipo (t3.micro), misma VPC y subred pública con IP pública.",
      "Security Group: reutilizar SG-WEB-LAB (HTTP 80).",
      'User data: el mismo script de la Actividad 2, cambiando el título por <h1>Servidor WEB 02 – Grupo A</h1>.',
      "Launch instance, esperar Running 2/2 y probar http://IP_DE_EC2_02 directamente.",
    ],
    puntos: [
      "Pestaña 1: http://IP_DE_EC2_01 → responde. Pestaña 2: http://IP_DE_EC2_02 → responde con “Servidor WEB 02”.",
      "Detener (Stop) EC2-01 → su IP deja de responder; la app en EC2-02 sigue respondiendo igual.",
      "Volver a dar Start a EC2-01 (la necesita la Actividad 4).",
    ],
    tituloPuntos: "Verificación",
    nota: "Conclusión: la aplicación ya no depende de un servidor — si uno cae, la otra instancia sigue sirviendo. Que el usuario no note la falla se resuelve en la Actividad 4 con el Load Balancer, que redirige el tráfico solo. Tip: ambas instancias deben quedar con el mismo contenido y el mismo Security Group para que la demo del balanceo se vea bien.",
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
    integrante: "Alejandro",
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
        caption: "Esquema: métricas y alarma de CPU",
        desc: "Curva de CPU de la instancia en CloudWatch durante 14 minutos: sube hasta ~80 % y la línea roja punteada es la alarma configurada al 70 %. Cuando el uso supera el umbral durante el periodo definido, CloudWatch genera la alerta — y esa misma métrica será la que dispare el Auto Scaling en la Actividad 7.",
      },
      {
        src: "/img/alejandro1.png",
        caption: "La alarma creada en la consola",
        desc: "La actividad hecha en la cuenta real: la alarma Alarma-CPU-EC2 dispara si CPUUtilization > 80 durante 1 punto de datos en 5 minutos, con la descripción “Detectar uso de CPU superior al 80 % durante un periodo de 5 minutos” y vinculada a la instancia i-0194aca0c0d198095. El estado “Datos insuficientes” es normal recién creada: CloudWatch tarda unos minutos en tener métricas de la instancia.",
      },
    ],
  },
  {
    id: 6,
    area: "Optimización",
    titulo: "Configurar AWS Trusted Advisor",
    integrante: "Alejandro",
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
        caption: "Esquema: recomendaciones por categoría",
        desc: "Trusted Advisor resumiendo el estado de la cuenta por categoría: verde significa sin problemas y amarillo que hay sugerencias pendientes. El objetivo de la actividad es abrir estas categorías y registrar al menos 3 recomendaciones con su categoría, riesgo y acción propuesta.",
      },
      {
        src: "/img/alejandro2.png",
        caption: "Trusted Advisor en la consola real",
        desc: "La pantalla Recomendaciones de Trusted Advisor en la cuenta del taller: el menú lateral lista las cinco categorías (costos, rendimiento, seguridad, tolerancia a errores y cuotas de servicio) y el resumen muestra 0 acciones recomendadas. El aviso azul explica por qué: con el plan de soporte Basic solo hay comprobaciones básicas; para desbloquear todas las comprobaciones AWS pide actualizar el plan. Igual sirve para el ejercicio: abrir cada categoría y registrar lo que aparezca.",
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
