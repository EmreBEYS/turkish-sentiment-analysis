# EDA ve veri bölme özeti

Bu rapor `python scripts/prepare_data.py` ile yeniden üretildi.

## Temizlik

- Ham satır: 489,644
- Aynı etiketli tekrar satırı: 2,044
- Çelişkili etiketi olan benzersiz metin: 97
- Çelişki nedeniyle çıkarılan toplam satır: 285
- Temiz benzersiz satır: 487,385

## Genel dağılım

| Sınıf | Adet | Oran |
|---|---:|---:|
| negative | 56,077 | 11.5% |
| neutral | 170,691 | 35.0% |
| positive | 260,617 | 53.5% |

Nötr örneklerin büyük bölümü Wikipedia kaynaklıdır; model karşılaştırmasında kaynak kısayolları ve sınıf dengesizliği ayrıca izlenmelidir.

## Uzunluk

Kelime sayısı medyanı 12, p95 değeri 56, en yüksek değer 2724.

## Bölmeler

| Bölme | Satır | negative | neutral | positive |
|---|---:|---:|---:|---:|
| train | 389,904 | 44,860 | 136,552 | 208,492 |
| validation | 48,733 | 5,606 | 17,068 | 26,059 |
| test | 48,748 | 5,611 | 17,071 | 26,066 |

Bölme %80/%10/%10 oranında, sabit tohumla ve `(label, source)` katmanlarına göre yapıldı. Aynı normalize metin iki farklı bölmede bulunamaz.

![Sınıf dağılımı](figures/class_distribution.svg)
