# 20 örneklik hata analizi protokolü

Bu dosya Sprint 04’te doldurulacaktır; şimdilik seçim yöntemi sabitlenmiştir.

1. Nihai test tahminlerinden yanlış sınıflanan kayıtları çıkar.
2. Her gerçek sınıftan en az 5 örnek seç.
3. Kalan 5 örneği en sık hata çiftleri ve klasik model–BERT ayrışmalarından seç.
4. Yalnızca kolay/açık hataları seçmemek için örnekleri sabit seed ile aday havuzundan örnekle.
5. Her satırda `id`, kısa metin/alinti, gerçek etiket, tahmin, model skoru, hata kategorisi ve yorum bulunsun.

Hedef tam olarak 20 incelenmiş örnektir. Kategoriler: olumsuzlama, ironi, karma duygu, bağlam eksikliği, kaynak/alan ipucu, yazım-gürültü, etiket şüphesi ve uzunluk/kesilme.

