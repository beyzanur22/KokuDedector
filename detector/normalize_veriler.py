import os
import csv
import numpy as np

klasor = "sinyaller"

for dosya in os.listdir(klasor):
    if dosya.endswith("_esit.csv"):
        tam_yol = os.path.join(klasor, dosya)
        etiket = dosya.split("_esit")[0]
        cikti_yolu = os.path.join(klasor, f"{etiket}_normalize.csv")

        with open(tam_yol, "r") as f:
            reader = csv.reader(f, delimiter=';')
            satirlar = list(reader)

        baslik = satirlar[0]
        veri_satirlari = list(zip(*satirlar[1:]))

        yeni_veri = []
        for sütun in veri_satirlari:
            try:
                sayilar = np.array([float(v) if v != '' else np.nan for v in sütun])
                min_val = np.nanmin(sayilar)
                max_val = np.nanmax(sayilar)
                if max_val - min_val == 0:
                    norm = [0 for _ in sayilar]
                else:
                    norm = [(v - min_val) / (max_val - min_val) if not np.isnan(v) else '' for v in sayilar]
                yeni_veri.append(norm)
            except:
                yeni_veri.append(sütun)  # bozulmuşsa dokunma

        yeni_veri = list(zip(*yeni_veri))

        with open(cikti_yolu, "w", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(baslik)
            writer.writerows(yeni_veri)

        print(f"✅ Normalize edildi → {cikti_yolu}")


