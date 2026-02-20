#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Market Fiyat Kar┼ş─▒la┼şt─▒rma ve Harcama Analizi - Streamlit Aray├╝z├╝
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

# ÔöÇÔöÇ Sayfa yap─▒land─▒rmas─▒ ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
st.set_page_config(
    page_title="Market Analiz Sistemi",
    page_icon="­şøÆ",
    layout="wide",
    initial_sidebar_state="expanded",
)

VER─░_DOSYASI = "market_verileri.json"


# ÔöÇÔöÇ Veri y├Ânetimi ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
def verileri_yukle():
    if os.path.exists(VER─░_DOSYASI):
        try:
            with open(VER─░_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"fisler": [], "urunler": {}, "marketler": {}}


def verileri_kaydet(veriler):
    with open(VER─░_DOSYASI, "w", encoding="utf-8") as f:
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


# ÔöÇÔöÇ Session state ba┼şlat ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
if "veriler" not in st.session_state:
    st.session_state.veriler = verileri_yukle()

if "sepet" not in st.session_state:
    st.session_state.sepet = []

# ÔöÇÔöÇ Kenar ├ğubu─şu ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
with st.sidebar:
    st.title("­şøÆ Market Analiz")
    st.markdown("---")
    sayfa = st.radio(
        "Men├╝",
        [
            "­şÅá Ana Sayfa",
            "­şôØ Yeni Fi┼ş Ekle",
            "­şÆ░ Fiyat Kar┼ş─▒la┼şt─▒r",
            "­şôè Harcama Analizi",
            "­şôï Fi┼şleri Listele",
            "­şÆ¥ Verileri D─▒┼şa Aktar",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    veriler = st.session_state.veriler
    st.metric("Toplam Fi┼ş", len(veriler["fisler"]))
    st.metric("Kay─▒tl─▒ ├£r├╝n", len(veriler["urunler"]))
    st.metric("Market Say─▒s─▒", len(veriler["marketler"]))


# ÔöÇÔöÇ Yard─▒mc─▒ ÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇÔöÇ
veriler = st.session_state.veriler


# =============================================================================
# ANA SAYFA
# =============================================================================
if sayfa == "­şÅá Ana Sayfa":
    st.title("­şøÆ Market Fiyat Kar┼ş─▒la┼şt─▒rma ve Harcama Analizi")
    st.subheader("Aileler i├ğin ak─▒ll─▒ market al─▒┼şveri┼ş asistan─▒ ­şÆ░")
    st.markdown("---")

    if not veriler["fisler"]:
        st.info("Hen├╝z fi┼ş giri┼şi yap─▒lmad─▒. Sol men├╝den **­şôØ Yeni Fi┼ş Ekle** ile ba┼şlay─▒n!")
    else:
        toplam_fis = len(veriler["fisler"])
        toplam_harcama = sum(f["toplam"] for f in veriler["fisler"])
        ort_fis = toplam_harcama / toplam_fis
        toplam_urun = sum(len(f["urunler"]) for f in veriler["fisler"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("­şôï Toplam Fi┼ş", toplam_fis)
        col2.metric("­şÆ░ Toplam Harcama", f"{toplam_harcama:,.2f} Ôé║")
        col3.metric("­şôè Ortalama Fi┼ş", f"{ort_fis:,.2f} Ôé║")
        col4.metric("­şøÆ Toplam Al─▒m", toplam_urun)

        st.markdown("---")

        # Son 10 fi┼ş grafi─şi
        st.subheader("­şôê Son Fi┼şler")
        son_fisler = veriler["fisler"][-10:]
        df_fisler = pd.DataFrame([
            {"Fi┼ş": f"#{f['id']} {f['market']}", "Tarih": f["tarih"], "Toplam (Ôé║)": f["toplam"]}
            for f in son_fisler
        ])
        fig = px.bar(df_fisler, x="Fi┼ş", y="Toplam (Ôé║)", color="Toplam (Ôé║)",
                     color_continuous_scale="Blues", title="Son 10 Al─▒┼şveri┼ş Tutar─▒")
        st.plotly_chart(fig, use_container_width=True)

        # Market da─ş─▒l─▒m─▒
        if len(veriler["marketler"]) > 0:
            st.subheader("­şÅ¬ Markete G├Âre Harcama Da─ş─▒l─▒m─▒")
            market_harcama = defaultdict(float)
            for f in veriler["fisler"]:
                market_harcama[f["market"]] += f["toplam"]
            df_market = pd.DataFrame(list(market_harcama.items()), columns=["Market", "Harcama (Ôé║)"])
            fig2 = px.pie(df_market, names="Market", values="Harcama (Ôé║)",
                          title="Marketlere G├Âre Harcama Pay─▒")
            st.plotly_chart(fig2, use_container_width=True)


# =============================================================================
# YEN─░ F─░┼Ş EKLE
# =============================================================================
elif sayfa == "­şôØ Yeni Fi┼ş Ekle":
    st.title("­şôØ Yeni Al─▒┼şveri┼ş Fi┼şi Ekle")
    st.markdown("---")

    col_sol, col_sag = st.columns([1, 1])

    with col_sol:
        st.subheader("Market Bilgileri")
        market_adi = st.text_input("Market Ad─▒ *", placeholder="├ûrn: Migros, A101, B─░M...")
        tarih = st.date_input("Al─▒┼şveri┼ş Tarihi", value=datetime.today())
        tarih_str = tarih.strftime("%d.%m.%Y")

        st.markdown("---")
        st.subheader("├£r├╝n Ekle")
        with st.form("urun_form", clear_on_submit=True):
            urun_adi = st.text_input("├£r├╝n Ad─▒")
            col_a, col_b, col_c = st.columns(3)
            miktar = col_a.number_input("Miktar", min_value=0.01, value=1.0, step=0.1)
            fiyat = col_b.number_input("Fiyat (Ôé║)", min_value=0.01, value=1.0, step=0.5)
            birim = col_c.selectbox("Birim", ["adet", "kg", "lt", "gr", "ml"])
            ekle_btn = st.form_submit_button("ÔŞò Sepete Ekle", use_container_width=True)

            if ekle_btn:
                if not urun_adi.strip():
                    st.error("├£r├╝n ad─▒ bo┼ş olamaz!")
                else:
                    birim_fiyat = fiyat / miktar if miktar > 0 else fiyat
                    st.session_state.sepet.append({
                        "ad": urun_adi.strip().title(),
                        "miktar": miktar,
                        "birim": birim,
                        "fiyat": fiyat,
                        "birim_fiyat": birim_fiyat,
                    })
                    st.success(f"Ô£à {urun_adi.title()} eklendi!")

    with col_sag:
        st.subheader("­şğ¥ Sepet")
        if not st.session_state.sepet:
            st.info("Sepet bo┼ş. Sol taraftan ├╝r├╝n ekleyin.")
        else:
            toplam = sum(u["fiyat"] for u in st.session_state.sepet)
            df_sepet = pd.DataFrame(st.session_state.sepet)[["ad", "miktar", "birim", "fiyat", "birim_fiyat"]]
            df_sepet.columns = ["├£r├╝n", "Miktar", "Birim", "Fiyat (Ôé║)", "Birim Fiyat (Ôé║)"]
            st.dataframe(df_sepet, use_container_width=True, hide_index=True)

            st.metric("­şÆ░ Toplam Tutar", f"{toplam:.2f} Ôé║")

            silme_col, kaydet_col = st.columns(2)

            with silme_col:
                if st.button("­şùæ´©Å Sepeti Temizle", use_container_width=True):
                    st.session_state.sepet = []
                    st.rerun()

            with kaydet_col:
                if st.button("­şÆ¥ Fi┼şi Kaydet", type="primary", use_container_width=True):
                    if not market_adi.strip():
                        st.error("L├╝tfen market ad─▒ girin!")
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
                        st.success(f"Ô£à Fi┼ş #{fis['id']} ba┼şar─▒yla kaydedildi! Toplam: {toplam:.2f} Ôé║")
                        st.balloons()
                        st.rerun()


# =============================================================================
# F─░YAT KAR┼ŞILA┼ŞTIR
# =============================================================================
elif sayfa == "­şÆ░ Fiyat Kar┼ş─▒la┼şt─▒r":
    st.title("­şÆ░ Fiyat Kar┼ş─▒la┼şt─▒rma")
    st.markdown("---")

    if not veriler["urunler"]:
        st.warning("Hen├╝z ├╝r├╝n verisi yok. ├ûnce fi┼ş ekleyin!")
    else:
        urun_listesi = sorted(veriler["urunler"].keys())
        secilen_urun = st.selectbox("Kar┼ş─▒la┼şt─▒rmak istedi─şiniz ├╝r├╝n├╝ se├ğin:", urun_listesi)

        if secilen_urun:
            urun_verileri = veriler["urunler"][secilen_urun]
            karsilastirma = []

            for market, kayitlar in urun_verileri.items():
                if kayitlar:
                    son = kayitlar[-1]
                    ortalama = statistics.mean([k["birim_fiyat"] for k in kayitlar])
                    karsilastirma.append({
                        "Market": market,
                        "Son Fiyat (Ôé║)": round(son["birim_fiyat"], 2),
                        "Ortalama (Ôé║)": round(ortalama, 2),
                        "Birim": son["birim"],
                        "Son Tarih": son["tarih"],
                        "Kay─▒t Say─▒s─▒": len(kayitlar),
                    })

            karsilastirma.sort(key=lambda x: x["Son Fiyat (Ôé║)"])

            st.subheader(f"­şöı **{secilen_urun}** - Marketler Aras─▒ Kar┼ş─▒la┼şt─▒rma")

            if len(karsilastirma) >= 1:
                en_ucuz = karsilastirma[0]
                en_pahali = karsilastirma[-1]

                c1, c2, c3 = st.columns(3)
                c1.metric("­şÑç En Ucuz", f"{en_ucuz['Market']}", f"{en_ucuz['Son Fiyat (Ôé║)']:.2f} Ôé║")
                c2.metric("­şÆ© En Pahal─▒", f"{en_pahali['Market']}", f"{en_pahali['Son Fiyat (Ôé║)']:.2f} Ôé║")
                if len(karsilastirma) > 1:
                    fark = en_pahali["Son Fiyat (Ôé║)"] - en_ucuz["Son Fiyat (Ôé║)"]
                    fark_yuzde = (fark / en_ucuz["Son Fiyat (Ôé║)"]) * 100
                    c3.metric("­şôè Fiyat Fark─▒", f"{fark:.2f} Ôé║", f"%{fark_yuzde:.1f}")

                st.markdown("---")

                df_kars = pd.DataFrame(karsilastirma)
                st.dataframe(df_kars, use_container_width=True, hide_index=True)

                st.markdown("---")
                fig = px.bar(
                    df_kars,
                    x="Market",
                    y="Son Fiyat (Ôé║)",
                    color="Market",
                    title=f"{secilen_urun} - Market Fiyat Kar┼ş─▒la┼şt─▒rmas─▒",
                    text="Son Fiyat (Ôé║)",
                    labels={"Son Fiyat (Ôé║)": "Son Fiyat (Ôé║)"},
                )
                fig.update_traces(texttemplate="%{text:.2f} Ôé║", textposition="outside")
                st.plotly_chart(fig, use_container_width=True)

                # Tarihsel fiyat trendi
                st.subheader("­şôê Fiyat Trendi")
                trend_data = []
                for market, kayitlar in urun_verileri.items():
                    for k in kayitlar:
                        trend_data.append({
                            "Tarih": k["tarih"],
                            "Birim Fiyat (Ôé║)": k["birim_fiyat"],
                            "Market": market,
                        })
                if trend_data:
                    df_trend = pd.DataFrame(trend_data)
                    fig2 = px.line(
                        df_trend,
                        x="Tarih",
                        y="Birim Fiyat (Ôé║)",
                        color="Market",
                        markers=True,
                        title=f"{secilen_urun} - Tarihe G├Âre Birim Fiyat De─şi┼şimi",
                    )
                    st.plotly_chart(fig2, use_container_width=True)


# =============================================================================
# HARCAMA ANAL─░Z─░
# =============================================================================
elif sayfa == "­şôè Harcama Analizi":
    st.title("­şôè Harcama Analizi")
    st.markdown("---")

    if not veriler["fisler"]:
        st.warning("Hen├╝z fi┼ş verisi yok. ├ûnce fi┼ş ekleyin!")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "­şôï Genel ├ûzet",
            "­şÅ¬ Markete G├Âre",
            "­şôà Ayl─▒k Analiz",
            "­şöÑ Pop├╝ler ├£r├╝nler",
        ])

        # --- Genel ├ûzet ---
        with tab1:
            toplam_fis = len(veriler["fisler"])
            toplam_harcama = sum(f["toplam"] for f in veriler["fisler"])
            ort_fis = toplam_harcama / toplam_fis
            toplam_urun = sum(len(f["urunler"]) for f in veriler["fisler"])

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("­şôï Fi┼ş Say─▒s─▒", toplam_fis)
            c2.metric("­şÆ░ Toplam Harcama", f"{toplam_harcama:,.2f} Ôé║")
            c3.metric("­şôè Ortalama Fi┼ş", f"{ort_fis:,.2f} Ôé║")
            c4.metric("­şøÆ Toplam Al─▒m", toplam_urun)
            c5.metric("­şÅ¬ Market Say─▒s─▒", len(veriler["marketler"]))

            st.markdown("---")

            df_all = pd.DataFrame([
                {
                    "Fi┼ş": f"#{f['id']}",
                    "Market": f["market"],
                    "Tarih": f["tarih"],
                    "├£r├╝n Say─▒s─▒": len(f["urunler"]),
                    "Toplam (Ôé║)": f["toplam"],
                }
                for f in veriler["fisler"]
            ])
            st.dataframe(df_all.sort_values("Fi┼ş", ascending=False).reset_index(drop=True),
                         use_container_width=True, hide_index=True)

        # --- Markete G├Âre ---
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
                    "Toplam Harcama (Ôé║)": round(harcama, 2),
                    "Fi┼ş Say─▒s─▒": market_fis[market],
                    "Ortalama Fi┼ş (Ôé║)": round(harcama / market_fis[market], 2),
                })
            df_market = pd.DataFrame(rows)
            st.dataframe(df_market, use_container_width=True, hide_index=True)

            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(df_market, x="Market", y="Toplam Harcama (Ôé║)",
                             color="Market", title="Markete G├Âre Toplam Harcama")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig2 = px.pie(df_market, names="Market", values="Toplam Harcama (Ôé║)",
                              title="Harcama Pay─▒")
                st.plotly_chart(fig2, use_container_width=True)

        # --- Ayl─▒k Analiz ---
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
                    "Ay/Y─▒l": ay_yil,
                    "Harcama (Ôé║)": round(harcama, 2),
                    "Fi┼ş Say─▒s─▒": aylik_fis[ay_yil],
                    "G├╝nl├╝k Ort. (Ôé║)": round(harcama / 30, 2),
                })
            df_ay = pd.DataFrame(rows_ay)
            st.dataframe(df_ay, use_container_width=True, hide_index=True)

            if not df_ay.empty:
                fig = px.line(df_ay, x="Ay/Y─▒l", y="Harcama (Ôé║)",
                              markers=True, title="Ayl─▒k Harcama Trendi")
                st.plotly_chart(fig, use_container_width=True)

        # --- Pop├╝ler ├£r├╝nler ---
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
                    "├£r├╝n": urun,
                    "Al─▒m Say─▒s─▒": alinma,
                    "Toplam Harcama (Ôé║)": round(urun_harcama[urun], 2),
                }
                for i, (urun, alinma) in enumerate(sirali)
            ]
            df_pop = pd.DataFrame(rows_urun)
            st.dataframe(df_pop, use_container_width=True, hide_index=True)

            if not df_pop.empty:
                fig = px.bar(df_pop.head(10), x="├£r├╝n", y="Al─▒m Say─▒s─▒",
                             color="Al─▒m Say─▒s─▒", title="En ├çok Al─▒nan 10 ├£r├╝n",
                             color_continuous_scale="Greens")
                st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# F─░┼ŞLER─░ L─░STELE
