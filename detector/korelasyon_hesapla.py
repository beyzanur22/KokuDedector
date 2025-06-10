import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

klasor = "sinyaller"

for dosya in os.listdir(klasor):
    if dosya.endswith("_normalize.csv"):
        dosya_yolu = os.path.join(klasor, dosya)
        veri = pd.read_csv(dosya_yolu, delimiter=';')

        # Boş hücreleri at (korelasyon düzgün çalışsın)
        veri = veri.dropna()

        # Korelasyon matrisi hesapla
        korelasyon = veri.corr()

        # Yeni dosya adı
        etiket = dosya.split("_normalize")[0]
        cikti_yolu = os.path.join(klasor, f"{etiket}_korelasyon.csv")

        # Excel'e yaz
        korelasyon.to_csv(cikti_yolu, sep=';')
        print(f"✅ Korelasyon matrisi oluşturuldu: {cikti_yolu}")

        # Grafik olarak göster
        plt.figure(figsize=(10, 8))
        sns.heatmap(korelasyon, cmap="coolwarm", annot=False)
        plt.title(f"{etiket} - Korelasyon Matrisi")
        plt.tight_layout()
        plt.show()

