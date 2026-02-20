#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Market Fiyat Karşılaştırma ve Harcama Analizi Programı
Aileler için kapsamlı market alışverişi yönetim sistemi
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import statistics

class MarketAnaliz:
    def __init__(self, veri_dosyasi="market_verileri.json"):
        self.veri_dosyasi = veri_dosyasi
        self.veriler = self.verileri_yukle()
        
    def verileri_yukle(self):
        """Kaydedilmiş verileri yükle"""
        if os.path.exists(self.veri_dosyasi):
            try:
                with open(self.veri_dosyasi, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"fisler": [], "urunler": {}, "marketler": {}}
        return {"fisler": [], "urunler": {}, "marketler": {}}
    
    def verileri_kaydet(self):
        """Verileri dosyaya kaydet"""
        with open(self.veri_dosyasi, 'w', encoding='utf-8') as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=2)
    
    def fis_ekle(self):
        """Yeni alışveriş fişi ekle"""
        print("\n" + "="*60)
        print("YENİ ALIŞ VERİŞ FİŞİ EKLEME")
        print("="*60)
        
        market_adi = input("Market adı: ").strip().title()
        tarih = input("Tarih (GG.AA.YYYY) [Enter=bugün]: ").strip()
        
        if not tarih:
            tarih = datetime.now().strftime("%d.%m.%Y")
        
        print("\nÜrünleri ekleyin (bitirmek için ürün adı yerine 'q' yazın):")
        
        urunler = []
        toplam = 0
        
        while True:
            print(f"\n--- Ürün #{len(urunler) + 1} ---")
            urun_adi = input("Ürün adı: ").strip()
            
            if urun_adi.lower() == 'q':
                break
            
            if not urun_adi:
                continue
            
            try:
                miktar = float(input("Miktar (adet/kg): "))
                fiyat = float(input("Fiyat (TL): "))
                birim = input("Birim (adet/kg/lt) [Enter=adet]: ").strip().lower() or "adet"
                
                birim_fiyat = fiyat / miktar if miktar > 0 else fiyat
                
                urunler.append({
                    "ad": urun_adi.title(),
                    "miktar": miktar,
                    "birim": birim,
                    "fiyat": fiyat,
                    "birim_fiyat": birim_fiyat
                })
                
                toplam += fiyat
                print(f"✓ Eklendi: {urun_adi} - {miktar} {birim} - {fiyat:.2f} TL (Birim: {birim_fiyat:.2f} TL)")
                
            except ValueError:
                print("❌ Hatalı giriş! Lütfen sayısal değer girin.")
        
        if not urunler:
            print("\n❌ Hiç ürün eklenmedi, fiş kaydedilmedi.")
            return
        
        # Fiş bilgilerini kaydet
        fis = {
            "id": len(self.veriler["fisler"]) + 1,
            "market": market_adi,
            "tarih": tarih,
            "urunler": urunler,
            "toplam": toplam,
            "kayit_zamani": datetime.now().isoformat()
        }
        
        self.veriler["fisler"].append(fis)
        
        # Ürün ve market verilerini güncelle
        self._urun_verilerini_guncelle(market_adi, tarih, urunler)
        
        self.verileri_kaydet()
        
        print("\n" + "="*60)
        print(f"✅ Fiş başarıyla kaydedildi!")
        print(f"Market: {market_adi}")
        print(f"Tarih: {tarih}")
        print(f"Toplam Ürün: {len(urunler)}")
        print(f"Toplam Tutar: {toplam:.2f} TL")
        print("="*60)
    
    def _urun_verilerini_guncelle(self, market, tarih, urunler):
        """Ürün ve market istatistiklerini güncelle"""
        for urun in urunler:
            urun_adi = urun["ad"]
            
            # Ürün veritabanını güncelle
            if urun_adi not in self.veriler["urunler"]:
                self.veriler["urunler"][urun_adi] = {}
            
            if market not in self.veriler["urunler"][urun_adi]:
                self.veriler["urunler"][urun_adi][market] = []
            
            self.veriler["urunler"][urun_adi][market].append({
                "tarih": tarih,
                "fiyat": urun["fiyat"],
                "birim_fiyat": urun["birim_fiyat"],
                "miktar": urun["miktar"],
                "birim": urun["birim"]
            })
            
            # Market veritabanını güncelle
            if market not in self.veriler["marketler"]:
                self.veriler["marketler"][market] = {
                    "toplam_alisveris": 0,
                    "toplam_harcama": 0,
                    "urun_sayisi": 0
                }
            
            self.veriler["marketler"][market]["toplam_alisveris"] += 1
            self.veriler["marketler"][market]["toplam_harcama"] += urun["fiyat"]
            self.veriler["marketler"][market]["urun_sayisi"] += 1
    
    def fiyat_karsilastir(self):
        """Ürün fiyatlarını marketler arası karşılaştır"""
        if not self.veriler["urunler"]:
            print("\n❌ Henüz ürün verisi yok.")
            return
        
        print("\n" + "="*60)
        print("FİYAT KARŞILAŞTIRMA")
        print("="*60)
        
        # Ürün listesini göster
        urunler = sorted(self.veriler["urunler"].keys())
        print("\nKayıtlı Ürünler:")
        for i, urun in enumerate(urunler, 1):
            print(f"{i}. {urun}")
        
        try:
            secim = int(input("\nKarşılaştırmak istediğiniz ürünün numarasını girin: "))
            if secim < 1 or secim > len(urunler):
                print("❌ Geçersiz seçim!")
                return
            
            urun_adi = urunler[secim - 1]
            urun_verileri = self.veriler["urunler"][urun_adi]
            
            print(f"\n{'='*60}")
            print(f"ÜRÜN: {urun_adi}")
            print(f"{'='*60}\n")
            
            karsilastirma = []
            
            for market, kayitlar in urun_verileri.items():
                if kayitlar:
                    son_kayit = kayitlar[-1]  # En son kayıt
                    ortalama = statistics.mean([k["birim_fiyat"] for k in kayitlar])
                    
                    karsilastirma.append({
                        "market": market,
                        "son_fiyat": son_kayit["birim_fiyat"],
                        "ortalama": ortalama,
                        "kayit_sayisi": len(kayitlar),
                        "son_tarih": son_kayit["tarih"],
                        "birim": son_kayit["birim"]
                    })
            
            # Fiyata göre sırala
            karsilastirma.sort(key=lambda x: x["son_fiyat"])
            
            print(f"{'Market':<20} {'Son Fiyat':<15} {'Ortalama':<15} {'Son Tarih':<15} {'Kayıt'}")
            print("-" * 80)
            
            for i, k in enumerate(karsilastirma, 1):
                ikon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                print(f"{ikon} {k['market']:<18} {k['son_fiyat']:.2f} TL/{k['birim']:<5} "
                      f"{k['ortalama']:.2f} TL/{k['birim']:<5} {k['son_tarih']:<15} {k['kayit_sayisi']}x")
            
            # En ucuz ve en pahalı fark
            if len(karsilastirma) > 1:
                fark = karsilastirma[-1]["son_fiyat"] - karsilastirma[0]["son_fiyat"]
                fark_yuzde = (fark / karsilastirma[0]["son_fiyat"]) * 100
                
                print("\n" + "-" * 80)
                print(f"💰 En Ucuz: {karsilastirma[0]['market']} - {karsilastirma[0]['son_fiyat']:.2f} TL")
                print(f"💸 En Pahalı: {karsilastirma[-1]['market']} - {karsilastirma[-1]['son_fiyat']:.2f} TL")
                print(f"📊 Fark: {fark:.2f} TL (%{fark_yuzde:.1f})")
                
        except (ValueError, IndexError):
            print("❌ Geçersiz giriş!")
    
    def harcama_analizi(self):
        """Detaylı harcama analizi"""
        if not self.veriler["fisler"]:
            print("\n❌ Henüz fiş verisi yok.")
            return
        
        print("\n" + "="*60)
        print("HARCAMA ANALİZİ")
        print("="*60)
        
        print("\n1. Genel Özet")
        print("2. Markete Göre Analiz")
        print("3. Aylık Analiz")
        print("4. En Çok Alınan Ürünler")
        
        try:
            secim = input("\nSeçiminiz (1-4): ").strip()
            
            if secim == "1":
                self._genel_ozet()
            elif secim == "2":
                self._market_analizi()
            elif secim == "3":
                self._aylik_analiz()
            elif secim == "4":
                self._populer_urunler()
            else:
                print("❌ Geçersiz seçim!")
                
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    def _genel_ozet(self):
        """Genel harcama özeti"""
        toplam_fis = len(self.veriler["fisler"])
        toplam_harcama = sum(fis["toplam"] for fis in self.veriler["fisler"])
        ortalama_fis = toplam_harcama / toplam_fis if toplam_fis > 0 else 0
        
        toplam_urun = sum(len(fis["urunler"]) for fis in self.veriler["fisler"])
        
        print(f"\n{'='*60}")
        print("GENEL ÖZET")
        print(f"{'='*60}")
        print(f"📋 Toplam Fiş Sayısı: {toplam_fis}")
        print(f"💰 Toplam Harcama: {toplam_harcama:.2f} TL")
        print(f"📊 Ortalama Fiş Tutarı: {ortalama_fis:.2f} TL")
        print(f"🛒 Toplam Ürün Alımı: {toplam_urun}")
        print(f"🏪 Alışveriş Yapılan Market Sayısı: {len(self.veriler['marketler'])}")
    
    def _market_analizi(self):
        """Markete göre harcama analizi"""
        print(f"\n{'='*60}")
        print("MARKETE GÖRE HARCAMA ANALİZİ")
        print(f"{'='*60}\n")
        
        market_harcanmalar = defaultdict(float)
        market_fis_sayisi = defaultdict(int)
        
        for fis in self.veriler["fisler"]:
            market_harcanmalar[fis["market"]] += fis["toplam"]
            market_fis_sayisi[fis["market"]] += 1
        
        # Harcamaya göre sırala
        sirali = sorted(market_harcanmalar.items(), key=lambda x: x[1], reverse=True)
        
        print(f"{'Market':<20} {'Toplam Harcama':<20} {'Fiş Sayısı':<15} {'Ortalama Fiş'}")
        print("-" * 75)
        
        for market, harcama in sirali:
            fis_sayisi = market_fis_sayisi[market]
            ortalama = harcama / fis_sayisi
            print(f"{market:<20} {harcama:>15.2f} TL {fis_sayisi:>13} {ortalama:>15.2f} TL")
        
        print("-" * 75)
        print(f"{'TOPLAM':<20} {sum(market_harcanmalar.values()):>15.2f} TL")
    
    def _aylik_analiz(self):
        """Aylık harcama analizi"""
        print(f"\n{'='*60}")
        print("AYLIK HARCAMA ANALİZİ")
        print(f"{'='*60}\n")
        
        aylik_harcama = defaultdict(float)
        aylik_fis = defaultdict(int)
        
        for fis in self.veriler["fisler"]:
            try:
                tarih_parcalari = fis["tarih"].split(".")
                if len(tarih_parcalari) == 3:
                    ay_yil = f"{tarih_parcalari[1]}.{tarih_parcalari[2]}"
                    aylik_harcama[ay_yil] += fis["toplam"]
                    aylik_fis[ay_yil] += 1
            except:
                continue
        
        sirali = sorted(aylik_harcama.items())
        
        print(f"{'Ay/Yıl':<15} {'Harcama':<20} {'Fiş Sayısı':<15} {'Günlük Ort.'}")
        print("-" * 70)
        
        for ay_yil, harcama in sirali:
            fis_sayisi = aylik_fis[ay_yil]
            # Basit 30 günlük ortalama
            gunluk = harcama / 30
            print(f"{ay_yil:<15} {harcama:>15.2f} TL {fis_sayisi:>13} {gunluk:>15.2f} TL")
    
    def _populer_urunler(self):
        """En çok alınan ürünleri listele"""
        print(f"\n{'='*60}")
        print("EN ÇOK ALINAN ÜRÜNLER")
        print(f"{'='*60}\n")
        
        urun_alinma = defaultdict(int)
        urun_harcama = defaultdict(float)
        
        for fis in self.veriler["fisler"]:
            for urun in fis["urunler"]:
                urun_alinma[urun["ad"]] += 1
                urun_harcama[urun["ad"]] += urun["fiyat"]
        
        # Alınma sayısına göre sırala
        sirali = sorted(urun_alinma.items(), key=lambda x: x[1], reverse=True)[:20]
        
        print(f"{'#':<5} {'Ürün':<30} {'Alım Sayısı':<15} {'Toplam Harcama'}")
        print("-" * 75)
        
        for i, (urun, alinma) in enumerate(sirali, 1):
            harcama = urun_harcama[urun]
            print(f"{i:<5} {urun:<30} {alinma:>12} {harcama:>18.2f} TL")
    
    def fisler_listele(self):
        """Tüm fişleri listele"""
        if not self.veriler["fisler"]:
            print("\n❌ Henüz fiş yok.")
            return
        
        print("\n" + "="*60)
        print("TÜM FİŞLER")
        print("="*60 + "\n")
        
        for fis in reversed(self.veriler["fisler"][-20:]):  # Son 20 fiş
            print(f"Fiş #{fis['id']} - {fis['market']} - {fis['tarih']}")
            print(f"Toplam: {fis['toplam']:.2f} TL - Ürün Sayısı: {len(fis['urunler'])}")
            print("-" * 60)
    
    def veri_disa_aktar(self):
        """Verileri CSV formatında dışa aktar"""
        if not self.veriler["fisler"]:
            print("\n❌ Dışa aktarılacak veri yok.")
            return
        
        dosya_adi = f"market_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            f.write("Fiş ID,Market,Tarih,Ürün,Miktar,Birim,Fiyat,Birim Fiyat\n")
            
            for fis in self.veriler["fisler"]:
                for urun in fis["urunler"]:
                    f.write(f"{fis['id']},{fis['market']},{fis['tarih']},"
                           f"{urun['ad']},{urun['miktar']},{urun['birim']},"
                           f"{urun['fiyat']:.2f},{urun['birim_fiyat']:.2f}\n")
        
        print(f"\n✅ Veriler başarıyla dışa aktarıldı: {dosya_adi}")