# =============================================================================
elif sayfa == "­şôï Fi┼şleri Listele":
    st.title("­şôï T├╝m Fi┼şler")
    st.markdown("---")

    if not veriler["fisler"]:
        st.warning("Hen├╝z fi┼ş yok.")
    else:
        col_filtre, col_bos = st.columns([1, 2])
        with col_filtre:
            market_filtre = st.selectbox(
                "Markete G├Âre Filtre",
                ["T├╝m├╝"] + sorted({f["market"] for f in veriler["fisler"]}),
            )

        fisler_goster = veriler["fisler"]
        if market_filtre != "T├╝m├╝":
            fisler_goster = [f for f in fisler_goster if f["market"] == market_filtre]

        fisler_goster = list(reversed(fisler_goster))

        for fis in fisler_goster:
            with st.expander(
                f"­şğ¥ Fi┼ş #{fis['id']} ÔÇö {fis['market']} ÔÇö {fis['tarih']} ÔÇö **{fis['toplam']:.2f} Ôé║**"
            ):
                df_fis = pd.DataFrame(fis["urunler"])[["ad", "miktar", "birim", "fiyat", "birim_fiyat"]]
                df_fis.columns = ["├£r├╝n", "Miktar", "Birim", "Fiyat (Ôé║)", "Birim Fiyat (Ôé║)"]
                st.dataframe(df_fis, use_container_width=True, hide_index=True)
                st.caption(f"Kay─▒t zaman─▒: {fis.get('kayit_zamani', '-')}")


