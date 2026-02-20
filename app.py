#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, statistics
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title="Market Analiz", page_icon="\U0001f6d2", layout="wide",
                   initial_sidebar_state="collapsed")

# Mobile responsive CSS
st.markdown("""
<style>
/* Sidebar toggle butonu her zaman görünür */
[data-testid="collapsedControl"] { display: flex !important; }
/* Metrik kutular mobile'da wrap */
[data-testid="metric-container"] { min-width: 80px; }
/* Dataframe mobile scroll */
[data-testid="stDataFrame"] { overflow-x: auto; }
/* Butonlar mobile'da tam genişlik */
@media (max-width: 640px) {
    [data-testid="stHorizontalBlock"] > div { min-width: 0 !important; }
    .stButton button { width: 100% !important; }
    h1 { font-size: 1.4rem !important; }
    h2 { font-size: 1.1rem !important; }
}
</style>
""", unsafe_allow_html=True)
VERI_DOSYASI = "market_verileri.json"

def verileri_yukle():
    if os.path.exists(VERI_DOSYASI):
        try:
            with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"fisler": [], "urunler": {}, "marketler": {}}

def verileri_kaydet(v):
    with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)

def urun_guncelle(veriler, market, tarih, urunler):
    for u in urunler:
        ad = u["ad"]
        veriler["urunler"].setdefault(ad, {}).setdefault(market, []).append({
            "tarih": tarih, "fiyat": u["fiyat"], "birim_fiyat": u["birim_fiyat"],
            "miktar": u["miktar"], "birim": u["birim"]
        })
        if market not in veriler["marketler"]:
            veriler["marketler"][market] = {"toplam_alisveris": 0, "toplam_harcama": 0, "urun_sayisi": 0}
        veriler["marketler"][market]["toplam_alisveris"] += 1
        veriler["marketler"][market]["toplam_harcama"] += u["fiyat"]
        veriler["marketler"][market]["urun_sayisi"] += 1

def fis_sil(veriler, fis_id):
    veriler["fisler"] = [f for f in veriler["fisler"] if f["id"] != fis_id]
    veriler["urunler"] = {}
    veriler["marketler"] = {}
    for f in veriler["fisler"]:
        urun_guncelle(veriler, f["market"], f["tarih"], f["urunler"])
    verileri_kaydet(veriler)
    return veriler

if "veriler" not in st.session_state:
    st.session_state.veriler = verileri_yukle()
if "sepet" not in st.session_state:
    st.session_state.sepet = []

