import cv2
from ultralytics import YOLO
from tkinter import messagebox
import time

# Modeli yükle / Load model
model = YOLO("yolov8n.pt")
# Etiketleri ayarla (TR) / Set labels (TR)
labels = ['Insan', 'Bisiklet', 'Araba', 'Motosiklet', 'Ucak', 'Otobus', 'Tren', 'Kamyon', 'Bot', 'Trafik Lambasi',
          'Yangin Muslugu', 'Dur Levhasi', 'Parkmetre', 'Bank', 'Kus', 'Kedi', 'Kopek', 'At', 'Koyun', 'Inek',
          'Fil', 'Ayi', 'Zebra', 'Zurafa', 'Canta', 'Semsiye', 'El Cantasi', 'Kravat', 'Bavul', 'Frizbi','Kayaklar',
          'Kayak', 'Spor Topu', 'Ucurtma', 'Beyzbol Sopasi', 'Beyzbol Eldiveni', 'Kaykay', 'Sorf Tahtasi','Tenis Raketi',
          'Sise', 'Kadeh', 'Bardak', 'Catal', 'Bicak', 'Kasik', 'Kase', 'Muz', 'Elma','Sandviç','Portakal', 'Brokoli',
          'Havuc', 'Sosisli', 'Pizza', 'Corek', 'Kek', 'Sandalye', 'Kanepe','Saksi Bitkisi','Yatak', 'Yemek Masasi',
          'Tuvalet', 'Ekran/TV', 'Laptop', 'Mouse', 'Remote', 'Klavye', 'Cep Telefonu','Mikrodalga', 'Firin', 'Tost Makinesi',
          'Lavabo', 'Buzdolabi', 'Kitap', 'Saat', 'Vazo', 'Makas', 'Ayicik','Sac Kurutma Makinesi', 'Dis Fircasi']

# Kamerayı aç ve fontu ayarla / Open the camera and set the font
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
aruco_params = cv2.aruco.DetectorParameters()

pixel_to_cm = 4.0               # Değer artırınca boyut artar / As you increase the value, the size increases
reference_width_cm = 7.5        # Referans nesnenin genişliği (Cep Telefonu baz alınmıştır) (cm cinsinden) / Width of reference object (based on Mobile Phone) (in cm)
reference_height_cm = 7.8       # Referans nesnenin yüksekliği (Cep Telefonu baz alınmıştır) (cm cinsinden) / Height of reference object (based on Mobile Phone) (in cm)
reference_width_px = 500        # Çerçeve genişliğinin piksel cinsinden değeri / Value of frame width in pixels
reference_height_px = 500       # Çerçeve yüksekliğinin piksel cinsinden değeri / Value of frame height in pixels
perspective_correction = 0.5    # Değeri artırınca nesnelerin uzaklaştıkça ölçüleri üzerindeki perspektif etkisini daha fazla düzeltiyor / Increasing the value further corrects the perspective effect on the size of objects as they move further away
distance = 2.0                  # Simüle edilen uzaklık değeri (cm cinsinden) / Simulated distance value (in cm)

# Mesafeyi ölçen fonksiyon / Calculate distance func
def calculate_distance(focal_length, actual_width, pixel_width):
    return (actual_width * focal_length) / pixel_width

# Özel nesneleri tespit etme fonksiyonu / Detect specific object func
def detect_specific_object(frame, model, labels, target_labels):
    results = model(frame, save=False, verbose=False)
    focal_length = (reference_width_px * distance) / reference_width_cm

    detected_object = False

    for i in range(len(results[0].boxes)):
        x1, y1, x2, y2 = results[0].boxes.xyxy[i]
        score = results[0].boxes.conf[i]
        label = results[0].boxes.cls[i]
        x1, y1, x2, y2, score, label = int(x1), int(y1), int(x2), int(y2), float(score), int(label)
        name = labels[label]

        if name in target_labels and not detected_object:
            width_cm = (x2 - x1) * pixel_to_cm * (1 + perspective_correction * distance)
            height_cm = (y2 - y1) * pixel_to_cm * (1 + perspective_correction * distance)

            real_width_cm = (width_cm / reference_width_px) * reference_width_cm
            real_height_cm = (height_cm / reference_height_px) * reference_height_cm

            distance_cm = calculate_distance(focal_length, reference_width_cm, x2 - x1)

            # Nesne bilgilerini ekrana yazdırma / Write on screen of objects information
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            text = f"{name}"
            cv2.putText(frame, text, (x1, y1 - 10), font, 1.0, (0, 255, 0), 2)
            cv2.putText(frame, f"Genislik: {real_width_cm:.2f} cm", (x1, y2 + 30), font, 0.8, (255, 127, 127), 2)
            cv2.putText(frame, f"Yukseklik: {real_height_cm:.2f} cm", (x1, y2 + 60), font, 0.8, (255, 127, 127), 2)
            cv2.putText(frame, f"Uzaklik: {distance_cm:.2f} cm", (x1, y2 + 90), font, 0.8, (255, 127, 127), 2)

            detected_object = True

    return frame

if __name__ == "__main__":
    prev_time = 0

    while True:
        success, img = cap.read()
        if not success:
            messagebox.showwarning("Hata", "Video Akışı Okunamıyor")
            break

        img = cv2.flip(img, 1)
        # Spesifik nesneler / Specific objects
        result_frame = detect_specific_object(img, model, labels, ["Cep Telefonu", "Sise", "Kadeh", "Bardak", "Catal", "Bicak", "Kasik", "Kase", "Klavye",
                                                                   "Mouse", "Ekran/TV", "Kanepe", "Sandalye", "Yatak", "Yemek Masasi", "Tuvalet", "Laptop", "Mikrodalga",
                                                                   "Firin", "Tost Makinesi", "Lavabo", "Buzdolabi", "Kitap", "Saat", "Vazo", "Makas", "Araba"])
        result_frame = cv2.resize(result_frame, (800, 600))

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time
        cv2.putText(result_frame, f"FPS: {int(fps)}", (10,40), font, 1.0, (0, 0, 255), 2)
        cv2.putText(result_frame, "(En dogru olcum icin uzaklik degeri 15cm civarinda olmalidir)", (10, 60), font, 0.5, (0, 0, 255), 1)
        cv2.putText(result_frame, "(Cikis icin 'ESC' veya 'Q' tusuna basiniz)", (10, 80), font, 0.5, (0, 0, 255), 1)

        cv2.imshow('Nesne Tespiti ve Ölçümü', result_frame)

        key = cv2.waitKey(1)
        if key == 27 or key == 81 or key == 113:
            break

cap.release()
cv2.destroyAllWindows()