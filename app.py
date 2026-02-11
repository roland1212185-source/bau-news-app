import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfiguration & Design
st.set_page_config(page_title="Bau-Handels-Cockpit 2026", layout="wide")

# Login-Logik (vereinfacht für den Test, da du ja schon eingeloggt bist)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True # Wir setzen es auf True für den Schnellstart

# 2. Daten-Datenbank für Lieferanten
news_daten = [
    {"Firma": "Egger", "Kategorie": "Preise", "Titel": "Egger OSB-Preisanpassung", "Inhalt": "Preiserhöhung von +6% für alle OSB 3/4 Lieferungen ab März 2026 angekündigt."},
    {"Firma": "Egger", "Kategorie": "Produkt", "Titel": "Neue Kollektion 24+", "Inhalt": "Lagerbestand für neue Dekore im Werk Wismar ab KW09 verfügbar."},
    {"Firma": "Ante", "Kategorie": "Logistik", "Titel": "KVH Lieferzeiten Ante", "Inhalt": "Aktuelle Lieferzeit für Standardquerschnitte liegt stabil bei 5-7 Werktagen."},
    {"Firma": "Ante", "Kategorie": "Preise", "Titel": "Rundholz-Zuschlag", "Inhalt": "Anpassung der Frachtpauschalen für Langholz aufgrund gestiegener Mautgebühren."},
    {"Firma": "Steico", "Kategorie": "Förderung", "Titel": "Steicozell Einblasdämmung", "Inhalt": "Neue Zertifizierung für staatliche BEG-Förderung (NBank/KfW) erfolgreich abgeschlossen."},
    {"Firma": "Steico", "Kategorie": "Produkt", "Titel": "Steico Duo Dry", "Inhalt": "Bestände für 60mm Platten im Zentrallager aktuell knapp - Vorlaufzeit einplanen."},
    {"Firma": "Allgemein", "Kategorie": "Markt", "Titel": "NBank Neubau-Förderung", "Inhalt": "Neues Programm für Familien in Niedersachsen ab April 2026 verfügbar."}
]

# 3. Sidebar (Das Auswahlmenü)
st.sidebar.header("Lieferanten-Radar")
auswahl = st.sidebar.multiselect(
    "Wähle deine Partner aus:",
    ["Egger", "Ante", "Steico"],
    default=["Egger", "Ante", "Steico"] # Standardmäßig alle anzeigen
)

# 4. Hauptbereich des Dashboards
st.title("🏗️ Bau-Handels-Cockpit 2026")
st.write(f"Willkommen im geschützten Bereich. Stand: {pd.to_datetime('today').strftime('%d.%m.%Y')}")

# Kennzahlen-Reihe
col1, col2, col3 = st.columns(3)
col1.metric("Bauzins 10J", "3,55 %", "-0,1 %")
col2.metric("Holz-Index", "142 Pkt", "+4,2 %")
col3.metric("Lager-Umschlag", "12 Tage", "-2 Tage")

st.divider()

# 5. News-Bereich mit Filter
st.header("📢 Aktuelle Lieferanten-News")

# Filtern der Daten basierend auf der Auswahl
gefilterte_news = [n for n in news_daten if n['Firma'] in auswahl or n['Firma'] == "Allgemein"]

if not auswahl:
    st.info("Bitte wähle links einen Lieferanten aus, um spezifische News zu sehen.")
else:
    for news in gefilterte_news:
        with st.expander(f"{news['Firma']} - {news['Titel']}"):
            st.write(f"**Kategorie:** {news['Kategorie']}")
            st.write(news['Inhalt'])

# 6. Preis-Chart (Fokus auf Rundholz)
st.divider()
st.header("📈 Marktpreis Rundholz (Fichte/Kiefer)")

# Hier trägst du deine aktuellen Preise ein (€ pro Festmeter)
rundholz_daten = pd.DataFrame({
    'Woche': ['KW03', 'KW04', 'KW05', 'KW06', 'KW07'],
    'Rundholz Preis (€/fm)': [95, 98, 102, 105, 108] 
})

fig = px.line(
    rundholz_daten, 
    x='Woche', 
    y='Rundholz Preis (€/fm)', 
    markers=True,
    title="Entwicklung Rundholz-Leitpreis (Sortiment 2b+)",
    line_shape="spline",
    color_discrete_sequence=['#8B4513'] # Holz-Braun
)

# Design-Feinschliff
fig.update_layout(
    yaxis_title="Preis in € pro Festmeter", 
    xaxis_title="Kalenderwoche",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

