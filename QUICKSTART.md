# ⚡ Hızlı Başlangıç Rehberi

5 dakikada Market Analiz Sistemi'ni kullanmaya başlayın!

## 🚀 1. Kurulum (30 saniye)

```bash
# Projeyi indirin
git clone https://github.com/[kullanici-adi]/market-analiz.git
cd market-analiz

# Programı çalıştırın
python market_analiz.py
```

**Gereksinimler**: Sadece Python 3.6+ yeterli!

## 📝 2. İlk Fişinizi Ekleyin (2 dakika)

Program açıldığında:

1. **Ana menüden `1` seçin** (Yeni Fiş Ekle)

2. **Market bilgilerini girin:**
```
Market adı: Migros
Tarih: [Enter tuşuna basın - bugünün tarihi otomatik gelir]
```

3. **Ürünleri ekleyin:**
```
Ürün adı: Süt
Miktar: 2
Fiyat: 48
Birim: lt

Ürün adı: Ekmek  
Miktar: 3
Fiyat: 18
Birim: adet

Ürün adı: q  [bitirmek için]
```

4. **Fiş kaydedildi!** ✅

## 💰 3. Fiyatları Karşılaştırın (1 dakika)

1. **Ana menüden `2` seçin** (Fiyat Karşılaştır)

2. **Örneğin "Süt" ürününü seçin**

3. **Sonuçları görün:**
   - Hangi market en ucuz? 🥇
   - Ne kadar tasarruf edebilirsiniz? 💰
   - Ortalama fiyat nedir? 📊

## 📊 4. Harcamalarınızı Analiz Edin (1 dakika)

1. **Ana menüden `3` seçin** (Harcama Analizi)

2. **İstediğiniz analizi seçin:**
   - `1` → Genel özet (toplam harcama, ortalama)
   - `2` → Markete göre (hangi markette ne kadar?)
   - `3` → Aylık analiz (ay ay harcama)
   - `4` → Popüler ürünler (en çok ne alıyorsunuz?)

## 🎯 İpuçları

### ✅ Başarılı Kullanım İçin

1. **Düzenli Kayıt**: Her alışverişten sonra fişi girin
2. **Tutarlı İsimler**: Ürün isimlerini aynı yazın
   - ✅ "Süt" → "Süt" → "Süt" 
   - ❌ "Süt" → "süt" → "SÜT"
3. **Doğru Birimler**: kg, lt, adet olarak yazın

### 🎬 Örnek Senaryo

**Haftalık Market Alışverişi:**

```
Pazartesi: A101'den alışveriş → Fişi gir
Çarşamba: Migros'tan alışveriş → Fişi gir
Cuma: ŞOK'tan alışveriş → Fişi gir
Pazar: "Fiyat Karşılaştır" → En ucuz market?
```

## 📱 Örnek Kullanım

### Fiş Ekleme Akışı
```
============================================================
YENİ ALIŞVERİŞ FİŞİ EKLEME
============================================================
Market adı: A101
Tarih: 15.02.2026

--- Ürün #1 ---
Ürün adı: Süt
Miktar: 2
Fiyat: 45
Birim: lt
✓ Eklendi: Süt - 2.0 lt - 45.00 TL (Birim: 22.50 TL)

--- Ürün #2 ---
Ürün adı: q

============================================================
✅ Fiş başarıyla kaydedildi!
Market: A101
Tarih: 15.02.2026
Toplam Ürün: 1
Toplam Tutar: 45.00 TL
============================================================
```

### Fiyat Karşılaştırma Sonucu
```
============================================================
ÜRÜN: Süt
============================================================

Market              Son Fiyat       Ortalama       Son Tarih       Kayıt
--------------------------------------------------------------------------------
🥇 A101              22.50 TL/lt    22.50 TL/lt    15.02.2026      1x
🥈 ŞOK               23.90 TL/lt    23.90 TL/lt    13.02.2026      1x
🥉 Migros            24.00 TL/lt    24.00 TL/lt    10.02.2026      1x

--------------------------------------------------------------------------------
💰 En Ucuz: A101 - 22.50 TL
💸 En Pahalı: Migros - 24.00 TL
📊 Fark: 1.50 TL (%6.7)
```

## 🎁 Bonus: Örnek Veri ile Test

Programı önce denemek isterseniz:

```bash
# Örnek veriyi kopyalayın
cp ornek_veri.json market_verileri.json

# Programı çalıştırın
python market_analiz.py

# Hazır verilerle fiyat karşılaştırma ve analiz yapın!
```

## ❓ Sık Sorulan Sorular

**S: Veriler nerede saklanıyor?**
A: Aynı klasörde `market_verileri.json` dosyasında

**S: Verileri yedekleyebilir miyim?**
A: Evet! `market_verileri.json` dosyasını kopyalayın

**S: CSV raporu nasıl alırım?**
A: Ana menüden `5` seçin, otomatik CSV oluşturulur

**S: Ürün ismini yanlış yazdım, düzeltebilir miyim?**
A: `market_verileri.json` dosyasını metin editörü ile düzeltebilirsiniz

**S: Kaç market ekleyebilirim?**
A: Sınırsız! İstediğiniz kadar market ekleyebilirsiniz

**S: Mobil uygulaması var mı?**
A: Şu an sadece bilgisayar sürümü var, ileride eklenebilir

## 🆘 Yardım

- **Detaylı rehber**: `README.md` dosyasını okuyun
- **Hata bildirimi**: GitHub Issues açın
- **Katkıda bulunun**: `CONTRIBUTING.md` dosyasına bakın

## 🎉 Başarılar!

Artık market alışverişlerinizde tasarruf etmeye hazırsınız! 

**İlk hedefiniz**: 10 fiş ekleyip fiyat karşılaştırması yapın 🎯

---

💡 **İpucu**: Ayda 100-300 TL tasarruf edebilirsiniz!
