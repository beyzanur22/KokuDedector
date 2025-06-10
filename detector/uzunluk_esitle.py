import os
import csv

klasor = "sinyaller"
hedef_uzunluk = 135 # sabit boy

for dosya in os.listdir(klasor):
    if dosya.endswith("_veri_toplu.csv"):
        tam_yol = os.path.join(klasor, dosya)
        etiket = dosya.split("_veri")[0]
        cikti_yolu = os.path.join(klasor, f"{etiket}_esit.csv")

        with open(tam_yol, "r") as f:
            reader = csv.reader(f, delimiter=';')
            satirlar = list(reader)

        baslik = satirlar[0]
        veri_satirlari = list(zip(*satirlar[1:]))

        yeni_veri = []
        for sütun in veri_satirlari:
            sütun = list(sütun)
            if len(sütun) > hedef_uzunluk:
                sütun = sütun[:hedef_uzunluk]
            elif len(sütun) < hedef_uzunluk:
                sütun += [""] * (hedef_uzunluk - len(sütun))
            yeni_veri.append(sütun)

        yeni_veri = list(zip(*yeni_veri))

        with open(cikti_yolu, "w", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(baslik)
            writer.writerows(yeni_veri)

        print(f"✅ {dosya} dosyası {hedef_uzunluk} veriye sabitlendi → {cikti_yolu}")
