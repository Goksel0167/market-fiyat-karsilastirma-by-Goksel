# Katkıda Bulunma Rehberi

Market Analiz Sistemi projesine katkıda bulunmak istediğiniz için teşekkür ederiz! 🎉

## Nasıl Katkıda Bulunabilirsiniz?

### 1. Hata Bildirimi (Bug Report)

Bir hata bulduysanız:
- GitHub Issues'da yeni bir issue açın
- Hatayı açık bir şekilde tanımlayın
- Hatayı nasıl tekrarlayabileceğimizi anlatın
- Sistemlerinizin bilgisini ekleyin (Python versiyonu, işletim sistemi)

### 2. Özellik Önerisi (Feature Request)

Yeni bir özellik önerisi için:
- GitHub Issues'da yeni bir issue açın
- "Feature Request" etiketi ekleyin
- Özelliği detaylı açıklayın
- Neden faydalı olacağını anlatın

### 3. Kod Katkısı (Pull Request)

#### Adım 1: Repository'yi Fork Edin
```bash
# GitHub'da "Fork" butonuna tıklayın
# Kendi hesabınıza fork'ladıktan sonra:
git clone https://github.com/[kullanici-adi]/market-analiz.git
cd market-analiz
```

#### Adım 2: Yeni Bir Branch Oluşturun
```bash
git checkout -b yeni-ozellik-ismi
```

Branch isimlendirme örnekleri:
- `feature/grafik-gosterim` - Yeni özellik için
- `fix/fiyat-hesaplama` - Hata düzeltme için
- `docs/kullanim-kilavuzu` - Dokümantasyon için

#### Adım 3: Değişikliklerinizi Yapın

Kod yazarken dikkat edilmesi gerekenler:
- Python PEP 8 standartlarına uyun
- Türkçe açıklama ve değişken isimleri kullanın
- Yorum satırları ekleyin
- Kodunuzu test edin

#### Adım 4: Commit Edin
```bash
git add .
git commit -m "Özellik: Grafik gösterimi eklendi"
```

Commit mesajı örnekleri:
- `Özellik: Excel export özelliği eklendi`
- `Düzeltme: Fiyat karşılaştırma hatası giderildi`
- `Dokümantasyon: README güncellendi`

#### Adım 5: Push Edin ve PR Oluşturun
```bash
git push origin yeni-ozellik-ismi
```

GitHub'da repository'nize gidin ve "Pull Request" oluşturun.

## Kod Standartları

### Python Stil Rehberi

```python
# İyi örnek
def fiyat_hesapla(miktar, birim_fiyat):
    """Toplam fiyatı hesapla"""
    return miktar * birim_fiyat

# Kötü örnek
def f(m,b):
    return m*b
```

### Değişken İsimlendirme
- Türkçe ve anlaşılır isimler kullanın
- Snake_case formatında yazın
- Açıklayıcı olsun

```python
# İyi
toplam_harcama = 0
urun_listesi = []

# Kötü
thc = 0
ul = []
```

### Fonksiyon Dokümantasyonu
```python
def fiyat_karsilastir(urun_adi, marketler):
    """
    Ürün fiyatlarını marketler arası karşılaştır
    
    Args:
        urun_adi (str): Karşılaştırılacak ürün adı
        marketler (list): Market listesi
    
    Returns:
        dict: Karşılaştırma sonuçları
    """
    # Kod...
```

## Test Etme

Değişikliklerinizi test edin:

```bash
# Programı çalıştırın
python market_analiz.py

# Temel işlevleri test edin:
# 1. Yeni fiş ekleyin
# 2. Fiyat karşılaştırma yapın
# 3. Analiz raporu oluşturun
```

## Pull Request Süreci

1. **PR Açıklaması**: Değişikliklerinizi detaylı açıklayın
2. **Screenshot**: Görsel değişiklikler varsa ekran görüntüsü ekleyin
3. **Test**: Nasıl test edildiğini yazın
4. **İlgili Issue**: Varsa issue numarasını belirtin (#123)

### PR Template

```markdown
## Değişiklik Özeti
[Kısaca ne değişti]

## Değişiklik Tipi
- [ ] Yeni özellik
- [ ] Hata düzeltme
- [ ] Dokümantasyon
- [ ] Performans iyileştirmesi

## Test Edildi mi?
- [ ] Evet, şu şekilde test edildi: [açıklama]
- [ ] Hayır

## Ekran Görüntüleri (varsa)
[Görsel ekleyin]

## İlgili Issue
Closes #[issue numarası]
```

## İyi Pratikler

### ✅ Yapılması Gerekenler
- Küçük ve odaklanmış PR'lar açın
- Açıklayıcı commit mesajları yazın
- Kod okumaya özen gösterin
- Test edin
- Dokümantasyon güncelleyin

### ❌ Yapılmaması Gerekenler
- Büyük ve karmaşık PR'lar açmayın
- Biçimlendirme değişiklikleriyle özellik değişikliklerini karıştırmayın
- Test edilmemiş kod göndermeyİn
- Mevcut kodu bozmayın

## Geliştirme Ortamı Kurulumu

```bash
# Repository'yi klonlayın
git clone https://github.com/[kullanici-adi]/market-analiz.git
cd market-analiz

# Virtual environment oluşturun (opsiyonel)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Programı test edin
python market_analiz.py
```

## Yardım ve İletişim

- **Sorularınız için**: GitHub Discussions kullanın
- **Hata bildirimi**: GitHub Issues açın
- **Özellik önerisi**: GitHub Issues açın

## Davranış Kuralları

- Saygılı ve yapıcı olun
- Farklı fikirlere açık olun
- Yardımsever bir topluluk oluşturalım
- Herkesin katkısına değer verin

## İleride Eklenebilecek Özellikler

Üzerinde çalışılabilecek fikirler:

### Öncelikli
- [ ] Grafik görselleştirme (matplotlib)
- [ ] Excel export (openpyxl)
- [ ] Kategori sistemi (gıda, temizlik, vb.)
- [ ] Bütçe uyarı sistemi

### Orta Öncelik
- [ ] Mobil uygulama (React Native)
- [ ] Web arayüzü (Flask/Django)
- [ ] Fiş OCR özelliği
- [ ] Fiyat trend tahminleri

### Uzun Vadeli
- [ ] Çoklu kullanıcı desteği
- [ ] Cloud senkronizasyon
- [ ] AI tabanlı alışveriş önerileri
- [ ] Market indirim takibi

## Teşekkürler! 🙏

Her türlü katkınız için teşekkür ederiz. Birlikte daha iyi bir program geliştirelim!
