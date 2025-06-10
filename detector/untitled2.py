import os
import numpy as np
import pandas as pd
import shutil

# === AYARLAR ===
source_dir = r"C:/Users/beyza/detector/datasets/train"
target_dir = r"C:/Users/bbeyza/detector/datasets/train_augmented"
class_names = ["alkol", "sigara", "saglikli"]
augment_per_signal = 2  # Her sinyale kaç tane yeni sinyal eklenecek

# Yeni klasör temiz başlatılsın
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
os.makedirs(target_dir, exist_ok=True)

# === Fonksiyonlar ===

def add_noise(signal, noise_level=5):
    noise = np.random.randint(-noise_level, noise_level + 1, size=signal.shape)
    return signal + noise

def shift_signal(signal, shift_max=5):
    shift = np.random.randint(-shift_max, shift_max)
    return np.roll(signal, shift)

# === AUGMENTATION ===
for label in class_names:
    klasor_yolu = os.path.join(source_dir, label)
    hedef_klasor = os.path.join(target_dir, label)
    os.makedirs(hedef_klasor, exist_ok=True)

    for dosya in os.listdir(klasor_yolu):
        if dosya.endswith(".csv"):
            dosya_yolu = os.path.join(klasor_yolu, dosya)
            df = pd.read_csv(dosya_yolu, sep=";")

            for col_index, col in enumerate(df.columns):
                signal = df[col].dropna().to_numpy(dtype=np.float32)

                if len(signal) != 129:
                    continue  # sadece tam uzunlukta olanları al

                # Orijinal sinyali kaydet
                orijinal_dosya = f"{label}{dosya.replace('.csv','')}_orj{col_index}.csv"
                pd.DataFrame(signal).to_csv(os.path.join(hedef_klasor, orijinal_dosya), sep=";", index=False, header=False)

                # Yeni sinyaller üret
                for i in range(augment_per_signal):
                    yeni_signal = add_noise(signal)
                    yeni_signal = shift_signal(yeni_signal)
                    yeni_dosya = f"{label}{dosya.replace('.csv','')}_aug{col_index}{i}.csv"
                    pd.DataFrame(yeni_signal).to_csv(os.path.join(hedef_klasor, yeni_dosya), sep=";", index=False, header=False)

print("✅ Augmentation tamamlandı ve yeni veriler 'train_augmented' klasörüne kaydedildi.")