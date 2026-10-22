# Sprint yol haritası

## Sprint 00 — kapsam ve yeniden üretilebilirlik (tamamlandı)

- AG News projesinden ayrı Türkçe duygu analizi kapsamı
- Lisansı açık ve metni erişilebilir veri seçimi
- Kaynak, lisans, risk ve atıf kaydı
- Python proje iskeleti, bağımlılık grupları, Git kuralları ve test altyapısı
- Başarı ölçütleri: macro-F1, weighted-F1, accuracy, sınıf bazlı precision/recall/F1 ve confusion matrix

## Sprint 01 — veri, EDA ve bölme (tamamlandı)

- SHA-256 doğrulamalı indirme
- Şema/etiket kontrolü, boş metin kontrolü
- Normalize tam tekrarların ve çelişkili etiketlerin çıkarılması
- `(label, source)` katmanlı, sabit tohumlu %80/%10/%10 bölme
- Bölmeler arası tam metin sızıntısı testi
- Sınıf, kaynak ve metin uzunluğu EDA çıktıları

## Sprint 02 — klasik ML taban çizgileri

- Ortak `TfidfVectorizer` hattı; word n-gram ve char n-gram deneyleri
- Logistic Regression, Multinomial Naive Bayes ve Linear SVM
- Yalnızca validation üzerinde hiperparametre seçimi
- Test setini tek seferlik nihai karşılaştırma için kilitleme
- Eğitim süresi, tahmin süresi ve model boyutu kaydı

## Sprint 03 — BERTurk

- Başlangıç modeli: `dbmdz/bert-base-turkish-cased`
- Aynı split ve aynı etiket eşlemesi
- Token uzunluğu analiziyle `max_length` seçimi
- Early stopping; seed, paket ve donanım kaydı
- En iyi klasik model ile aynı metrik tablosunda karşılaştırma

## Sprint 04 — değerlendirme ve 20 hata analizi

- Accuracy, macro/weighted-F1, sınıf bazlı precision/recall/F1
- Confusion matrix ve klasik model–BERT fark tablosu
- Test hatalarından sabit yöntemle 20 örnek: her gerçek sınıftan ve ana hata çiftlerinden temsil
- Her örnek için: metin kimliği, gerçek/tahmin, güven/skor, model, hata kategorisi, kısa açıklama
- Hata kategorileri: olumsuzlama, ironi, karma duygu, bağlam eksikliği, alan/kaynak etkisi, yazım-gürültü, etiket şüphesi, uzun metin/kesilme

## Sprint 05 — raporlama ve teslim

- Sonuç tabloları, sınırlamalar, etik notlar ve yeniden üretme komutları
- Kullanılmayan deney/artifact temizliği
- Sürüm etiketi ve teslim kontrol listesi

## Kapsam dışı

Robot kontrolü, görüntü işleme, sensör verisi, LLM tabanlı uygulama, canlı API ve dönem projesine özgü genişletmeler bu ödev reposuna eklenmez.

