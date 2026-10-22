# Türkçe Duygu Analizi

Robotik dersi NLP ödevi için, önceki AG News konu sınıflandırmasından bağımsız Türkçe üç sınıflı duygu analizi projesi. Hedef; TF-IDF tabanlı Logistic Regression, Multinomial Naive Bayes ve Linear SVM modellerini BERTurk ile aynı veri bölmeleri ve metrikler üzerinde karşılaştırmaktır.

Bu repo yalnızca ders ödevini kapsar. Olası dönem projesi özellikleri burada geliştirilmez.

## Durum

- Sprint 00: kapsam, veri/lisans kararı ve iskelet — tamamlandı
- Sprint 01: EDA, temizlik ve sızıntısız bölme — tamamlandı
- Sprint 02+: modelleme, BERT ve 20 örneklik hata analizi — yol haritasında

## Veri seti

`winvoker/turkish-sentiment-analysis-dataset` kullanılır. Hugging Face veri kartı veri setini CC BY-SA 4.0 olarak işaretler. Ham veriler Git’e eklenmez; kaynak ve riskler [docs/DATASET.md](docs/DATASET.md) içinde kayıtlıdır.

Ham veri: 489.644 satır, üç etiket ve altı kaynak. Hazırlama adımı normalize tekrarları/etiket çelişkilerini çıkarır ve `(label, source)` katmanlı %80/%10/%10 split üretir.

## Kurulum

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

BERT sprintinde:

```powershell
python -m pip install -r requirements-bert.txt
```

## Veriyi yeniden üretme

```powershell
python scripts/download_data.py
python scripts/prepare_data.py
python -m unittest discover -s tests -v
```

`download_data.py` iki kaynak dosyayı sabit SHA-256 değerleriyle doğrular. `prepare_data.py` şu yerel çıktıları oluşturur:

- `data/processed/{train,validation,test}.csv` — Git dışında
- `reports/eda_summary.json`
- `reports/class_distribution.csv`
- `reports/figures/class_distribution.svg`
- `docs/eda.md`

## Değerlendirme planı

Ana ölçüt macro-F1’dır. Accuracy, weighted-F1, sınıf bazlı precision/recall/F1 ve confusion matrix birlikte raporlanacaktır. Nihai raporda sabit protokolle seçilmiş 20 yanlış tahmin nitel olarak incelenecektir.

Ayrıntılar: [Sprint yol haritası](docs/SPRINTS.md) ve [hata analizi protokolü](docs/ERROR_ANALYSIS.md).

