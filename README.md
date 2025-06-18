# 📊 Aktieanalys med P/S-tal

En enkel och interaktiv Streamlit-app för att analysera aktier utifrån:
- P/S-tal
- Förväntad omsättning
- Antal utestående aktier
- Nuvarande kurs

Appen beräknar potentiella aktiekurser idag och i slutet av året samt visar om aktien är under- eller övervärderad i %.

## 🚀 Funktioner

- Lägg till nya bolag
- Spara all data i databas (`/mnt/data/database.db`)
- Redigera och ta bort bolag med ett klick
- Visuell bläddringsfunktion mellan bolag
- Sortering: Mest undervärderad aktie visas först
- Automatisk %-beräkning utifrån nuvarande kurs
- All data bevaras vid omstart (via Streamlit Cloud)

## 🧠 Beräkningar

**Potentiell kurs idag**  
= (Omsättning i år / Antal aktier) × Genomsnittligt P/S-tal

**Potentiell kurs slut året**  
= (Omsättning nästa år / Antal aktier) × Genomsnittligt P/S-tal

**Över-/undervärdering (%)**  
= ((Potentiell kurs / Nuvarande kurs) - 1) × 100

## 🌐 Streamlit Cloud

Appen är optimerad för [Streamlit Cloud](https://streamlit.io/cloud) och använder:
- Persistent datalagring: `/mnt/data/database.db`
- Kräver inte någon extern databas eller backend

## 🛠️ Installation lokalt (valfritt)

```bash
git clone https://github.com/ditt-användarnamn/ditt-repo.git
cd ditt-repo
pip install -r requirements.txt
streamlit run app.py
