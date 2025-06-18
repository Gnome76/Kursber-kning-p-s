import streamlit as st
from database import (
    init_db, insert_company, get_all_companies,
    update_company, delete_company
)
import os

st.set_page_config(page_title="Aktieanalys", layout="wide")

# Initiera databas
init_db()

# Hjälpfunktion för att räkna ut potentiella kurser
def beräkna_potentiella_kurser(row):
    snitt_ps = sum(row[6:11]) / 5
    potentiell_kurs_idag = (row[3] / row[5]) * snitt_ps
    potentiell_kurs_slutet_av_året = (row[4] / row[5]) * snitt_ps
    under_over_idag = ((potentiell_kurs_idag - row[2]) / row[2]) * 100
    under_over_slutet = ((potentiell_kurs_slutet_av_året - row[2]) / row[2]) * 100
    return potentiell_kurs_idag, potentiell_kurs_slutet_av_året, under_over_idag, under_over_slutet

st.title("📈 Aktieanalys")

# Lägga till nytt bolag
with st.expander("➕ Lägg till nytt bolag"):
    with st.form("add_company"):
        bolag = st.text_input("Bolag")
        nuvarande_kurs = st.number_input("Nuvarande kurs", format="%.2f")
        omsättning_i_år = st.number_input("Förväntad omsättning i år", format="%.0f")
        omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år", format="%.0f")
        antal_aktier = st.number_input("Antal utestående aktier", format="%.0f")
        ps1 = st.number_input("P/S 1", format="%.2f")
        ps2 = st.number_input("P/S 2", format="%.2f")
        ps3 = st.number_input("P/S 3", format="%.2f")
        ps4 = st.number_input("P/S 4", format="%.2f")
        ps5 = st.number_input("P/S 5", format="%.2f")
        submitted = st.form_submit_button("Lägg till bolag")
        if submitted and bolag:
            insert_company(bolag, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5)
            st.success("Bolag tillagt.")
            st.session_state["refresh"] = True

# Hämta alla bolag
companies = get_all_companies()

# Sortera bolagen efter mest undervärderade (baserat på slutet av året)
bolag_beräkningar = []
for row in companies:
    pki, pks, uo_idag, uo_slut = beräkna_potentiella_kurser(row)
    bolag_beräkningar.append((row, pki, pks, uo_idag, uo_slut))

bolag_beräkningar.sort(key=lambda x: x[4], reverse=True)

if "bolags_index" not in st.session_state:
    st.session_state["bolags_index"] = 0

if bolag_beräkningar:
    index = st.session_state["bolags_index"]
    row, pki, pks, uo_idag, uo_slut = bolag_beräkningar[index]
    st.subheader(f"{row[1]}")

    st.markdown(f"""
    **Nuvarande kurs:** {row[2]:.2f} kr  
    **Potentiell kurs (idag):** {pki:.2f} kr ({uo_idag:+.1f}%)  
    **Potentiell kurs (slutet av året):** {pks:.2f} kr ({uo_slut:+.1f}%)  
    """)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Föregående", disabled=index == 0):
            st.session_state["bolags_index"] -= 1
    with col2:
        if st.button("Nästa ➡️", disabled=index == len(bolag_beräkningar) - 1):
            st.session_state["bolags_index"] += 1

    with st.expander("✏️ Redigera bolag"):
        with st.form(f"edit_{row[0]}"):
            nuvarande_kurs = st.number_input("Nuvarande kurs", value=row[2], format="%.2f")
            omsättning_i_år = st.number_input("Förväntad omsättning i år", value=row[3], format="%.0f")
            omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år", value=row[4], format="%.0f")
            antal_aktier = st.number_input("Antal utestående aktier", value=row[5], format="%.0f")
            ps1 = st.number_input("P/S 1", value=row[6], format="%.2f")
            ps2 = st.number_input("P/S 2", value=row[7], format="%.2f")
            ps3 = st.number_input("P/S 3", value=row[8], format="%.2f")
            ps4 = st.number_input("P/S 4", value=row[9], format="%.2f")
            ps5 = st.number_input("P/S 5", value=row[10], format="%.2f")
            update = st.form_submit_button("Spara ändringar")
            if update:
                update_company(row[0], nuvarande_kurs, omsättning_i_år, omsättning_nästa_år,
                               antal_aktier, ps1, ps2, ps3, ps4, ps5)
                st.success("Bolag uppdaterat.")
                st.session_state["refresh"] = True

    if st.button("🗑️ Ta bort bolag"):
        delete_company(row[0])
        st.success("Bolag borttaget.")
        st.session_state["refresh"] = True

# Tvinga uppdatering om ändringar skett
if st.session_state.get("refresh"):
    st.session_state["refresh"] = False
    st.experimental_rerun()
