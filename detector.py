import os, time, sys, cv2, numpy as np
from collections import deque
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import ObjectDetector, ObjectDetectorOptions, RunningMode
from mediapipe import Image, ImageFormat

# =================== CONFIG ===================
MODEL_PATH = r"C:\Users\USUARIO\Desktop\efficientdet_lite0.tflite"
CAMERA_INDEX = 3
SCORE_THRESHOLD = 0.3
MAX_RESULTS = 5

# Porcentaje del área del frame que activa alerta
ALERT_AREA_RATIO = 0.10    # alerta a partir del 10%
# límites para sonido (en segundos)
MAX_BEEP_INTERVAL = 1.0    # lejos → beep cada 1s
MIN_BEEP_INTERVAL = 0.1    # muy cerca → beep cada 0.1ss
# ==============================================

def beep():
    """Beep en Windows."""
    if sys.platform.startswith("win"):
        try:
            import winsound
            winsound.Beep(1000, 150)
        except Exception:
            pass

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(MODEL_PATH)

latest_result = deque(maxlen=1)
last_beep_ts = 0
last_ratio = 0

def draw_and_alert(frame, detections):
    global last_beep_ts, last_ratio
    h_img, w_img = frame.shape[:2]
    frame_area = h_img * w_img
    alert_active = False
    alert_labels = []
    max_ratio = 0

    for det in detections:
        b = det.bounding_box
        x, y = int(b.origin_x), int(b.origin_y)
        bw, bh = int(b.width), int(b.height)
        x2, y2 = x + bw, y + bh

        # Datos de la detección
        label, score = "obj", 0.0
        if det.categories:
            cat = det.categories[0]
            label = cat.category_name or "obj"
            score = float(cat.score or 0.0)

        # Calcular proporción de área
        obj_area = bw * bh
        ratio = obj_area / frame_area
        max_ratio = max(max_ratio, ratio)

        # Color: rojo si está cerca, verde si no
        color = (0, 0, 255) if ratio >= ALERT_AREA_RATIO else (0, 255, 0)

        # Dibujar caja y etiqueta
        cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {score*100:.1f}%  {ratio*100:.1f}%", 
                    (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,255), 2)

        if ratio >= ALERT_AREA_RATIO:
            alert_active = True
            alert_labels.append(label)

    # --- ALERTA VISUAL ---
    if alert_active:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w_img, 80), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

        # triángulo de advertencia
        pts = np.array([[25, 60], [55, 60], [40, 25]], np.int32)
        cv2.fillPoly(frame, [pts], (0, 255, 255))  # amarillo
        cv2.polylines(frame, [pts], True, (0, 0, 0), 2)
        cv2.putText(frame, "!", (35, 58), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0,0,0), 3)

        msg = f"OBJETO CERCA ({', '.join(alert_labels)})"
        cv2.putText(frame, msg, (70, 55), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)

    # --- ALERTA SONORA PROGRESIVA ---
    if alert_active:
        # Convertir tamaño (ratio) en frecuencia de beep
        # Ej: 0.1 → 1s, 0.3 → 0.5s, 0.5+ → 0.1s
        scaled_ratio = min(max_ratio, 0.5)  # saturamos a 50%
        interval = MAX_BEEP_INTERVAL - (scaled_ratio / 0.5) * (MAX_BEEP_INTERVAL - MIN_BEEP_INTERVAL)
        now = time.time()
        if now - last_beep_ts >= interval:
            beep()
            last_beep_ts = now
        last_ratio = scaled_ratio

def detection_callback(result, output_image, timestamp_ms):
    latest_result.clear()
    latest_result.append(result)

# Configuración del detector
options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    max_results=MAX_RESULTS,
    score_threshold=SCORE_THRESHOLD,
    running_mode=RunningMode.LIVE_STREAM,
    result_callback=detection_callback
)
detector = ObjectDetector.create_from_options(options)

# Cámara DroidCam
cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
if not cap.isOpened():
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_MSMF)
if not cap.isOpened():
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_ANY)
if not cap.isOpened():
    raise RuntimeError(f"No se pudo abrir cámara índice {CAMERA_INDEX}.")

print("✅ Detector con sonido progresivo activo. Presiona ESC para salir.")
try:
    while True:
        ok, frame_bgr = cap.read()
        if not ok:
            print("⚠️ No se pudo leer frame.")
            break

        mp_image = Image(image_format=ImageFormat.SRGB,
                         data=cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
        detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        if latest_result:
            draw_and_alert(frame_bgr, latest_result[0].detections)

        cv2.imshow("Detección + Alerta Progresiva", frame_bgr)
        if cv2.waitKey(1) & 0xFF == 27:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
