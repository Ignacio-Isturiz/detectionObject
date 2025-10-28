# probar_indices.py
import cv2, time

def try_index(i):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return False
    ok, frame = cap.read()
    if not ok:
        cap.release()
        return False
    cv2.putText(frame, f"INDEX {i}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)
    cv2.imshow(f"CAM INDEX {i}", frame)
    cv2.waitKey(800)  # muestra 0.8s
    cap.release()
    cv2.destroyAllWindows()
    return True

for i in range(6):  # prueba 0..5
    if try_index(i):
        print(f"[OK] index {i}")
