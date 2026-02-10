import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
import time

# --- KONFIGURATION ---
st.set_page_config(page_title="Bau-News Weltklasse", layout="wide", initial_sidebar_state="expanded")

# --- SICHERHEITS-CHECK ---
def check_auth():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        st.title("🔐 Interner Bereich - Baustoffhandel")
        user = st.text_input("Benutzer")
        pw = st.text_input("Passwort", type="password")
        code = st.text_input("Mobil-Code (2FA)")
        if st.button("Einloggen"):
            # Nutze deine gewünschten Daten (später in Streamlit Secrets ändern)
            if pw == "weltklasse2026" and code == "123456":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Zugriff verweigert.")
        return False
    return True

if check_auth():
    # --- SIDEBAR: LIEFERANTEN-AUSWAHL ---
    st.sidebar.title("🏢 Lieferanten-Radar")
    # Alle Lieferanten aus deinen Screenshots (Auszug)
    lieferanten = [
        "1 A Bauchemie", "ABC Klinker", "ACO", "Ante", "Ardex", "Bauder", "Baumit", 
        "BMI", "Bostik", "Danogips", "Dyckerhoff", "Egger", "Fischer", "Gutex", 
        "Heidelberg Materials", "Kingspan", "Knauf", "Mapei", "PCI", "Remmers", 
        "Rockwool", "Saint-Gobain", "Steico", "Wienerberger", "Xella", "Zambelli"
    ]
    auswahl = st.sidebar.multiselect("Fokus-Partner", lieferanten, default=["Ante", "Egger", "Steico"])

    # --- HAUPTBEREICH ---
    st.title("🏗️ Bau-Handels-Cockpit 2026")
    
    # QUADRANT 1 & 2: MARKT & ENERGIE
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Bauzins 10J", "3,55 %", "+0,05 %")
        st.caption("EZB Leitzins: 2,15 %")
    with col2:
        st.metric("Strom (Börse)", "105 €/MWh", "-15 %")
        st.metric("Gas (Neu)", "9,27 ct/kWh", "+1,4 ct CO2")
    with col3:
        st.warning("⚠️ CBAM-Frist: 31.03.2026")
        st.info("📦 Zollfreigrenze 150€ entfällt")

    st.divider()

    # QUADRANT 3: HOLZMARKT-PROGNOSE (KVH, OSB, BSH)
    st.header("🌲 Holz-Monitor (Vorprodukte & Trends)")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        fig = go.Figure()
        wochen = ['KW03', 'KW04', 'KW05', 'KW06']
        fig.add_trace(go.Scatter(x=wochen, y=[450, 465, 480, 485], name="KVH (€/m³)", line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=wochen, y=[125, 128, 130, 130], name="Rundholz Fichte (€/fm)", line=dict(dash='dot')))
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.write("**KI-Prognose OSB:**")
        st.error("Preisanstieg +7 %")
        st.write("Grund: Neue EU-Harzverordnung 2026.")

    st.divider()

    # QUADRANT 4: TÄGLICHER MARKTBERICHT
    st.header("📋 Täglicher Marktbericht Niedersachsen")
    with st.expander("Bericht vom 10.02.2026 öffnen", expanded=True):
        st.markdown(f"""
        **Marktlage:** Holzpreise ziehen durch Sanierungs-Boom an. Rundholz bei 130 €/fm stabil.
        **Vertriebs-Tipp:** NBank bietet aktuell **100.000 € Darlehen** für Wohneigentum. 
        Ideal für Kunden von {', '.join(auswahl)}.
        **Zoll-Check:** Prüfung der Stahl-Zertifikate bei Befestigungstechnik-Partnern zwingend.
        """)
        if st.button("Bericht als PDF exportieren"):
            st.toast("PDF wird generiert...")

    # FOOTER
    st.sidebar.markdown("---")
    if st.sidebar.button("Abmelden"):
        st.session_state.auth = False
        st.rerun()
