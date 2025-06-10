import os
import pandas as pd

klasor = "sinyaller"
esik_deger = 0.6  # ortalama korelasyon alt sınırı

for dosya in os.listdir(klasor):
    if dosya.endswith("_normalize.csv"):
        dosya_yolu = os.path.join(klasor, dosya)
        etiket = dosya.split("_normalize")[0]
        cikti_yolu = os.path.join(klasor, f"{etiket}_temiz.csv")

        df = pd.read_csv(dosya_yolu, delimiter=';')
        df = df.dropna()

        korelasyon = df.corr()

        # Her sütunun ortalama korelasyonunu hesapla
        ort_korelasyon = korelasyon.mean()

        # Eşik değerden küçük olanları çıkar
        kalan_sutunlar = ort_korelasyon[ort_korelasyon >= esik_deger].index.tolist()
        df_temiz = df[kalan_sutunlar]

        df_temiz.to_csv(cikti_yolu, index=False, sep=';')
        print(f"✅ {dosya} → düşük korelasyonlar silindi, kaydedildi: {cikti_yolu}")
