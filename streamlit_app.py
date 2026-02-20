#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Market Fiyat Karşılaştırma ve Harcama Analizi - Streamlit Arayüzü
"""

import json
import os
import statistics
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from collections import defaultdict

# ── Sayfa yapılandırması ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Market Analiz Sistemi",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

VERİ_DOSYASI = "market_verileri.json"


# ── Veri yönetimi ─────────────────────────────────────────────────────────────
def verileri_yukle():
    if os.path.exists(VERİ_DOSYASI):
        try:
            with open(VERİ_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"fisler": [], "urunler": {}, "marketler": {}}


def verileri_kaydet(veriler):
    with open(VERİ_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=2)


def urun_verilerini_guncelle(veriler, market, tarih, urunler):
    for urun in urunler:
        urun_adi = urun["ad"]
        veriler["urunler"].setdefault(urun_adi, {})
        veriler["urunler"][urun_adi].setdefault(market, [])
        veriler["urunler"][urun_adi][market].append({
            "tarih": tarih,
            "fiyat": urun["fiyat"],
            "birim_fiyat": urun["birim_fiyat"],
            "miktar": urun["miktar"],
            "birim": urun["birim"],
        })
        if market not in veriler["marketler"]:
            veriler["marketler"][market] = {
                "toplam_alisveris": 0,
                "toplam_harcama": 0,
                "urun_sayisi": 0,
            }
        veriler["marketler"][market]["toplam_alisveris"] += 1
        veriler["marketler"][market]["toplam_harcama"] += urun["fiyat"]
        veriler["marketler"][market]["urun_sayisi"] += 1


# ── Session state başlat ──────────────────────────────────────────────────────
if "veriler" not in st.session_state:
    st.session_state.veriler = verileri_yukle()

if "sepet" not in st.session_state:
    st.session_state.sepet = []

# ── Kenar çubuğu ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🛒 Market Analiz")
    st.markdown("---")
    sayfa = st.radio(
        "Menü",
        [
            "🏠 Ana Sayfa",
            "📝 Yeni Fiş Ekle",
            "💰 Fiyat Karşılaştır",
            "📊 Harcama Analizi",
            "📋 Fişleri Listele",
            "💾 Verileri Dışa Aktar",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    veriler = st.session_state.veriler
    st.metric("Toplam Fiş", len(veriler["fisler"]))
    st.metric("Kayıtlı Ürün", len(veriler["urunler"]))
    st.metric("Market Sayısı", len(veriler["marketler"]))


# ── Yardımcı ─────────────────────────────────────────────────────────────────
veriler = st.session_state.veriler


# =============================================================================
# ANA SAYFA
# =============================================================================
if sayfa == "🏠 Ana Sayfa":
    st.title("🛒 Market Fiyat Karşılaştırma ve Harcama Analizi")
    st.subheader("Aileler için akıllı market alışveriş asistanı 💰")
    st.markdown("---")

    if not veriler["fisler"]:
        st.info("Henüz fiş girişi yapılmadı. Sol menüden **📝 Yeni Fiş Ekle** ile başlayın!")
    else:
        toplam_fis = len(veriler["fisler"])
        toplam_harcama = sum(f["toplam"] for f in veriler["fisler"])
        ort_fis = toplam_harcama / toplam_fis
        toplam_urun = sum(len(f["urunler"]) for f in veriler["fisler"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📋 Toplam Fiş", toplam_fis)
        col2.metric("💰 Toplam Harcama", f"{toplam_harcama:,.2f} ₺")
        col3.metric("📊 Ortalama Fiş", f"{ort_fis:,.2f} ₺")
        col4.metric("🛒 Toplam Alım", toplam_urun)

        st.markdown("---")

        # Son 10 fiş grafiği
        st.subheader("📈 Son Fişler")
        son_fisler = veriler["fisler"][-10:]
        df_fisler = pd.DataFrame([
            {"Fiş": f"#{f['id']} {f['market']}", "Tarih": f["tarih"], "Toplam (₺)": f["toplam"]}
            for f in son_fisler
        ])
        fig = px.bar(df_fisler, x="Fiş", y="Toplam (₺)", color="Toplam (₺)",
                     color_continuous_scale="Blues", title="Son 10 Alışveriş Tutarı")
        st.plotly_chart(fig, use_container_width=True)

        # Market dağılımı
        if len(veriler["marketler"]) > 0:
            st.subheader("🏪 Markete Göre Harcama Dağılımı")
            market_harcama = defaultdict(float)
            for f in veriler["fisler"]:
                market_harcama[f["market"]] += f["toplam"]
            df_market = pd.DataFrame(list(market_harcama.items()), columns=["Market", "Harcama (₺)"])
            fig2 = px.pie(df_market, names="Market", values="Harcama (₺)",
                          title="Marketlere Göre Harcama Payı")
            st.plotly_chart(fig2, use_container_width=True)


# =============================================================================
# YENİ FİŞ EKLE
# =============================================================================
elif sayfa == "📝 Yeni Fiş Ekle":
    st.title("📝 Yeni Alışveriş Fişi Ekle")
    st.markdown("---")

    col_sol, col_sag = st.columns([1, 1])

    with col_sol:
        st.subheader("Market Bilgileri")
        market_adi = st.text_input("Market Adı *", placeholder="Örn: Migros, A101, BİM...")
        tarih = st.date_input("Alışveriş Tarihi", value=datetime.today())
        tarih_str = tarih.strftime("%d.%m.%Y")

        st.markdown("---")
        st.subheader("Ürün Ekle")
        with st.form("urun_form", clear_on_submit=True):
            urun_adi = st.text_input("Ürün Adı")
            col_a, col_b, col_c = st.columns(3)
            miktar = col_a.number_input("Miktar", min_value=0.01, value=1.0, step=0.1)
            fiyat = col_b.number_input("Fiyat (₺)", min_value=0.01, value=1.0, step=0.5)
            birim = col_c.selectbox("Birim", ["adet", "kg", "lt", "gr", "ml"])
            ekle_btn = st.form_submit_button("➕ Sepete Ekle", use_container_width=True)

            if ekle_btn:
                if not urun_adi.strip():
                    st.error("Ürün adı boş olamaz!")
                else:
                    birim_fiyat = fiyat / miktar if miktar > 0 else fiyat
                    st.session_state.sepet.append({
                        "ad": urun_adi.strip().title(),
                        "miktar": miktar,
                        "birim": birim,
                        "fiyat": fiyat,
                        "birim_fiyat": birim_fiyat,
                    })
                    st.success(f"✅ {urun_adi.title()} eklendi!")

    with col_sag:
        st.subheader("🧾 Sepet")
        if not st.session_state.sepet:
            st.info("Sepet boş. Sol taraftan ürün ekleyin.")
        else:
            toplam = sum(u["fiyat"] for u in st.session_state.sepet)
            df_sepet = pd.DataFrame(st.session_state.sepet)[["ad", "miktar", "birim", "fiyat", "birim_fiyat"]]
            df_sepet.columns = ["Ürün", "Miktar", "Birim", "Fiyat (₺)", "Birim Fiyat (₺)"]
            st.dataframe(df_sepet, use_container_width=True, hide_index=True)

            st.metric("💰 Toplam Tutar", f"{toplam:.2f} ₺")

            silme_col, kaydet_col = st.columns(2)

            with silme_col:
                if st.button("🗑️ Sepeti Temizle", use_container_width=True):
                    st.session_state.sepet = []
                    st.rerun()

            with kaydet_col:
                if st.button("💾 Fişi Kaydet", type="primary", use_container_width=True):
                    if not market_adi.strip():
                        st.error("Lütfen market adı girin!")
                    else:
                        fis = {
                            "id": len(veriler["fisler"]) + 1,
                            "market": market_adi.strip().title(),
                            "tarih": tarih_str,
                            "urunler": st.session_state.sepet.copy(),
                            "toplam": toplam,
                            "kayit_zamani": datetime.now().isoformat(),
                        }
                        veriler["fisler"].append(fis)
                        urun_verilerini_guncelle(
                            veriler, market_adi.strip().title(),
                            tarih_str, st.session_state.sepet
                        )
                        verileri_kaydet(veriler)
                        st.session_state.veriler = veriler
                        st.session_state.sepet = []
                        st.success(f"✅ Fiş #{fis['id']} başarıyla kaydedildi! Toplam: {toplam:.2f} ₺")
                        st.balloons()
                        st.rerun()


# =============================================================================
# FİYAT KARŞILAŞTIR
# =============================================================================
elif sayfa == "💰 Fiyat Karşılaştır":
    st.title("💰 Fiyat Karşılaştırma")
    st.markdown("---")

    if not veriler["urunler"]:
        st.warning("Henüz ürün verisi yok. Önce fiş ekleyin!")
    else:
        urun_listesi = sorted(veriler["urunler"].keys())
        secilen_urun = st.selectbox("Karşılaştırmak istediğiniz ürünü seçin:", urun_listesi)

        if secilen_urun:
            urun_verileri = veriler["urunler"][secilen_urun]
            karsilastirma = []

            for market, kayitlar in urun_verileri.items():
                if kayitlar:
                    son = kayitlar[-1]
                    ortalama = statistics.mean([k["birim_fiyat"] for k in kayitlar])
                    karsilastirma.append({
                        "Market": market,
                        "Son Fiyat (₺)": round(son["birim_fiyat"], 2),
                        "Ortalama (₺)": round(ortalama, 2),
                        "Birim": son["birim"],
                        "Son Tarih": son["tarih"],
                        "Kayıt Sayısı": len(kayitlar),
                    })

            karsilastirma.sort(key=lambda x: x["Son Fiyat (₺)"])

            st.subheader(f"🔍 **{secilen_urun}** - Marketler Arası Karşılaştırma")

            if len(karsilastirma) >= 1:
                en_ucuz = karsilastirma[0]
                en_pahali = karsilastirma[-1]

                c1, c2, c3 = st.columns(3)
                c1.metric("🥇 En Ucuz", f"{en_ucuz['Market']}", f"{en_ucuz['Son Fiyat (₺)']:.2f} ₺")
                c2.metric("💸 En Pahalı", f"{en_pahali['Market']}", f"{en_pahali['Son Fiyat (₺)']:.2f} ₺")
                if len(karsilastirma) > 1:
                    fark = en_pahali["Son Fiyat (₺)"] - en_ucuz["Son Fiyat (₺)"]
                    fark_yuzde = (fark / en_ucuz["Son Fiyat (₺)"]) * 100
                    c3.metric("📊 Fiyat Farkı", f"{fark:.2f} ₺", f"%{fark_yuzde:.1f}")

                st.markdown("---")

                df_kars = pd.DataFrame(karsilastirma)
                st.dataframe(df_kars, use_container_width=True, hide_index=True)

                st.markdown("---")
                fig = px.bar(
                    df_kars,
                    x="Market",
                    y="Son Fiyat (₺)",
                    color="Market",
                    title=f"{secilen_urun} - Market Fiyat Karşılaştırması",
                    text="Son Fiyat (₺)",
                    labels={"Son Fiyat (₺)": "Son Fiyat (₺)"},
                )
                fig.update_traces(texttemplate="%{text:.2f} ₺", textposition="outside")
                st.plotly_chart(fig, use_container_width=True)

                # Tarihsel fiyat trendi
                st.subheader("📈 Fiyat Trendi")
                trend_data = []
                for market, kayitlar in urun_verileri.items():
                    for k in kayitlar:
                        trend_data.append({
                            "Tarih": k["tarih"],
                            "Birim Fiyat (₺)": k["birim_fiyat"],
                            "Market": market,
                        })
                if trend_data:
                    df_trend = pd.DataFrame(trend_data)
                    fig2 = px.line(
                        df_trend,
                        x="Tarih",
                        y="Birim Fiyat (₺)",
                        color="Market",
                        markers=True,
                        title=f"{secilen_urun} - Tarihe Göre Birim Fiyat Değişimi",
                    )
                    st.plotly_chart(fig2, use_container_width=True)


# =============================================================================
# HARCAMA ANALİZİ
# =============================================================================
elif sayfa == "📊 Harcama Analizi":
    st.title("📊 Harcama Analizi")
    st.markdown("---")

    if not veriler["fisler"]:
        st.warning("Henüz fiş verisi yok. Önce fiş ekleyin!")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Genel Özet",
            "🏪 Markete Göre",
            "📅 Aylık Analiz",
            "🔥 Popüler Ürünler",
        ])

        # --- Genel Özet ---
        with tab1:
            toplam_fis = len(veriler["fisler"])
            toplam_harcama = sum(f["toplam"] for f in veriler["fisler"])
            ort_fis = toplam_harcama / toplam_fis
            toplam_urun = sum(len(f["urunler"]) for f in veriler["fisler"])

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("📋 Fiş Sayısı", toplam_fis)
            c2.metric("💰 Toplam Harcama", f"{toplam_harcama:,.2f} ₺")
            c3.metric("📊 Ortalama Fiş", f"{ort_fis:,.2f} ₺")
            c4.metric("🛒 Toplam Alım", toplam_urun)
            c5.metric("🏪 Market Sayısı", len(veriler["marketler"]))

            st.markdown("---")

            df_all = pd.DataFrame([
                {
                    "Fiş": f"#{f['id']}",
                    "Market": f["market"],
                    "Tarih": f["tarih"],
                    "Ürün Sayısı": len(f["urunler"]),
                    "Toplam (₺)": f["toplam"],
                }
                for f in veriler["fisler"]
            ])
            st.dataframe(df_all.sort_values("Fiş", ascending=False).reset_index(drop=True),
                         use_container_width=True, hide_index=True)

        # --- Markete Göre ---
        with tab2:
            market_harcama = defaultdict(float)
            market_fis = defaultdict(int)
            for f in veriler["fisler"]:
                market_harcama[f["market"]] += f["toplam"]
                market_fis[f["market"]] += 1

            rows = []
            for market, harcama in sorted(market_harcama.items(), key=lambda x: x[1], reverse=True):
                rows.append({
                    "Market": market,
                    "Toplam Harcama (₺)": round(harcama, 2),
                    "Fiş Sayısı": market_fis[market],
                    "Ortalama Fiş (₺)": round(harcama / market_fis[market], 2),
                })
            df_market = pd.DataFrame(rows)
            st.dataframe(df_market, use_container_width=True, hide_index=True)

            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(df_market, x="Market", y="Toplam Harcama (₺)",
                             color="Market", title="Markete Göre Toplam Harcama")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig2 = px.pie(df_market, names="Market", values="Toplam Harcama (₺)",
                              title="Harcama Payı")
                st.plotly_chart(fig2, use_container_width=True)

        # --- Aylık Analiz ---
        with tab3:
            aylik_harcama = defaultdict(float)
            aylik_fis = defaultdict(int)
            for f in veriler["fisler"]:
                try:
                    parcalar = f["tarih"].split(".")
                    if len(parcalar) == 3:
                        ay_yil = f"{parcalar[1]}.{parcalar[2]}"
                        aylik_harcama[ay_yil] += f["toplam"]
                        aylik_fis[ay_yil] += 1
                except Exception:
                    continue

            rows_ay = []
            for ay_yil, harcama in sorted(aylik_harcama.items()):
                rows_ay.append({
                    "Ay/Yıl": ay_yil,
                    "Harcama (₺)": round(harcama, 2),
                    "Fiş Sayısı": aylik_fis[ay_yil],
                    "Günlük Ort. (₺)": round(harcama / 30, 2),
                })
            df_ay = pd.DataFrame(rows_ay)
            st.dataframe(df_ay, use_container_width=True, hide_index=True)

            if not df_ay.empty:
                fig = px.line(df_ay, x="Ay/Yıl", y="Harcama (₺)",
                              markers=True, title="Aylık Harcama Trendi")
                st.plotly_chart(fig, use_container_width=True)

        # --- Popüler Ürünler ---
        with tab4:
            urun_alinma = defaultdict(int)
            urun_harcama = defaultdict(float)
            for f in veriler["fisler"]:
                for u in f["urunler"]:
                    urun_alinma[u["ad"]] += 1
                    urun_harcama[u["ad"]] += u["fiyat"]

            sirali = sorted(urun_alinma.items(), key=lambda x: x[1], reverse=True)[:20]
            rows_urun = [
                {
                    "#": i + 1,
                    "Ürün": urun,
                    "Alım Sayısı": alinma,
                    "Toplam Harcama (₺)": round(urun_harcama[urun], 2),
                }
                for i, (urun, alinma) in enumerate(sirali)
            ]
            df_pop = pd.DataFrame(rows_urun)
            st.dataframe(df_pop, use_container_width=True, hide_index=True)

            if not df_pop.empty:
                fig = px.bar(df_pop.head(10), x="Ürün", y="Alım Sayısı",
                             color="Alım Sayısı", title="En Çok Alınan 10 Ürün",
                             color_continuous_scale="Greens")
                st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# FİŞLERİ LİSTELE
# =============================================================================
elif sayfa == "📋 Fişleri Listele":
    st.title("📋 Tüm Fişler")
    st.markdown("---")

    if not veriler["fisler"]:
        st.warning("Henüz fiş yok.")
    else:
        col_filtre, col_bos = st.columns([1, 2])
        with col_filtre:
            market_filtre = st.selectbox(
                "Markete Göre Filtre",
                ["Tümü"] + sorted({f["market"] for f in veriler["fisler"]}),
            )

        fisler_goster = veriler["fisler"]
        if market_filtre != "Tümü":
            fisler_goster = [f for f in fisler_goster if f["market"] == market_filtre]

        fisler_goster = list(reversed(fisler_goster))

        for fis in fisler_goster:
            with st.expander(
                f"🧾 Fiş #{fis['id']} — {fis['market']} — {fis['tarih']} — **{fis['toplam']:.2f} ₺**"
            ):
                df_fis = pd.DataFrame(fis["urunler"])[["ad", "miktar", "birim", "fiyat", "birim_fiyat"]]
                df_fis.columns = ["Ürün", "Miktar", "Birim", "Fiyat (₺)", "Birim Fiyat (₺)"]
                st.dataframe(df_fis, use_container_width=True, hide_index=True)
                st.caption(f"Kayıt zamanı: {fis.get('kayit_zamani', '-')}")


# =============================================================================
# VERİLERİ DIŞA AKTAR
# =============================================================================
elif sayfa == "💾 Verileri Dışa Aktar":
    st.title("💾 Verileri Dışa Aktar")
    st.markdown("---")

    if not veriler["fisler"]:
        st.warning("Dışa aktarılacak veri yok.")
    else:
        rows_csv = []
        for fis in veriler["fisler"]:
            for urun in fis["urunler"]:
                rows_csv.append({
                    "Fiş ID": fis["id"],
                    "Market": fis["market"],
                    "Tarih": fis["tarih"],
                    "Ürün": urun["ad"],
                    "Miktar": urun["miktar"],
                    "Birim": urun["birim"],
                    "Fiyat (₺)": urun["fiyat"],
                    "Birim Fiyat (₺)": urun["birim_fiyat"],
                })
        df_export = pd.DataFrame(rows_csv)
        st.dataframe(df_export, use_container_width=True, hide_index=True)

        csv_data = df_export.to_csv(index=False, encoding="utf-8-sig")
        dosya_adi = f"market_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        st.download_button(
            label="📥 CSV Olarak İndir",
            data=csv_data,
            file_name=dosya_adi,
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )

        st.markdown("---")
        json_data = json.dumps(veriler, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 JSON Olarak İndir (Tüm Veri)",
            data=json_data,
            file_name="market_verileri.json",
            mime="application/json",
            use_container_width=True,
        )
