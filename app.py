import streamlit as st
import pandas as pd
from database import init_db, insert_company, get_all_companies, update_company, delete_company

# Initiera databasen
init_db()

st.set_page_config(page_title="Aktieanalys med P/S-tal", layout="centered")

st.title("📊 Aktieanalys med P/S-tal")

# --- Formulär för att lägga till ett nytt bolag ---
st.subheader("➕ Lägg till bolag")
with st.form("add_company_form"):
    namn = st.text_input("Bolagsnamn")
    nuvarande_kurs = st.number_input("Nuvarande kurs", step=0.01)
    omsättning_i_år = st.number_input("Förväntad omsättning i år (MSEK)", step=1.0)
    omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år (MSEK)", step=1.0)
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", step=0.1)
    ps1 = st.number_input("P/S 1", step=0.1)
    ps2 = st.number_input("P/S 2", step=0.1)
    ps3 = st.number_input("P/S 3", step=0.1)
    ps4 = st.number_input("P/S 4", step=0.1)
    ps5 = st.number_input("P/S 5", step=0.1)

    skicka = st.form_submit_button("Lägg till bolag")
    if skicka and namn:
        data = (
            namn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år,
            antal_aktier, ps1, ps2, ps3, ps4, ps5
        )
        insert_company(data)
        st.success(f"Bolaget {namn} har lagts till!")

# --- Hämta data ---
rows = get_all_companies()

if not rows:
    st.info("Inga bolag har lagts till ännu.")
    st.stop()

# --- Skapa DataFrame och beräkningar ---
df = pd.DataFrame(rows, columns=[
    "id", "Bolag", "Nuvarande kurs", "Omsättning i år", "Omsättning nästa år",
    "Antal aktier", "P/S1", "P/S2", "P/S3", "P/S4", "P/S5"
])

df["P/S snitt"] = df[["P/S1", "P/S2", "P/S3", "P/S4", "P/S5"]].mean(axis=1)
df["Pot. kurs idag"] = (df["Omsättning i år"] / df["Antal aktier"]) * df["P/S snitt"]
df["Pot. kurs slut året"] = (df["Omsättning nästa år"] / df["Antal aktier"]) * df["P/S snitt"]
df["% diff idag"] = ((df["Pot. kurs idag"] / df["Nuvarande kurs"]) - 1) * 100
df["% diff slut året"] = ((df["Pot. kurs slut året"] / df["Nuvarande kurs"]) - 1) * 100

# --- Sortera efter mest undervärderad slutet av året ---
df.sort_values("% diff slut året", ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

# --- Bläddra bolag ett i taget ---
st.subheader("📈 Bolagsanalyser")

index = st.number_input("📘 Välj bolag att visa", min_value=0, max_value=len(df)-1, step=1)

row = df.loc[index]

st.markdown(f"### {row['Bolag']}")
st.metric("💰 Nuvarande kurs", f"{row['Nuvarande kurs']:.2f} kr")

col1, col2 = st.columns(2)
with col1:
    st.metric("📍 Potentiell kurs idag", f"{row['Pot. kurs idag']:.2f} kr", f"{row['% diff idag']:.1f} %")
with col2:
    st.metric("📈 Potentiell kurs slut året", f"{row['Pot. kurs slut året']:.2f} kr", f"{row['% diff slut året']:.1f} %")

# --- Redigering och borttagning ---
st.subheader("⚙️ Redigera bolagsdata")

fält_namn = {
    "Nuvarande kurs": "Nuvarande kurs",
    "Omsättning i år": "Omsättning i år",
    "Omsättning nästa år": "Omsättning nästa år",
    "Antal aktier": "Antal aktier",
    "P/S1": "P/S1",
    "P/S2": "P/S2",
    "P/S3": "P/S3",
    "P/S4": "P/S4",
    "P/S5": "P/S5"
}

databas_fält = {
    "Nuvarande kurs": "current_price",
    "Omsättning i år": "revenue_this_year",
    "Omsättning nästa år": "revenue_next_year",
    "Antal aktier": "shares_outstanding",
    "P/S1": "ps1",
    "P/S2": "ps2",
    "P/S3": "ps3",
    "P/S4": "ps4",
    "P/S5": "ps5"
}

ändrad = False
ändrade_värden = {}

for visningsnamn, db_namn in databas_fält.items():
    nytt_värde = st.number_input(visningsnamn, value=float(row[visningsnamn]), step=0.1, key=f"edit_{visningsnamn}")
    if nytt_värde != float(row[visningsnamn]):
        ändrade_värden[db_namn] = nytt_värde
        ändrad = True

if ändrad:
    for fält, värde in ändrade_värden.items():
        update_company(int(row["id"]), fält, värde)
    st.experimental_rerun()

if st.button("🗑️ Ta bort bolag"):
    delete_company(int(row["id"]))
    st.success(f"Bolaget {row['Bolag']} har tagits bort.")
    st.experimental_rerun()
