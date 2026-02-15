# 🛒 Market Fiyat Karşılaştırma ve Harcama Analizi Sistemi

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/status-active-success)

Aileler için geliştirilmiş kapsamlı market alışverişi yönetim ve analiz programı. Alışveriş fişlerinizi kaydedin, marketler arası fiyatları karşılaştırın ve harcamalarınızı detaylı analiz edin!

---

## 🎯 Proje Amacı

Her ailenin yaşadığı ortak problem: **"Hangi markette hangi ürün daha ucuz?"**

Bu program ile:
- ✅ Market market fiyatları kolayca karşılaştırın
- ✅ En uygun fiyatları bulun ve tasarruf edin
- ✅ Aylık harcamalarınızı takip edin
- ✅ Hangi üründe ne kadar harcadığınızı görün
- ✅ Veriye dayalı alışveriş kararları alın

## ✨ Özellikler

### 📝 Fiş Yönetimi
- Detaylı fiş girişi (market adı, tarih, ürünler, fiyatlar)
- Ürün bazında miktar ve birim takibi (adet, kg, lt)
- Otomatik birim fiyat hesaplama
- Kolay ve hızlı veri girişi

### 💰 Fiyat Karşılaştırma
- Market market fiyat karşılaştırması
- En ucuz ve en pahalı marketleri gösterir
- Ortalama fiyat hesaplama
- Fiyat farkı analizi (TL ve % olarak)
- Geçmiş fiyat takibi

### 📊 Kapsamlı Harcama Analizi
- **Genel Özet**: Toplam harcama, ortalama fiş tutarı, toplam alışveriş sayısı
- **Markete Göre Analiz**: Hangi markette ne kadar harcandığı
- **Aylık Analiz**: Aylık harcama trendleri ve günlük ortalamalar
- **Popüler Ürünler**: En çok alınan ürünler ve harcama dağılımı

### 💾 Veri Yönetimi
- Otomatik JSON formatında veri kaydetme
- CSV formatında raporlama
- Veri bütünlüğü ve kolay yedekleme

## 🚀 Kurulum

### Gereksinimler
- Python 3.6 veya üzeri
- Ek kütüphane gerektirmez (sadece standart Python kütüphaneleri)

### Adım Adım Kurulum

1. **Projeyi İndirin**
```bash
git clone https://github.com/[kullanici-adi]/market-analiz.git
cd market-analiz
```

2. **Programı Çalıştırın**
```bash
python market_analiz.py
```

veya Linux/Mac'te:
```bash
chmod +x market_analiz.py
./market_analiz.py
```

## 📖 Kullanım Kılavuzu

### 1️⃣ Yeni Fiş Ekleme

Program ilk açıldığında ana menüden "1" seçeneğini seçin:

```
1. Market adını girin (örn: Migros, A101, ŞOK)
2. Tarihi girin veya bugünün tarihi için Enter'a basın
3. Ürün bilgilerini girin:
   - Ürün adı
   - Miktar (örn: 2, 1.5)
   - Fiyat (TL)
   - Birim (adet, kg, lt)
4. Tüm ürünler bitince 'q' yazıp Enter'a basın
```

**Örnek Fiş Girişi:**
```
Market adı: Migros
Tarih: 15.02.2026
Ürün adı: Süt
Miktar: 2
Fiyat: 45.50
Birim: lt

Ürün adı: Ekmek
Miktar: 3
Fiyat: 15.00
Birim: adet
```

### 2️⃣ Fiyat Karşılaştırma

Aynı ürünün farklı marketlerdeki fiyatlarını karşılaştırın:

```
1. Ana menüden "2" seçeneğini seçin
2. Listeden karşılaştırmak istediğiniz ürünü seçin
3. Sonuçları inceleyin:
   - 🥇 En ucuz market
   - 🥈 İkinci en ucuz market
   - 🥉 Üçüncü en ucuz market
   - Fiyat farkları ve yüzdelik oranlar
```

### 3️⃣ Harcama Analizi

Detaylı harcama raporları oluşturun:

**Genel Özet:**
- Toplam ne kadar harcandığı
- Kaç fiş girildiği
- Ortalama fiş tutarı
- Toplam ürün sayısı

**Markete Göre Analiz:**
- Her marketten ne kadar alışveriş yapıldığı
- Market bazında harcama dağılımı
- Ortalama fiş tutarları

**Aylık Analiz:**
- Ay ay harcama trendleri
- Günlük ortalama harcamalar
- Dönemsel karşılaştırmalar

**Popüler Ürünler:**
- En çok alınan 20 ürün
- Ürün bazında toplam harcamalar
- Alım sıklıkları

### 4️⃣ Veri Dışa Aktarma

Tüm verilerinizi CSV formatında Excel'de açabilecek şekilde dışa aktarın:

