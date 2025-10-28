🧠 Object Detection con Alerta Progresiva

Detección de objetos en tiempo real con advertencias visuales y sonoras dinámicas según la cercanía.

📘 Descripción General

Este proyecto implementa un sistema de detección de objetos en tiempo real utilizando el modelo EfficientDet Lite0 de MediaPipe.
Además de mostrar las detecciones visualmente, incluye un sistema de alerta progresiva que emite un sonido (beep) y una advertencia visual cada vez que un objeto se acerca demasiado a la cámara.

El sonido aumenta su frecuencia conforme el objeto ocupa un mayor porcentaje del área del frame, simulando una alarma de proximidad inteligente.

🚀 Características Principales

🎯 Detección de objetos en tiempo real con MediaPipe Tasks y EfficientDet Lite0 (.tflite).

🔔 Alerta sonora progresiva:

Cuanto más cerca esté el objeto (mayor área en pantalla), más rápido suena el beep.

⚠️ Alerta visual dinámica:

Cajas verdes (objeto lejano) o rojas (objeto cercano).

Mensaje de advertencia con ícono de peligro.

📸 Compatible con cámaras locales o DroidCam.

⚙️ Código limpio y modular, ideal para ampliaciones (por ejemplo, integración con IoT o robots).

🧩 Requisitos Previos
🐍 Versión de Python

Python 3.9 o superior.

📦 Dependencias

Instala los módulos necesarios:

pip install opencv-python mediapipe numpy


⚠️ En Windows, para el sonido se usa winsound, que viene incluido en la librería estándar.

🗂️ Estructura del Proyecto
ObjectDetection/
│
├── efficientdet_lite0.tflite        # Modelo de MediaPipe (descargado previamente)
├── main.py                          # Script principal
└── README.md                        # Este archivo

⚙️ Configuración

Edita los parámetros iniciales del script según tu entorno:

MODEL_PATH = r"C:\Users\USUARIO\Desktop\efficientdet_lite0.tflite"  # Ruta al modelo
CAMERA_INDEX = 3         # Índice de cámara (0, 1, 2, 3, etc.)
SCORE_THRESHOLD = 0.3    # Umbral mínimo de confianza
MAX_RESULTS = 5          # Máximo de detecciones simultáneas

ALERT_AREA_RATIO = 0.10  # Porcentaje del área que activa alerta (10%)
MAX_BEEP_INTERVAL = 1.0  # Intervalo máximo entre beeps (objeto lejos)
MIN_BEEP_INTERVAL = 0.1  # Intervalo mínimo (objeto muy cerca)


🔧 Si usas DroidCam, verifica el índice correcto con:

import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Cámara {i} disponible")
        cap.release()

🧠 Lógica de Funcionamiento
1️⃣ Captura de video

El programa abre la cámara mediante cv2.VideoCapture() y obtiene cada frame.

2️⃣ Detección de objetos

Cada frame se convierte en formato MediaPipe.Image y se envía al detector:

mp_image = Image(image_format=ImageFormat.SRGB,
                 data=cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
detector.detect_async(mp_image, time.time_ns() // 1_000_000)

3️⃣ Evaluación de cercanía

Se calcula el área del objeto vs área total del frame.
Si el objeto ocupa más del 10% (ALERT_AREA_RATIO), se activa una alerta.

4️⃣ Alerta visual

El frame se pinta con una franja roja y un triángulo de advertencia, mostrando el nombre del objeto y su confianza.

5️⃣ Alerta sonora progresiva

El intervalo del beep varía de forma proporcional al tamaño del objeto:

Tamaño relativo	Intervalo entre beeps
0–10% (lejos)	1.0 s
25% (medio)	0.5 s
≥50% (muy cerca)	0.1 s

El sonido se emite mediante winsound.Beep(1000, 150) (solo en Windows).

🎨 Interfaz Visual

Caja verde: objeto detectado sin peligro.

Caja roja + advertencia: objeto demasiado cerca.

Texto: nombre, porcentaje de confianza, porcentaje de área ocupada.

Encabezado rojo: “OBJETO CERCA (label)”.

🧠 Código Clave: Escalado de Intensidad de Alerta
scaled_ratio = min(max_ratio, 0.5)
interval = MAX_BEEP_INTERVAL - (scaled_ratio / 0.5) * (MAX_BEEP_INTERVAL - MIN_BEEP_INTERVAL)


Esto traduce la proporción del área del objeto en una frecuencia de beep, de manera continua y progresiva.

▶️ Ejecución

En consola, navega hasta la carpeta del proyecto y ejecuta:

python main.py


La ventana mostrará la cámara en vivo con detección activa.
Presiona ESC para salir.

🧪 Ejemplo de Uso

Inicia DroidCam o conecta una cámara USB.

Ejecuta el script.

Acerca lentamente un objeto a la cámara.

Verás cómo la caja pasa de verde a roja y el beep aumenta su frecuencia.

💡 Posibles Extensiones

🔉 Integrar sonido personalizado o archivos .wav.

🤖 Conectar el sistema a un microcontrolador (por ejemplo, Arduino) para activar luces o motores.

🧩 Agregar clasificación personalizada (personas, vehículos, etc.) entrenando un modelo propio.

🌐 Integrar con un dashboard web para registro de eventos detectados.

🧾 Créditos

Frameworks: MediaPipe
 · OpenCV

Modelo Base: EfficientDet Lite0 (TensorFlow Lite)

Lenguaje: Python 3.10+