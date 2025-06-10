import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import tensorflow as tf
import seaborn as sns
import matplotlib.pyplot as plt

# === Ayarlar ===
test_path = r"C:\Users\beyza\OneDrive\Desktop\detector\datasets\test"
class_names = ["alkol", "sigara", "saglikli"]

# === Veri Yükleme Fonksiyonu ===
def load_test_data(path, class_names):
    X = []
    y = []
    for label in class_names:
        folder = os.path.join(path, label)
        if not os.path.exists(folder):
            print(f"❌ Klasör yok: {folder}")
            continue
        for file in os.listdir(folder):
            if file.endswith(".csv"):
                file_path = os.path.join(folder, file)
                df = pd.read_csv(file_path, sep=";", skiprows=1, header=None)
                df_numeric = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1)
                for col in df_numeric.columns:
                    signal = df_numeric[col].dropna().to_numpy()
                    if len(signal) == 129:
                        try:
                            signal = signal.astype(np.float32)
                            X.append(signal)
                            y.append(label)
                        except Exception as e:
                            print(f"{file_path} hata: {e}")
                    else:
                        print(f"{file_path} uzunluk {len(signal)} - atlandı.")
    return np.array(X), np.array(y)

# === Veri Hazırlığı ===
X_test, y_test = load_test_data(test_path, class_names)
X_test = X_test[..., np.newaxis]  # 3D reshape

# === Label Encoding ===
encoder = LabelEncoder()
encoder.fit(class_names)
y_test_encoded = encoder.transform(y_test)

# === Modeli Yükle ===
model = tf.keras.models.load_model("nefes_modeli2.keras")

# === Tahmin ===
y_pred_probs = model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)

# === Değerlendirme ===
acc = accuracy_score(y_test_encoded, y_pred)
print(f"✅ Doğruluk (Accuracy): {acc * 100:.2f}%\n")

print("📋 Sınıflandırma Raporu:")
print(classification_report(y_test_encoded, y_pred, target_names=class_names))

# === Confusion Matrix ===
cm = confusion_matrix(y_test_encoded, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=class_names, yticklabels=class_names, cmap='Blues')
plt.xlabel("Tahmin Edilen")
plt.ylabel("Gerçek")
plt.title("Confusion Matrix")
plt.show()
