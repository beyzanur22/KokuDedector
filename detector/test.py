
import serial
import numpy as np
import tensorflow as tf
import time

# Modeli yükle
model = tf.keras.models.load_model("nefes_modeli2.keras")

# Seri portu ayarla (COM portunu sistemine göre değiştir)
ser = serial.Serial('COM4', 9600, timeout=1)

# Sinyali model girişine uygun hale getir
def preprocess_signal(signal):
    signal = np.array(signal)
    if len(signal) != 129:
        return None
    return signal.reshape(1, 129, 1)

# Tahmin sonucunu etiketle
def decode_prediction(pred):
    classes = ["alkol","sigara","saglikli"]
    return classes[np.argmax(pred)]

print("🔌 Arduino'dan veri bekleniyor...")

while True:
    sinyal_verisi = []
    start_time = time.time()

    print("⏱️ 7 saniyelik sinyal kaydı başlıyor...")

    # 10 saniyelik veri oku
    while time.time() - start_time < 7:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            try:
                values = list(map(float, line.split(',')))
                sinyal_verisi.extend(values)
            except:
                continue

    # 135 örnek toplandıysa tahmin yap
    if len(sinyal_verisi) >= 129:
        input_signal = sinyal_verisi[:129]
        processed_signal = preprocess_signal(input_signal)

        if processed_signal is not None:
            prediction = model.predict(processed_signal)
            predicted_class = decode_prediction(prediction)
            print(f"📢 Tahmin: {predicted_class}")
        else:
            print("⚠️ Veri formatı hatalı, yeniden deneyin.")
    else:
        print("⚠️ Yeterli veri toplanamadı. Lütfen tekrar deneyin.")

    # Döngüyü sonlandırmak istersen:
    tekrar = input("Yeni bir ölçüm almak için Enter'a basın, çıkmak için 'q': ")
    if tekrar.lower() == 'q':
        break

ser.close()
