import serial
import time
import csv
import os
import numpy as np

ser = serial.Serial('COM4', 9600)  
time.sleep(2)

etiket = input("Bu sinyalin etiketi nedir? ( sigara, saglikli, alkol): ")

# Klasör ve dosya yolu belirleme
klasor = "sinyaller"
os.makedirs(klasor, exist_ok=True)
dosya_adi = f"{etiket}_veri_toplu.csv"
tam_yol = os.path.join(klasor, dosya_adi)

veri_listesi = []
baslangic = time.time()

print("\n⏳ 10 saniyelik sinyal kaydı başlıyor...")

while time.time() - baslangic < 10:
    if ser.in_waiting:
        satir = ser.readline().decode('utf-8').strip()
        try:
            deger = int(satir)
            veri_listesi.append(deger)
        except:
            continue

print("✅ Kayıt tamamlandı. Toplam veri sayısı:", len(veri_listesi))

# Tüm sinyallerin eşit uzunlukta olması için sabit uzunluk belirle
hedef_uzunluk = 250
if len(veri_listesi) < hedef_uzunluk:
    veri_listesi += [""] * (hedef_uzunluk - len(veri_listesi))
elif len(veri_listesi) > hedef_uzunluk:
    veri_listesi = veri_listesi[:hedef_uzunluk]

veriler_np = np.array(veri_listesi).reshape(-1, 1)

# Eğer dosya varsa, verileri oku ve yeni sütun olarak ekle
if os.path.isfile(tam_yol):
    with open(tam_yol, "r") as f:
        reader = csv.reader(f, delimiter=';')
        mevcut_veri = list(reader)
    basliklar = mevcut_veri[0]
    veri_satirlari = mevcut_veri[1:]

    # Satır sayısını sabit uzunluğa getir
    while len(veri_satirlari) < hedef_uzunluk:
        veri_satirlari.append([''] * len(basliklar))

    # Yeni başlık ve veri sütun olarak ekleniyor
    basliklar.append(f"Ornek{len(basliklar) + 1}")
    for i in range(hedef_uzunluk):
        veri_satirlari[i].append(str(veriler_np[i][0]))

    # Dosyayı tekrar yaz
    with open(tam_yol, "w", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(basliklar)
        writer.writerows(veri_satirlari)
else:
    # İlk kez yazıyorsa başlık ve veri sütunu oluştur
    basliklar = ["Ornek1"]
    with open(tam_yol, "w", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(basliklar)
        for deger in veri_listesi:
            writer.writerow([deger])

print(f"\n💾 Ham sinyal sütun olarak {etiket}_veri_toplu.csv dosyasına eklendi.")
ser.close()



