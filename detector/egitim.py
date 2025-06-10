import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

# Klasör yolları ve sınıf isimleri
train_path = r"C:\Users\beyza\OneDrive\Desktop\detector\datasets\train"
test_path = r"C:\Users\beyza\OneDrive\Desktop\detector\datasets\test"

class_names = ["alkol", "sigara","saglikli"]
# === CSV'DEN VERİ OKUMA ve CNN formatına çevirme ===
def load_and_prepare_data(root_path, class_names):
    X = []
    y = []

    for label in class_names:
        folder = os.path.join(root_path, label)
        for filename in os.listdir(folder):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path, sep=";")

                # Her sütun 1 kişi
                for col in df.columns:
                    signal = df[col].dropna().to_numpy()
                    if len(signal) == 129:  # sadece tam uzunlukta olanları al
                        X.append(signal)
                        y.append(label)

    X = np.array(X)
    y = np.array(y)
    X = X[..., np.newaxis]  # CNN için (örnek, 129, 1)
    return X, y



# === VERİYİ YÜKLE ===
X_train, y_train = load_and_prepare_data(train_path, class_names)
X_test, y_test = load_and_prepare_data(test_path, class_names)

# === LABEL'ları SAYISAL HALE GETİR ===
encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)
y_test = encoder.transform(y_test)

# === KONTROL ===
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)
print("X_test :", X_test.shape)
print("y_test :", y_test.shape)
print("Sınıf etiketleri:", list(encoder.classes_))

#Eğitim kısmı

model = Sequential()

# 1️⃣ İlk Conv1D katmanı: 32 filtre, 3 uzunluğunda kernel, ReLU aktivasyonu
model.add(Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(129, 1)))

# 2️⃣ MaxPooling: veriyi 2’ye bölerek boyutu azaltır
model.add(MaxPooling1D(pool_size=2))

# 3️⃣ İkinci Conv1D: daha derin özellikleri öğrenmek için
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))

# 4️⃣ MaxPooling: yine boyut azaltma
model.add(MaxPooling1D(pool_size=2))

# 5️⃣ Flatten: tüm özellikleri tek vektöre çevir
model.add(Flatten())

# 6️⃣ Fully connected katman: 64 nöron
model.add(Dense(64, activation='relu'))

# 7️⃣ Dropout: overfitting’e karşı
model.add(Dropout(0.5))

# 8️⃣ Çıkış katmanı: 4 sınıf olduğu için 4 nöron ve softmax aktivasyonu
model.add(Dense(4, activation='softmax'))

model.compile(
    loss='sparse_categorical_crossentropy',  # çünkü etiketlerimiz [0,1,2,3] şeklinde
    optimizer='adam',  # popüler, hızlı öğrenen optimizasyon yöntemi
    metrics=['accuracy']  # başarıyı ölçmek için doğruluk oranı
)
checkpoint = ModelCheckpoint(
    "nefes_modeli2.keras",  # en iyi modeli bu isimle kaydet
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)
#eğitim
history = model.fit(
    X_train, y_train,
    epochs=16,
    batch_size=8,
    validation_data=(X_test, y_test),
    callbacks=[checkpoint]
)