with st.sidebar:
    st.title("\U0001f6d2 Market Analiz")
    st.markdown("---")
    sayfa = st.radio("Menu", [
        "\U0001f3e0 Ana Sayfa",
        "\U0001f4dd Yeni Fis Ekle",
        "\U0001f4b0 Fiyat Karsilastir",
        "\U0001f4ca Harcama Analizi",
        "\U0001f4cb Fisleri Listele",
        "\U0001f5d1\ufe0f Fis Sil",
        "\U0001f4be Verileri Disa Aktar",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.caption("\U0001f4e4 Varolan JSON verinizi yukleyin (50MB+)")
    uploaded = st.file_uploader("JSON yukle", type=["json"], label_visibility="collapsed")
    if uploaded is not None:
        try:
            boyut_mb = uploaded.size / (1024 * 1024)
            icerik = json.load(uploaded)
            if "fisler" in icerik and "urunler" in icerik:
                verileri_kaydet(icerik)
                st.session_state.veriler = icerik
                st.success(f"Yuklendi! {len(icerik['fisler'])} fis ({boyut_mb:.1f} MB)")
                st.rerun()
            else:
                st.error("Gecersiz JSON formati!")
        except Exception as e:
            st.error(f"Hata: {e}")
    st.markdown("---")
    v = st.session_state.veriler
    st.metric("Toplam Fis", len(v["fisler"]))
    st.metric("Kayitli Urun", len(v["urunler"]))
    st.metric("Market Sayisi", len(v["marketler"]))

veriler = st.session_state.veriler

# ─── ANA SAYFA ────────────────────────────────────────────────────────────────
if sayfa == "\U0001f3e0 Ana Sayfa":
    st.title("\U0001f6d2 Market Fiyat Karsilastirma ve Harcama Analizi")
    st.subheader("Aileler icin akilli market alisveris asistani \U0001f4b0")
    st.markdown("---")
    if not veriler["fisler"]:
        st.info("Henuz fis girisi yapilmadi. Sol menuден Yeni Fis Ekle ile baslayin!")
    else:
        tf = len(veriler["fisler"])
        th = sum(f["toplam"] for f in veriler["fisler"])
        tu = sum(len(f["urunler"]) for f in veriler["fisler"])
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("\U0001f4cb Toplam Fis", tf)
        c2.metric("\U0001f4b0 Toplam Harcama", f"{th:,.2f} TL")
        c3.metric("\U0001f4ca Ortalama Fis", f"{th/tf:,.2f} TL")
        c4.metric("\U0001f6d2 Toplam Alim", tu)
        st.markdown("---")
        son_fisler = veriler["fisler"][-10:]
        df_f = pd.DataFrame([{"Fis": f"#{f['id']} {f['market']}", "Toplam (TL)": f["toplam"]}
                              for f in son_fisler])
        st.plotly_chart(px.bar(df_f, x="Fis", y="Toplam (TL)",
                               color_discrete_sequence=["#1f77b4"],
                               title="Son 10 Alisveris Tutari"),
                        use_container_width=True)
        mh = defaultdict(float)
        for f in veriler["fisler"]:
            mh[f["market"]] += f["toplam"]
        df_m = pd.DataFrame(list(mh.items()), columns=["Market", "Harcama (TL)"])
        st.plotly_chart(px.pie(df_m, names="Market", values="Harcama (TL)",
                               title="Markete Gore Harcama Dagilimi"),
                        use_container_width=True)

# ─── YENİ FİŞ EKLE ────────────────────────────────────────────────────────────
elif sayfa == "\U0001f4dd Yeni Fis Ekle":
    st.title("\U0001f4dd Yeni Alisveris Fisi Ekle")
    st.markdown("---")
    col_sol, col_sag = st.columns(2)
    with col_sol:
        st.subheader("Market Bilgileri")
        market_adi = st.text_input("Market Adi *", placeholder="Orn: Migros, A101, BIM...")
        tarih = st.date_input("Alisveris Tarihi", value=datetime.today())
        tarih_str = tarih.strftime("%d.%m.%Y")
        st.markdown("---")
        st.subheader("Urun Ekle")
        with st.form("urun_form", clear_on_submit=True):
            urun_adi = st.text_input("Urun Adi")
            ca, cb = st.columns(2)
            miktar = ca.number_input("Miktar", min_value=0.01, value=1.0, step=0.1)
            fiyat  = cb.number_input("Fiyat (TL)", min_value=0.01, value=1.0, step=0.5)
            birim  = st.selectbox("Birim", ["adet", "kg", "lt", "gr", "ml"])
            if st.form_submit_button("+ Sepete Ekle", use_container_width=True):
                if not urun_adi.strip():
                    st.error("Urun adi bos olamaz!")
                else:
                    bp = fiyat / miktar if miktar > 0 else fiyat
                    st.session_state.sepet.append({
                        "ad": urun_adi.strip().title(), "miktar": miktar,
                        "birim": birim, "fiyat": fiyat, "birim_fiyat": bp
                    })
                    st.success(f"Eklendi: {urun_adi.title()}")
    with col_sag:
        st.subheader("\U0001f9fe Sepet")
        if not st.session_state.sepet:
            st.info("Sepet bos.")
        else:
            toplam = sum(u["fiyat"] for u in st.session_state.sepet)
            # Her ürünü ayrı satır — 2 kolonlu (bilgi | sil), mobile uyumlu
            sil_index = None
            for i, u in enumerate(st.session_state.sepet):
                col_info, col_btn = st.columns([5, 1])
                with col_info:
                    st.markdown(
                        f"**{u['ad']}** &nbsp; `{u['miktar']} {u['birim']}` &nbsp; "
                        f"**{u['fiyat']:.2f} TL**",
                        unsafe_allow_html=True
                    )
                with col_btn:
                    if st.button("\u274c", key=f"sil_{i}", help=f"{u['ad']} kaldir",
                                 use_container_width=True):
                        sil_index = i
                st.divider()
            if sil_index is not None:
                st.session_state.sepet.pop(sil_index)
                st.rerun()
            st.metric("\U0001f4b0 Toplam", f"{toplam:.2f} TL")
            sc, kc = st.columns(2)
            if sc.button("Sepeti Temizle", use_container_width=True):
                st.session_state.sepet = []
                st.rerun()
            if kc.button("Fisi Kaydet", type="primary", use_container_width=True):
                if not market_adi.strip():
                    st.error("Market adi girin!")
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
                    urun_guncelle(veriler, fis["market"], tarih_str, st.session_state.sepet)
                    verileri_kaydet(veriler)
                    st.session_state.veriler = veriler
                    st.session_state.sepet = []
                    st.success(f"Fis #{fis['id']} kaydedildi! Toplam: {toplam:.2f} TL")
                    st.balloons()
                    st.rerun()

# ─── FİYAT KARŞILAŞTIR ────────────────────────────────────────────────────────
elif sayfa == "\U0001f4b0 Fiyat Karsilastir":
    st.title("\U0001f4b0 Fiyat Karsilastirma")
    st.markdown("---")
    if not veriler["urunler"]:
        st.warning("Henuz urun verisi yok. Once fis ekleyin!")
    else:
        secilen = st.selectbox("Urun secin:", sorted(veriler["urunler"].keys()))
        if secilen:
            kars = []
            for market, kayitlar in veriler["urunler"][secilen].items():
                if kayitlar:
                    son = kayitlar[-1]
                    ort = statistics.mean([k["birim_fiyat"] for k in kayitlar])
                    kars.append({"Market": market, "Son Fiyat (TL)": round(son["birim_fiyat"], 2),
                                 "Ortalama (TL)": round(ort, 2), "Birim": son["birim"],
                                 "Son Tarih": son["tarih"], "Kayit": len(kayitlar)})
            kars.sort(key=lambda x: x["Son Fiyat (TL)"])
            st.subheader(f"{secilen} - Marketler Arasi Karsilastirma")
            if kars:
                ucuz, pahali = kars[0], kars[-1]
                c1, c2, c3 = st.columns(3)
                c1.metric("En Ucuz", ucuz["Market"], f"{ucuz['Son Fiyat (TL)']:.2f} TL")
                c2.metric("En Pahali", pahali["Market"], f"{pahali['Son Fiyat (TL)']:.2f} TL")
                if len(kars) > 1:
                    fark = pahali["Son Fiyat (TL)"] - ucuz["Son Fiyat (TL)"]
                    c3.metric("Fark", f"{fark:.2f} TL",
                              f"%{(fark/ucuz['Son Fiyat (TL)'])*100:.1f}")
                st.markdown("---")
                df_k = pd.DataFrame(kars)
                st.dataframe(df_k, use_container_width=True, hide_index=True)
                fig = px.bar(df_k, x="Market", y="Son Fiyat (TL)", color="Market",
                             text="Son Fiyat (TL)", title=f"{secilen} - Fiyat Karsilastirmasi")
                fig.update_traces(texttemplate="%{text:.2f} TL", textposition="outside")
                st.plotly_chart(fig, use_container_width=True)
                trend = []
                for market, kayitlar in veriler["urunler"][secilen].items():
                    for k in kayitlar:
                        trend.append({"Tarih": k["tarih"], "Birim Fiyat (TL)": k["birim_fiyat"],
                                      "Market": market})
                if trend:
                    st.plotly_chart(px.line(pd.DataFrame(trend), x="Tarih", y="Birim Fiyat (TL)",
                                            color="Market", markers=True,
                                            title=f"{secilen} - Fiyat Trendi"),
                                    use_container_width=True)

# ─── HARCAMA ANALİZİ ──────────────────────────────────────────────────────────
elif sayfa == "\U0001f4ca Harcama Analizi":
    st.title("\U0001f4ca Harcama Analizi")
    st.markdown("---")
    if not veriler["fisler"]:
        st.warning("Henuz fis yok. Once fis ekleyin!")
    else:
        t1, t2, t3, t4 = st.tabs(["Genel Ozet","Markete Gore","Aylik Analiz","Populer Urunler"])
        with t1:
            tf = len(veriler["fisler"]); th = sum(f["toplam"] for f in veriler["fisler"])
            tu = sum(len(f["urunler"]) for f in veriler["fisler"])
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("Fis", tf); c2.metric("Toplam", f"{th:,.2f} TL")
            c3.metric("Ort. Fis", f"{th/tf:,.2f} TL"); c4.metric("Alim", tu)
            c5.metric("Market", len(veriler["marketler"]))
            st.dataframe(pd.DataFrame([{
                "Fis":f"#{f['id']}","Market":f["market"],"Tarih":f["tarih"],
                "Urun":len(f["urunler"]),"Toplam (TL)":f["toplam"]
            } for f in veriler["fisler"]]).sort_values("Fis", ascending=False).reset_index(drop=True),
            use_container_width=True, hide_index=True)
        with t2:
            mh = defaultdict(float); mf = defaultdict(int)
            for f in veriler["fisler"]: mh[f["market"]] += f["toplam"]; mf[f["market"]] += 1
            df_m = pd.DataFrame([{"Market":m,"Toplam (TL)":round(h,2),"Fis":mf[m],
                                   "Ort. Fis (TL)":round(h/mf[m],2)}
                                  for m,h in sorted(mh.items(),key=lambda x:x[1],reverse=True)])
            st.dataframe(df_m, use_container_width=True, hide_index=True)
            col1, col2 = st.columns(2)
            col1.plotly_chart(px.bar(df_m, x="Market", y="Toplam (TL)", color="Market",
                                     title="Markete Gore Harcama"), use_container_width=True)
            col2.plotly_chart(px.pie(df_m, names="Market", values="Toplam (TL)",
                                     title="Harcama Payi"), use_container_width=True)
        with t3:
            ah = defaultdict(float); af = defaultdict(int)
            for f in veriler["fisler"]:
                try:
                    p = f["tarih"].split(".")
                    if len(p)==3: ay=f"{p[1]}.{p[2]}"; ah[ay]+=f["toplam"]; af[ay]+=1
                except: pass
            df_a = pd.DataFrame([{"Ay/Yil":ay,"Harcama (TL)":round(h,2),"Fis":af[ay],
                                   "Gunluk Ort.":round(h/30,2)}
                                  for ay,h in sorted(ah.items())])
            st.dataframe(df_a, use_container_width=True, hide_index=True)
            if not df_a.empty:
                st.plotly_chart(px.line(df_a, x="Ay/Yil", y="Harcama (TL)",
                                        markers=True, title="Aylik Trend"), use_container_width=True)
        with t4:
            ua = defaultdict(int); uh = defaultdict(float)
            for f in veriler["fisler"]:
                for u in f["urunler"]: ua[u["ad"]]+=1; uh[u["ad"]]+=u["fiyat"]
            rows = [{"#":i+1,"Urun":u,"Alim":a,"Harcama (TL)":round(uh[u],2)}
                    for i,(u,a) in enumerate(sorted(ua.items(),key=lambda x:x[1],reverse=True)[:20])]
            df_p = pd.DataFrame(rows)
            st.dataframe(df_p, use_container_width=True, hide_index=True)
            if not df_p.empty:
                st.plotly_chart(px.bar(df_p.head(10), x="Urun", y="Alim",
                                       color="Alim", title="En Cok Alinan 10 Urun",
                                       color_continuous_scale="Greens"),
                                use_container_width=True)

# ─── FİŞLERİ LİSTELE ──────────────────────────────────────────────────────────
elif sayfa == "\U0001f4cb Fisleri Listele":
    st.title("\U0001f4cb Tum Fisler")
    st.markdown("---")
    if not veriler["fisler"]:
        st.warning("Henuz fis yok.")
    else:
        filtre = st.selectbox("Markete Gore Filtre",
                              ["Tumu"] + sorted({f["market"] for f in veriler["fisler"]}))
        goster = veriler["fisler"] if filtre == "Tumu" else [f for f in veriler["fisler"] if f["market"]==filtre]
        for fis in reversed(goster):
            with st.expander(f"Fis #{fis['id']} — {fis['market']} — {fis['tarih']} — {fis['toplam']:.2f} TL"):
                df_f = pd.DataFrame(fis["urunler"])[[ "ad","miktar","birim","fiyat","birim_fiyat"]]
                df_f.columns = ["Urun","Miktar","Birim","Fiyat (TL)","B.Fiyat (TL)"]
                st.dataframe(df_f, use_container_width=True, hide_index=True)

# ─── FİŞ SİL ─────────────────────────────────────────────────────────────────
elif sayfa == "\U0001f5d1\ufe0f Fis Sil":
    st.title("\U0001f5d1\ufe0f Fis Sil")
    st.markdown("---")
    if not veriler["fisler"]:
        st.warning("Henuz fis yok.")
    else:
        st.info(f"Toplam {len(veriler['fisler'])} fis kayitli.")
        # Tablo olarak listele
        df_liste = pd.DataFrame([{
            "ID": f["id"],
            "Market": f["market"],
            "Tarih": f["tarih"],
            "Urun Sayisi": len(f["urunler"]),
            "Toplam (TL)": f["toplam"]
        } for f in reversed(veriler["fisler"])]).reset_index(drop=True)
        st.dataframe(df_liste, use_container_width=True, hide_index=True)
        st.markdown("---")
        st.subheader("Fis Sec ve Sil")
        fis_secenekleri = {
            f"#{f['id']} - {f['market']} - {f['tarih']} - {f['toplam']:.2f} TL": f["id"]
            for f in reversed(veriler["fisler"])
        }
        secilen_label = st.selectbox("Silmek istediginiz fisi secin:", list(fis_secenekleri.keys()))
        secilen_id = fis_secenekleri[secilen_label]
        st.warning(f"**{secilen_label}** silinecek. Bu islem geri alinamaz!")
        if st.button("\U0001f5d1\ufe0f Fisi Kalici Olarak Sil", type="primary", use_container_width=True):
            st.session_state.veriler = fis_sil(veriler, secilen_id)
            st.success("Fis basariyla silindi!")
            st.rerun()

# ─── VERİLERİ DIŞA AKTAR ─────────────────────────────────────────────────────
elif sayfa == "\U0001f4be Verileri Disa Aktar":
    st.title("\U0001f4be Verileri Disa Aktar")
    st.markdown("---")
    if not veriler["fisler"]:
        st.warning("Disa aktarilacak veri yok.")
    else:
        rows = []
        for fis in veriler["fisler"]:
            for u in fis["urunler"]:
                rows.append({"Fis ID":fis["id"],"Market":fis["market"],"Tarih":fis["tarih"],
                              "Urun":u["ad"],"Miktar":u["miktar"],"Birim":u["birim"],
                              "Fiyat":u["fiyat"],"B.Fiyat":u["birim_fiyat"]})
        df_e = pd.DataFrame(rows)
        st.dataframe(df_e, use_container_width=True, hide_index=True)
        st.download_button("CSV Indir", df_e.to_csv(index=False, encoding="utf-8-sig"),
                           f"market_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv",
                           type="primary", use_container_width=True)
        st.download_button("JSON Indir", json.dumps(veriler, ensure_ascii=False, indent=2),
                           "market_verileri.json", "application/json", use_container_width=True)
