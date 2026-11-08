import cv2
import mediapipe as mp
from mediapipe.python.solutions import hands as mpHands
from mediapipe.python.solutions import drawing_utils as mpDraw
import math
import serial
import time

# --- BLUETOOTH AYARLARI ---
try:
    ser = serial.Serial('COM5', 9600, timeout=1)  # 9600 baud
    time.sleep(2)
    print("COM5'e baglandi! 9600 baud ile calisiyor.")
except:
    print("HATA: COM5 acilamadi!")
    ser = None

# --- PARMAK MESAFE AYARLARI ---
MIN_MESAFE = 40
MAX_MESAFE = 200
YUMUSATMA_KATSAYISI = 0.2
OLU_BOLGE = 3

# --- KAMERA VE MEDIAPIPE ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

parmak_uclari = [4, 8, 12, 16, 20]
eski_acilar   = [0, 0, 0, 0, 0]
onceki_acilar = [-1, -1, -1, -1, -1]  # Degisim kontrolu icin

def map_range(x, in_min, in_max, out_min, out_max):
    if x < in_min: x = in_min
    if x > in_max: x = in_max
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    imgRGB.flags.writeable = False
    results = hands.process(imgRGB)
    imgRGB.flags.writeable = True

    guncel_acilar = [0, 0, 0, 0, 0]

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            lm0 = handLms.landmark[0]
            cx0, cy0 = int(lm0.x * w), int(lm0.y * h)

            for i, uc_id in enumerate(parmak_uclari):
                lm_uc = handLms.landmark[uc_id]
                cx_uc, cy_uc = int(lm_uc.x * w), int(lm_uc.y * h)

                mesafe = math.hypot(cx_uc - cx0, cy_uc - cy0)
                ham_aci = map_range(mesafe, MIN_MESAFE, MAX_MESAFE, 0, 180)

                hesaplanan_aci = int(
                    (ham_aci * YUMUSATMA_KATSAYISI) +
                    (eski_acilar[i] * (1.0 - YUMUSATMA_KATSAYISI))
                )

                if abs(hesaplanan_aci - eski_acilar[i]) < OLU_BOLGE:
                    hesaplanan_aci = eski_acilar[i]

                guncel_acilar[i] = hesaplanan_aci
                eski_acilar[i]   = hesaplanan_aci

            # SADECE DEGISIM VARSA GONDER
            if guncel_acilar != onceki_acilar:
                veri_paketi = f"<{guncel_acilar[0]},{guncel_acilar[1]},{guncel_acilar[2]},{guncel_acilar[3]},{guncel_acilar[4]}>\n"
                if ser:
                    try:
                        ser.write(veri_paketi.encode())
                        onceki_acilar = guncel_acilar.copy()
                    except:
                        pass

                cv2.putText(img, veri_paketi.strip(), (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Biyonik El", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if ser: ser.close()