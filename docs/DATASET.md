# Veri seti kararı

## Seçilen veri

- Ad: `winvoker/turkish-sentiment-analysis-dataset`
- Kaynak: https://huggingface.co/datasets/winvoker/turkish-sentiment-analysis-dataset
- Görev: Türkçe, üç sınıflı duygu sınıflandırma (`negative`, `neutral`, `positive`)
- Ham boyut: 489.644 satır
- Lisans: CC BY-SA 4.0 (veri kartında belirtilen lisans)
- Alanlar: `text`, `label`, `dataset`

Bu seçim AG News konu sınıflandırmasından hem dil hem görev açısından ayrıdır. Veri metinleri doğrudan erişilebilir, üç sınıf klasik ML ile BERT için ortaktır ve ham dosyalar sabit SHA-256 değerleriyle doğrulanır.

### Atıf ve paylaşım koşulu

Veri bu repoda yeniden dağıtılmaz. Kullanıcı `scripts/download_data.py` ile kaynaktan indirir. Veri veya türevi yayımlanırsa CC BY-SA 4.0 atıf ve aynı lisans koşulları ayrıca uygulanmalıdır. Kaynak veri kartındaki alt kaynakların kökeni de raporda belirtilmelidir.

## İncelenen fakat seçilmeyen adaylar

### Boğaziçi TULAP — Dataset for Targeted Sentiment Analysis in Turkish

MIT lisanslı, akademik ve üç sınıflı bir kaynaktır. Ancak indirilen CSV’ler tweet metni yerine tweet URL’leri içerir. Canlı platform erişimine bağımlı olduğu ve metinlerin yeniden üretilebilirliği zayıf olduğu için ana veri yapılmadı.

### TRSAv1

150.000 dengeli Türkçe e-ticaret yorumu içerir; fakat erişilebilir veri kartında açık bir lisans tanımlayıcısı yoktur. “Gerçek lisanslı veri” koşulu nedeniyle kullanılmadı.

## Etik ve yöntemsel riskler

- Veri; ürün yorumları, mağaza yorumları, tweetler, film yorumları ve Wikipedia cümlelerini birleştirir.
- Nötr sınıfın önemli kısmı Wikipedia kaynaklıdır. Model, duygu yerine kaynak/üslup ipuçlarını öğrenebilir.
- Kullanıcı üretimi metinlerde kişisel bilgi veya saldırgan ifade bulunabilir; örnekler raporlara gereksiz yere kopyalanmamalıdır.
- Tekrarlı metinler ve çelişkili etiketler bölmeden önce çıkarılır.
- Birincil başarı ölçütü `macro-F1`; accuracy yalnız başına yorumlanmaz.

