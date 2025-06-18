import streamlit as st
from database import init_db, insert_bolag, hamta_alla_bolag, uppdatera_bolag, ta_bort_bolag
import os

# Initiera databas
init_db()

st.set_page_config(page_title="Aktieanalysapp", layout="centered")

st.title("Aktieanalysapp")

# Funktioner för beräkningar
def berakna_potentiell_kurs(omsattning, antal_aktier, ps_varden):
    ps_medel = sum(ps_varden) / len(ps_varden)
    return (omsattning / antal_aktier) * ps_medel

def berakna_undervardering(pot_kurs, nuv_kurs):
    return ((pot_kurs - nuv_kurs) / nuv_kurs) * 100

# Hämta bolagsdata från DB
bolag_lista = hamta_alla_bolag()

# Sortera bolagen på mest undervärderad (högst % undervärdering först)
sorterad_bolag = []
for b in bolag_lista:
    ps_varden = b[6:11]
    pot_kurs_idag = berakna_potentiell_kurs(b[3], b[5], ps_varden)
    pot_kurs_nasta_ar = berakna_potentiell_kurs(b[4], b[5], ps_varden)
    undervardering = berakna_undervardering(pot_kurs_nasta_ar, b[2])
    sorterad_bolag.append((b, pot_kurs_idag, pot_kurs_nasta_ar, undervardering))

sorterad_bolag.sort(key=lambda x: x[3], reverse=True)

# Session state för nuvarande bolagsindex
if "index" not in st.session_state:
    st.session_state.index = 0

# Visa bolagsinfo om bolag finns
if not sorterad_bolag:
    st.info("Inga bolag inlagda ännu.")
else:
    idx = st.session_state.index
    if idx >= len(sorterad_bolag):
        idx = 0
        st.session_state.index = 0

    bolag, pot_idag, pot_nasta_ar, underv = sorterad_bolag[idx]

    with st.form("redigera_bolag"):
        st.header(f"Bolag: {bolag[1]}")

        bolagsnamn = st.text_input("Bolag", value=bolag[1])
        nuvarande_kurs = st.number_input("Nuvarande kurs", value=bolag[2], format="%.2f")
        omsattning_i_ar = st.number_input("Förväntad omsättning i år", value=bolag[3], format="%.2f")
        omsattning_nasta_ar = st.number_input("Förväntad omsättning nästa år", value=bolag[4], format="%.2f")
        antal_aktier = st.number_input("Antal utestående aktier", value=bolag[5], format="%.0f")
        ps1 = st.number_input("P/S 1", value=bolag[6], format="%.2f")
        ps2 = st.number_input("P/S 2", value=bolag[7], format="%.2f")
        ps3 = st.number_input("P/S 3", value=bolag[8], format="%.2f")
        ps4 = st.number_input("P/S 4", value=bolag[9], format="%.2f")
        ps5 = st.number_input("P/S 5", value=bolag[10], format="%.2f")

        knapp_uppdatera = st.form_submit_button("Spara ändringar")
        knapp_radera = st.form_submit_button("Ta bort bolag")

        if knapp_uppdatera:
            uppdatera_bolag(bolag[0], bolagsnamn, nuvarande_kurs, omsattning_i_ar, omsattning_nasta_ar,
                           antal_aktier, ps1, ps2, ps3, ps4, ps5)
            st.success("Ändringar sparade!")

        if knapp_radera:
            ta_bort_bolag(bolag[0])
            st.success(f"Bolag '{bolag[1]}' borttaget!")
            if st.session_state.index > 0:
                st.session_state.index -= 1

    st.markdown("---")

    # Visa beräkningar
    st.subheader("Beräkningar")
    st.write(f"Potentiell kurs idag: **{pot_idag:.2f}**")
    st.write(f"Potentiell kurs om ett år: **{pot_nasta_ar:.2f}**")

    underv_text = f"Undervärdering baserat på framtida kurs: **{underv:.2f} %**"
    if underv > 0:
        st.markdown(f"<span style='color:green'>{underv_text}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color:red'>{underv_text}</span>", unsafe_allow_html=True)

    # Navigeringsknappar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Föregående") and st.session_state.index > 0:
            st.session_state.index -= 1
    with col3:
        if st.button("Nästa ➡️") and st.session_state.index < len(sorterad_bolag) - 1:
            st.session_state.index += 1

    st.markdown("---")

# Formulär för att lägga till nytt bolag
with st.form("nytt_bolag"):
    st.header("Lägg till nytt bolag")
    bolagsnamn_nytt = st.text_input("Bolag", key="ny_bolag")
    nuvarande_kurs_nytt = st.number_input("Nuvarande kurs", format="%.2f", key="ny_nuv_kurs")
    oms_i_ar_nytt = st.number_input("Förväntad omsättning i år", format="%.2f", key="ny_oms_i_ar")
    oms_nasta_ar_nytt = st.number_input("Förväntad omsättning nästa år", format="%.2f", key="ny_oms_nasta_ar")
    antal_aktier_nytt = st.number_input("Antal utestående aktier", format="%.0f", key="ny_antal_aktier")
    ps1_nytt = st.number_input("P/S 1", format="%.2f", key="ny_ps1")
    ps2_nytt = st.number_input("P/S 2", format="%.2f", key="ny_ps2")
    ps3_nytt = st.number_input("P/S 3", format="%.2f", key="ny_ps3")
    ps4_nytt = st.number_input("P/S 4", format="%.2f", key="ny_ps4")
    ps5_nytt = st.number_input("P/S 5", format="%.2f", key="ny_ps5")

    skickat = st.form_submit_button("Lägg till bolag")
    if skickat:
        if bolagsnamn_nytt.strip() == "":
            st.error("Fyll i bolagsnamn!")
        else:
            insert_bolag(bolagsnamn_nytt, nuvarande_kurs_nytt, oms_i_ar_nytt, oms_nasta_ar_nytt,
                         antal_aktier_nytt, ps1_nytt, ps2_nytt, ps3_nytt, ps4_nytt, ps5_nytt)
            st.success(f"Bolag '{bolagsnamn_nytt}' tillagt!")
            # Töm formuläret
            for key in ["ny_bolag", "ny_nuv_kurs", "ny_oms_i_ar", "ny_oms_nasta_ar", "ny_antal_aktier",
                        "ny_ps1", "ny_ps2", "ny_ps3", "ny_ps4", "ny_ps5"]:
                st.session_state[key] = "" if "bolag" in key else 0
            st.session_state.index = len(sorterad_bolag)  # Visa senast tillagda