# =============================================================================
# VER─░LER─░ DI┼ŞA AKTAR
# =============================================================================
elif sayfa == "­şÆ¥ Verileri D─▒┼şa Aktar":
    st.title("­şÆ¥ Verileri D─▒┼şa Aktar")
    st.markdown("---")

    if not veriler["fisler"]:
        st.warning("D─▒┼şa aktar─▒lacak veri yok.")
    else:
        rows_csv = []
        for fis in veriler["fisler"]:
            for urun in fis["urunler"]:
                rows_csv.append({
                    "Fi┼ş ID": fis["id"],
                    "Market": fis["market"],
                    "Tarih": fis["tarih"],
                    "├£r├╝n": urun["ad"],
                    "Miktar": urun["miktar"],
                    "Birim": urun["birim"],
                    "Fiyat (Ôé║)": urun["fiyat"],
                    "Birim Fiyat (Ôé║)": urun["birim_fiyat"],
                })
        df_export = pd.DataFrame(rows_csv)
        st.dataframe(df_export, use_container_width=True, hide_index=True)

        csv_data = df_export.to_csv(index=False, encoding="utf-8-sig")
        dosya_adi = f"market_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        st.download_button(
            label="­şôÑ CSV Olarak ─░ndir",
            data=csv_data,
            file_name=dosya_adi,
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )

        st.markdown("---")
        json_data = json.dumps(veriler, ensure_ascii=False, indent=2)
        st.download_button(
            label="­şôÑ JSON Olarak ─░ndir (T├╝m Veri)",
            data=json_data,
            file_name="market_verileri.json",
            mime="application/json",
            use_container_width=True,
        )
