# Sprint 01 kaydı

Durum: tamamlandı

## Kabul ölçütleri

- [x] Ham CSV şeması ve etiketleri doğrulandı.
- [x] Normalize tam tekrarlar bölmeden önce kaldırıldı.
- [x] Aynı metnin çelişkili etiketleri veri dışında bırakıldı.
- [x] Sabit tohumlu, etiket+kaynak katmanlı %80/%10/%10 split üretildi.
- [x] Bölmeler arası tam metin sızıntısı olmadığı test edildi.
- [x] EDA JSON, CSV, Markdown ve SVG çıktıları üretildi.

## Definition of Done

`python -m unittest discover -s tests -v` başarılıdır ve `python scripts/prepare_data.py` aynı özet sayıları yeniden üretir.