```
1. Ana menüden "5" seçeneğini seçin
2. Otomatik olarak "market_rapor_[tarih_saat].csv" dosyası oluşturulur
3. Bu dosyayı Excel veya LibreOffice ile açabilirsiniz
```

## 📁 Veri Yapısı

Program, verilerinizi `market_verileri.json` dosyasında saklar:

```json
{
  "fisler": [
    {
      "id": 1,
      "market": "Migros",
      "tarih": "15.02.2026",
      "urunler": [...],
      "toplam": 150.50
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
      "toplam_harcama": 750.25
    }
  }
}
```

## 💡 Kullanım Senaryoları

### Senaryo 1: Haftalık Market Alışverişi
```
1. Her market alışverişinden sonra fişi programa girin
2. Hafta sonunda "Harcama Analizi" ile ne kadar harcadığınızı görün
3. "Fiyat Karşılaştırma" ile hangi üründe hangi market daha uygun öğrenin
```

### Senaryo 2: Aylık Bütçe Takibi
```
1. Ay boyunca tüm fişleri düzenli girin
2. Ay sonunda "Aylık Analiz" raporu çıkarın
3. Hangi kategoride (ürünlerde) fazla harcama yaptığınızı görün
4. Bir sonraki ay için bütçe planı yapın
```

### Senaryo 3: En Ucuz Market Bulma
```
1. Aynı ürünleri farklı marketlerden alırken her seferinde kaydedin
2. "Fiyat Karşılaştırma" ile en ucuz marketi tespit edin
3. Düzenli alınan ürünler için en uygun marketi belirleyin
```

## 🎯 İpuçları

- ✅ **Düzenli Giriş**: Alışverişten hemen sonra fişi girin, unutmayın
- ✅ **Tutarlı İsimlendirme**: Ürün isimlerini her zaman aynı şekilde yazın (örn: "Süt" vs "süt")
- ✅ **Birim Takibi**: Birim fiyat karşılaştırması için birimleri doğru girin
- ✅ **Yedekleme**: `market_verileri.json` dosyasını düzenli yedekleyin
- ✅ **CSV Raporları**: Önemli analizler için CSV raporu alıp saklayın

## 🔧 Gelişmiş Özellikler (İleride Eklenebilir)

- [ ] Grafik ve görselleştirme
- [ ] Mobil uygulama desteği
- [ ] Fiş fotoğrafından otomatik veri çekme (OCR)
- [ ] Bütçe uyarı sistemi
- [ ] Alışveriş listesi önerileri
- [ ] Fiyat trend tahminleri
- [ ] Çoklu kullanıcı desteği
- [ ] Kategori bazlı analiz

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak isterseniz:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: ...'`)
4. Branch'inizi push edin (`git push origin yeni-ozellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📧 İletişim

Sorularınız, önerileriniz veya hata bildirimleri için:
- GitHub Issues kullanın
- Pull Request gönderin

## 🙏 Teşekkürler

Bu programı kullanarak market alışverişlerinizde tasarruf etmenizi ve bütçenizi daha iyi yönetmenizi umuyoruz!

---

**Not**: Bu program aileler için geliştirilmiştir ve hiçbir kişisel veri dışarıya aktarılmaz. Tüm veriler bilgisayarınızda yerel olarak saklanır.

## 🎬 Örnek Ekran Görüntüleri

### Ana Menü
```
============================================================
               MARKET ANALİZ SİSTEMİ
============================================================

1. 📝 Yeni Fiş Ekle
2. 💰 Fiyat Karşılaştır
3. 📊 Harcama Analizi
4. 📋 Fişleri Listele
5. 💾 Verileri Dışa Aktar (CSV)
6. ❌ Çıkış
```

### Fiyat Karşılaştırma Sonucu
```
============================================================
ÜRÜN: Süt
============================================================

Market              Son Fiyat       Ortalama       Son Tarih       Kayıt
--------------------------------------------------------------------------------
🥇 A101              22.50 TL/lt    23.00 TL/lt    15.02.2026      3x
🥈 ŞOK               23.90 TL/lt    24.50 TL/lt    14.02.2026      2x
🥉 Migros            24.50 TL/lt    24.20 TL/lt    15.02.2026      4x

--------------------------------------------------------------------------------
💰 En Ucuz: A101 - 22.50 TL
💸 En Pahalı: Migros - 24.50 TL
📊 Fark: 2.00 TL (%8.9)
```

## ⚡ Hızlı Başlangıç

```bash
# Projeyi klonlayın
git clone https://github.com/[kullanici-adi]/market-analiz.git
cd market-analiz

# Programı çalıştırın
python market_analiz.py

# İlk fişinizi ekleyin ve tasarruf etmeye başlayın!
```
