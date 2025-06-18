import streamlit as st
from database import (
    init_db, lägg_till_bolag, hamta_alla_bolag,
    uppdatera_bolag, ta_bort_bolag
)
import os

# Initiera databasen
init_db()

st.set_page_config(page_title="Aktieanalys med P/S-tal", layout="wide")
st.title("📈 Aktieanalys med P/S-tal")

# Formulär: Lägg till nytt bolag
st.header("Lägg till nytt bolag")
with st.form("nytt_bolag_formulär", clear_on_submit=True):
    bolagsnamn = st.text_input("Bolagsnamn")
    nuvarande_kurs = st.number_input("Nuvarande kurs", format="%.2f")
    omsättning_år = st.number_input("Förväntad omsättning i år (MSEK)", format="%.0f")
    omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år (MSEK)", format="%.0f")
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", format="%.2f")
    ps1 = st.number_input("P/S 1", format="%.2f")
    ps2 = st.number_input("P/S 2", format="%.2f")
    ps3 = st.number_input("P/S 3", format="%.2f")
    ps4 = st.number_input("P/S 4", format="%.2f")
    ps5 = st.number_input("P/S 5", format="%.2f")
    skicka = st.form_submit_button("Lägg till bolag")

    if skicka:
        lägg_till_bolag(
            bolagsnamn, nuvarande_kurs, omsättning_år,
            omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5
        )
        st.success(f"Bolaget {bolagsnamn} har lagts till.")

# Hämta bolag och sortera
alla_bolag = hamta_alla_bolag()

def beräkna_pot_kurser(bolag):
    genomsnitt_ps = sum(bolag[6:11]) / 5
    pot_kurs_idag = (bolag[3] / bolag[5]) * genomsnitt_ps if bolag[5] != 0 else 0
    pot_kurs_slutåret = (bolag[4] / bolag[5]) * genomsnitt_ps if bolag[5] != 0 else 0
    övervärdering_idag = ((pot_kurs_idag - bolag[2]) / bolag[2]) * 100 if bolag[2] != 0 else 0
    övervärdering_slutåret = ((pot_kurs_slutåret - bolag[2]) / bolag[2]) * 100 if bolag[2] != 0 else 0
    return pot_kurs_idag, pot_kurs_slutåret, övervärdering_idag, övervärdering_slutåret

# Sortera bolag utifrån mest undervärderad baserat på slutårets potentiella kurs
alla_bolag.sort(key=lambda x: beräkna_pot_kurser(x)[3], reverse=True)

# Visa tabell
st.header("📊 Översikt över bolag")
for index, bolag in enumerate(alla_bolag):
    pot_kurs_idag, pot_kurs_slutåret, över_idag, över_slut = beräkna_pot_kurser(bolag)

    färg = "🟢" if pot_kurs_slutåret > bolag[2] else "🔴"

    with st.expander(f"{färg} {bolag[1]} – Nuvarande kurs: {bolag[2]:.2f} kr"):
        st.write(f"**Förväntad omsättning i år:** {bolag[3]:,.0f} MSEK")
        st.write(f"**Förväntad omsättning nästa år:** {bolag[4]:,.0f} MSEK")
        st.write(f"**Antal aktier:** {bolag[5]:,.2f} miljoner")
        st.write(f"**P/S-tal (1–5):** {', '.join([str(round(p,2)) for p in bolag[6:11]])}")
        st.write(f"**Potentiell kurs idag:** {pot_kurs_idag:.2f} kr ({över_idag:.1f}%)")
        st.write(f"**Potentiell kurs slutet av året:** {pot_kurs_slutåret:.2f} kr ({över_slut:.1f}%)")

        # Redigera formulär
        with st.form(f"redigera_{index}"):
            ny_kurs = st.number_input("Ny nuvarande kurs", value=float(bolag[2]), format="%.2f")
            ny_oms_år = st.number_input("Ny omsättning i år", value=float(bolag[3]), format="%.0f")
            ny_oms_nästa = st.number_input("Ny omsättning nästa år", value=float(bolag[4]), format="%.0f")
            ny_aktier = st.number_input("Nytt antal aktier", value=float(bolag[5]), format="%.2f")
            ny_ps = [
                st.number_input(f"Nytt P/S {i+1}", value=float(bolag[6+i]), format="%.2f")
                for i in range(5)
            ]
            ändra = st.form_submit_button("Spara ändringar")
            if ändra:
                uppdatera_bolag(bolag[0], ny_kurs, ny_oms_år, ny_oms_nästa, ny_aktier, *ny_ps)
                st.success("Ändringar sparade.")
                st.session_state["uppdaterad"] = True

        # Radera bolag
        if st.button(f"Ta bort {bolag[1]}", key=f"ta_bort_{index}"):
            ta_bort_bolag(bolag[0])
            st.success(f"{bolag[1]} har tagits bort.")
            st.session_state["uppdaterad"] = True

# Om något uppdaterats, ladda om sidan
if "uppdaterad" in st.session_state:
    del st.session_state["uppdaterad"]
    st.experimental_rerun()
