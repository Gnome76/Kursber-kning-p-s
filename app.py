import streamlit as st
from database import (
    initiera_databas,
    lägg_till_bolag,
    hämta_alla_bolag,
    uppdatera_bolag,
    ta_bort_bolag,
)
import statistics

st.set_page_config(page_title="Aktieanalys", layout="wide")
initiera_databas()

st.title("📈 Aktieanalys baserat på P/S-tal")

# Formulär för att lägga till nytt bolag
with st.form("lägg_till"):
    st.subheader("Lägg till nytt bolag")
    bolagsnamn = st.text_input("Bolagsnamn")
    nuvarande_kurs = st.number_input("Nuvarande kurs", format="%.2f")
    omsättning_i_år = st.number_input("Förväntad omsättning i år (MSEK)", format="%.0f")
    omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år (MSEK)", format="%.0f")
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", format="%.0f")
    ps1 = st.number_input("P/S-tal 1", format="%.2f")
    ps2 = st.number_input("P/S-tal 2", format="%.2f")
    ps3 = st.number_input("P/S-tal 3", format="%.2f")
    ps4 = st.number_input("P/S-tal 4", format="%.2f")
    ps5 = st.number_input("P/S-tal 5", format="%.2f")
    skicka = st.form_submit_button("Lägg till")

    if skicka and bolagsnamn:
        lägg_till_bolag(
            bolagsnamn, nuvarande_kurs, omsättning_i_år,
            omsättning_nästa_år, antal_aktier,
            ps1, ps2, ps3, ps4, ps5
        )
        st.success(f"{bolagsnamn} har lagts till.")

# Hämta bolag
bolag = hämta_alla_bolag()

if bolag:
    st.subheader("📊 Lista över bolag")

    tabell_data = []
    for b in bolag:
        medel_ps = statistics.mean(b[6:11])
        potentiell_kurs_idag = (b[3] / b[5]) * medel_ps
        potentiell_kurs_slut = (b[4] / b[5]) * medel_ps
        övervärdering = ((potentiell_kurs_slut - b[2]) / b[2]) * 100
        tabell_data.append({
            "ID": b[0],
            "Bolag": b[1],
            "Nuvarande kurs": b[2],
            "Potentiell kurs (idag)": round(potentiell_kurs_idag, 2),
            "Potentiell kurs (slutet av året)": round(potentiell_kurs_slut, 2),
            "Undervärdering (%)": round(övervärdering, 2)
        })

    sorterad = sorted(tabell_data, key=lambda x: x["Undervärdering (%)"], reverse=True)
    st.dataframe(sorterad, use_container_width=True)

    # Formulär för redigering
    st.subheader("✏️ Redigera bolag")
    valt_bolag = st.selectbox("Välj bolag att redigera", bolag, format_func=lambda x: x[1])

    with st.form("uppdatera"):
        ny_kurs = st.number_input("Ny kurs", value=valt_bolag[2], format="%.2f")
        ny_oms_år = st.number_input("Omsättning i år", value=valt_bolag[3], format="%.0f")
        ny_oms_nästa = st.number_input("Omsättning nästa år", value=valt_bolag[4], format="%.0f")
        ny_aktier = st.number_input("Antal aktier", value=valt_bolag[5], format="%.0f")
        ny_ps = [st.number_input(f"P/S {i+1}", value=valt_bolag[6+i], format
