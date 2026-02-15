# 📁 Proje Yapısı

```
market-analiz/
│
├── 📄 market_analiz.py          # Ana program dosyası
├── 📄 README.md                  # Detaylı proje dokümantasyonu
├── 📄 QUICKSTART.md             # Hızlı başlangıç rehberi
├── 📄 CONTRIBUTING.md           # Katkıda bulunma rehberi
├── 📄 LICENSE                    # MIT Lisansı
├── 📄 requirements.txt          # Python bağımlılıkları
├── 📄 .gitignore               # Git ignore dosyası
├── 📄 ornek_veri.json          # Test için örnek veri
│
├── 📂 Kullanıcı Verileri (çalışma zamanında oluşturulur)
│   ├── market_verileri.json    # Ana veri dosyası (otomatik oluşur)
│   └── market_rapor_*.csv      # Dışa aktarılan raporlar
│
└── 📂 İleride Eklenebilecekler
    ├── web/                     # Web arayüzü
    ├── mobile/                  # Mobil uygulama
    ├── tests/                   # Test dosyaları
    └── docs/                    # Ek dokümantasyon
```

## 📄 Dosya Açıklamaları

### Ana Program
- **market_analiz.py**: Tüm işlevleri içeren ana Python programı (500+ satır)

### Dokümantasyon
- **README.md**: Kapsamlı kullanım kılavuzu, özellikler, kurulum
- **QUICKSTART.md**: 5 dakikada başlangıç rehberi
- **CONTRIBUTING.md**: Geliştirici katkı rehberi
- **STRUCTURE.md**: Bu dosya - proje yapısı

### Yapılandırma
- **LICENSE**: MIT Lisansı metni
- **requirements.txt**: Python kütüphane gereksinimleri
- **.gitignore**: Git'in görmezden gelmesi gereken dosyalar

### Veri Dosyaları
- **ornek_veri.json**: Test için hazır örnek veri
- **market_verileri.json**: Kullanıcı verileri (program çalıştırılınca oluşur)

## 🔧 Kod Yapısı (market_analiz.py)

```python
class MarketAnaliz:
    │
    ├── __init__()                      # Başlatma
    ├── verileri_yukle()                # JSON'dan veri yükleme
    ├── verileri_kaydet()               # JSON'a veri kaydetme
    │
    ├── 📝 Fiş İşlemleri
    │   ├── fis_ekle()                  # Yeni fiş girişi
    │   ├── fisler_listele()            # Fişleri göster
    │   └── _urun_verilerini_guncelle() # İstatistikleri güncelle
    │
    ├── 💰 Fiyat Karşılaştırma
    │   └── fiyat_karsilastir()         # Market market karşılaştırma
    │
    ├── 📊 Analiz Fonksiyonları
    │   ├── harcama_analizi()           # Ana analiz menüsü
    │   ├── _genel_ozet()               # Toplam harcama özeti
    │   ├── _market_analizi()           # Markete göre analiz
    │   ├── _aylik_analiz()             # Aylık trend analizi
    │   └── _populer_urunler()          # En çok alınan ürünler
    │
    └── 💾 Veri Yönetimi
        └── veri_disa_aktar()           # CSV export

def ana_menu():                          # Ana program döngüsü
```

## 📊 Veri Modeli

### JSON Veri Yapısı

```json
{
  "fisler": [
    {
      "id": 1,
      "market": "Migros",
      "tarih": "15.02.2026",
      "urunler": [
        {
          "ad": "Süt",
          "miktar": 2.0,
          "birim": "lt",
          "fiyat": 48.0,
          "birim_fiyat": 24.0
        }
      ],
      "toplam": 131.0,
      "kayit_zamani": "2026-02-15T10:30:00"
    }
  ],
  "urunler": {
    "Süt": {
      "Migros": [...],
      "A101": [...]
    }
  },
  "marketler": {
    "Migros": {
      "toplam_alisveris": 5,
      "toplam_harcama": 750.25,
      "urun_sayisi": 15
    }
  }
}
```

## 🎨 Kullanıcı Arayüzü Akışı

```
Program Başlangıcı
        ↓
    Ana Menü
    ┌─────────────────────┐
    │ 1. Fiş Ekle         │
    │ 2. Fiyat Karşılaştır│
    │ 3. Harcama Analizi  │
    │ 4. Fişleri Listele  │
    │ 5. CSV Export       │
    │ 6. Çıkış           │
    └─────────────────────┘
            ↓
    ┌──────────┴──────────┐
    ↓                      ↓
Fiş Ekle            Fiyat Karşılaştır
    ↓                      ↓
Market Adı          Ürün Seçimi
    ↓                      ↓
Tarih               Karşılaştırma Sonucu
    ↓                      ↓
Ürünler             En Ucuz/Pahalı
    ↓                      ↓
Kaydet              Fark Analizi
```

## 🔐 Güvenlik ve Gizlilik

- ✅ Tüm veriler yerel olarak saklanır
- ✅ İnternet bağlantısı gerektirmez
- ✅ Kişisel veriler dışarıya aktarılmaz
- ✅ Açık kaynak - kod tamamen görülebilir

## 🚀 Performans

- **Hafıza**: ~10-20 MB
- **Dosya Boyutu**: ~15 KB (program)
- **Veri Boyutu**: ~1-5 MB (1000+ fiş için)
- **Hız**: Anlık yanıt (<1 saniye)

## 📈 İstatistikler

| Özellik | Detay |
|---------|-------|
| Kod Satırı | ~500 satır |
| Fonksiyon Sayısı | 15+ fonksiyon |
| Desteklenen Format | JSON, CSV |
| Dil Desteği | Türkçe |
| Platform | Cross-platform |

## 🔄 Güncellenme Geçmişi

### v1.0.0 (İlk Sürüm)
- ✅ Temel fiş yönetimi
- ✅ Fiyat karşılaştırma
- ✅ Harcama analizi
- ✅ CSV export
- ✅ Kapsamlı dokümantasyon

### İleride Eklenebilecekler
- [ ] Grafik görselleştirme
- [ ] Web arayüzü
- [ ] Mobil uygulama
- [ ] OCR fiş okuma
- [ ] Bulut senkronizasyon

## 💻 Sistem Gereksinimleri

### Minimum
- Python 3.6+
- 50 MB boş disk alanı
- 512 MB RAM

### Önerilen
- Python 3.8+
- 100 MB boş disk alanı
- 1 GB RAM

## 📞 Destek

- **Dokümantasyon**: README.md
- **Hızlı Başlangıç**: QUICKSTART.md
- **Katkıda Bulunma**: CONTRIBUTING.md
- **Sorunlar**: GitHub Issues

---

**Not**: Bu yapı esnek ve genişletilebilir şekilde tasarlanmıştır.
