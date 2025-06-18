import streamlit as st
from database import init_db, insert_bolag, hamta_alla_bolag, uppdatera_bolag, ta_bort_bolag
import numpy as np

# Initiera databas
init_db()

if 'refresh' not in st.session_state:
    st.session_state['refresh'] = False

def tvinga_uppdatering():
    st.session_state['refresh'] = not st.session_state['refresh']

def berakna_potentiell_kurs(omsattning, antal_aktier, ps_varden):
    ps_genomsnitt = np.mean(ps_varden)
    return (omsattning / antal_aktier) * ps_genomsnitt if antal_aktier else 0

st.title("Enkel Aktieanalysapp")

with st.form("lagg_till_bolag"):
    bolag = st.text_input("Bolag")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    omsattning_i_ar = st.number_input("Förväntad omsättning i år (MSEK)", min_value=0.0, format="%.2f")
    omsattning_nasta_ar = st.number_input("Förväntad omsättning nästa år (MSEK)", min_value=0.0, format="%.2f")
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", min_value=1, format="%d")
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
    ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f")

    lagg_till = st.form_submit_button("Lägg till bolag")

if lagg_till:
    if bolag.strip() == "":
        st.error("Ange bolagsnamn!")
    else:
        insert_bolag(
            bolag.strip(),
            nuvarande_kurs,
            omsattning_i_ar,
            omsattning_nasta_ar,
            antal_aktier,
            ps1, ps2, ps3, ps4, ps5
        )
        st.success(f"{bolag} har lagts till.")
        tvinga_uppdatering()

bolag_lista = hamta_alla_bolag()

for bolag_info in bolag_lista:
    omsattning_i_ar = bolag_info["omsattning_i_ar"]
    omsattning_nasta_ar = bolag_info["omsattning_nasta_ar"]
    antal_aktier = bolag_info["antal_aktier"]
    ps_varden = [bolag_info["ps1"], bolag_info["ps2"], bolag_info["ps3"], bolag_info["ps4"], bolag_info["ps5"]]

    pot_kurs_idag = berakna_potentiell_kurs(omsattning_i_ar, antal_aktier, ps_varden)
    pot_kurs_arskiftet = berakna_potentiell_kurs(omsattning_nasta_ar, antal_aktier, ps_varden)

    undervardering_idag = (pot_kurs_idag - bolag_info["nuvarande_kurs"]) / bolag_info["nuvarande_kurs"] * 100 if bolag_info["nuvarande_kurs"] > 0 else 0
    undervardering_arskiftet = (pot_kurs_arskiftet - bolag_info["nuvarande_kurs"]) / bolag_info["nuvarande_kurs"] * 100 if bolag_info["nuvarande_kurs"] > 0 else 0

    bolag_info.update({
        "pot_kurs_idag": pot_kurs_idag,
        "pot_kurs_arskiftet": pot_kurs_arskiftet,
        "undervardering_idag": undervardering_idag,
        "undervardering_arskiftet": undervardering_arskiftet
    })

bolag_lista.sort(key=lambda b: b["undervardering_arskiftet"], reverse=True)

if "index" not in st.session_state:
    st.session_state.index = 0

def visa_bolag(index):
    bolag_info = bolag_lista[index]
    st.header(f"Bolag: {bolag_info['bolag']}")
    st.write(f"Nuvarande kurs: {bolag_info['nuvarande_kurs']:.2f} SEK")
    st.write(f"Potentiell kurs idag: {bolag_info['pot_kurs_idag']:.2f} SEK")
    st.write(f"Potentiell kurs i slutet av året: {bolag_info['pot_kurs_arskiftet']:.2f} SEK")
    st.write(f"Under-/Övervärdering idag: {bolag_info['undervardering_idag']:.2f} %")
    st.write(f"Under-/Övervärdering i slutet av året: {bolag_info['undervardering_arskiftet']:.2f} %")

    with st.expander("Redigera bolag"):
        ny_nuvarande_kurs = st.number_input("Nuvarande kurs", value=bolag_info['nuvarande_kurs'], format="%.2f", key=f"edit_nuvarande_{index}")
        ny_omsattning_i_ar = st.number_input("Förväntad omsättning i år (MSEK)", value=bolag_info['omsattning_i_ar'], format="%.2f", key=f"edit_omsattning_i_ar_{index}")
        ny_omsattning_nasta_ar = st.number_input("Förväntad omsättning nästa år (MSEK)", value=bolag_info['omsattning_nasta_ar'], format="%.2f", key=f"edit_omsattning_nasta_ar_{index}")
        ny_antal_aktier = st.number_input("Antal utestående aktier (miljoner)", value=bolag_info['antal_aktier'], format="%d", key=f"edit_antal_aktier_{index}")
        ny_ps1 = st.number_input("P/S 1", value=bolag_info['ps1'], format="%.2f", key=f"edit_ps1_{index}")
        ny_ps2 = st.number_input("P/S 2", value=bolag_info['ps2'], format="%.2f", key=f"edit_ps2_{index}")
        ny_ps3 = st.number_input("P/S 3", value=bolag_info['ps3'], format="%.2f", key=f"edit_ps3_{index}")
        ny_ps4 = st.number_input("P/S 4", value=bolag_info['ps4'], format="%.2f", key=f"edit_ps4_{index}")
        ny_ps5 = st.number_input("P/S 5", value=bolag_info['ps5'], format="%.2f", key=f"edit_ps5_{index}")

        if st.button("Spara ändringar", key=f"spara_{index}"):
            uppdatera_bolag(
                bolag_info["id"],
                bolag_info["bolag"],
                ny_nuvarande_kurs,
                ny_omsattning_i_ar,
                ny_omsattning_nasta_ar,
                ny_antal_aktier,
                ny_ps1, ny_ps2, ny_ps3, ny_ps4, ny_ps5
            )
            st.success("Ändringar sparade!")
            tvinga_uppdatering()

    if st.button("Ta bort bolag", key=f"ta_bort_{index}"):
        ta_bort_bolag(bolag_info["id"])
        st.success(f"Bolag {bolag_info['bolag']} borttaget.")
        if st.session_state.index >= len(bolag_lista) - 1:
            st.session_state.index = max(0, len(bolag_lista) - 2)
        tvinga_uppdatering()

if bolag_lista:
    visa_bolag(st.session_state.index)
    col1, col2, col3 = st.columns([1,4,1])
    with col1:
        if st.button("⬅️ Föregående") and st.session_state.index > 0:
            st.session_state.index -= 1
            tvinga_uppdatering()
    with col3:
        if st.button("Nästa ➡️") and st.session_state.index < len(bolag_lista) - 1:
            st.session_state.index += 1
            tvinga_uppdatering()
else:
    st.info("Inga bolag tillagda än.")