def ana_menu():
    """Ana menü"""
    analiz = MarketAnaliz()
    
    while True:
        print("\n" + "="*60)
        print(" " * 15 + "MARKET ANALİZ SİSTEMİ")
        print("="*60)
        print("\n1. 📝 Yeni Fiş Ekle")
        print("2. 💰 Fiyat Karşılaştır")
        print("3. 📊 Harcama Analizi")
        print("4. 📋 Fişleri Listele")
        print("5. 💾 Verileri Dışa Aktar (CSV)")
        print("6. ❌ Çıkış")
        
        secim = input("\nSeçiminiz (1-6): ").strip()
        
        if secim == "1":
            analiz.fis_ekle()
        elif secim == "2":
            analiz.fiyat_karsilastir()
        elif secim == "3":
            analiz.harcama_analizi()
        elif secim == "4":
            analiz.fisler_listele()
        elif secim == "5":
            analiz.veri_disa_aktar()
        elif secim == "6":
            print("\n👋 Programdan çıkılıyor...")
            break
        else:
            print("\n❌ Geçersiz seçim! Lütfen 1-6 arası bir sayı girin.")


if __name__ == "__main__":
    print("\n" + "="*60)
    print(" " * 10 + "MARKET FİYAT KARŞILAŞTIRMA VE")
    print(" " * 12 + "HARCAMA ANALİZİ SİSTEMİ")
    print("="*60)
    print("\nAileler için kapsamlı market alışverişi yönetim programı")
    print("Fişlerinizi ekleyin, fiyatları karşılaştırın, tasarruf edin!")
    
    input("\nDevam etmek için Enter'a basın...")
    
    try:
        ana_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
