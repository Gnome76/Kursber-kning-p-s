import streamlit as st
from database import (
    initiera_databas,
    lägg_till_bolag,
    hämta_alla_bolag,
    uppdatera_bolag,
    ta_bort_bolag,
)

st.set_page_config(page_title="Aktieanalys", page_icon="📈")
initiera_databas()

st.title("Aktieanalysapp")

def beräkna_potentiell_kurs(omsättning, antal_aktier, ps_list):
    ps_medel = sum(ps_list) / len(ps_list)
    return (omsättning / antal_aktier) * ps_medel

# Initiera session_state-variabel för att trigga uppdatering
if "uppdatera" not in st.session_state:
    st.session_state.uppdatera = False

# Funktion för att trigga "uppdatering"
def trigga_uppdatering():
    st.session_state.uppdatera = not st.session_state.uppdatera

# Formulär för nytt bolag
with st.form("nytt_bolag"):
    st.header("Lägg till nytt bolag")

    bolagsnamn = st.text_input("Bolag")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    omsättning_i_år = st.number_input("Omsättning i år (MSEK)", min_value=0.0, format="%.2f")
    omsättning_nästa_år = st.number_input("Omsättning nästa år (MSEK)", min_value=0.0, format="%.2f")
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", min_value=1, step=1)
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
    ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f")

    skicka = st.form_submit_button("Lägg till bolag")

    if skicka:
        lägg_till_bolag(
            bolagsnamn,
            nuvarande_kurs,
            omsättning_i_år,
            omsättning_nästa_år,
            antal_aktier,
            ps1, ps2, ps3, ps4, ps5,
        )
        st.success(f"Bolag '{bolagsnamn}' har lagts till!")
        trigga_uppdatering()

st.header("Alla bolag")

# Ladda bolag på nytt när 'uppdatera' ändras
bolag_lista = hämta_alla_bolag()

if not bolag_lista:
    st.info("Inga bolag inlagda ännu.")
else:
    for b in bolag_lista:
        (
            id, bolagsnamn, nuvarande_kurs,
            omsättning_i_år, omsättning_nästa_år,
            antal_aktier, ps1, ps2, ps3, ps4, ps5
        ) = b

        ps_lista = [ps1, ps2, ps3, ps4, ps5]

        pot_kurs_idag = beräkna_potentiell_kurs(omsättning_i_år, antal_aktier, ps_lista)
        pot_kurs_nasta_år = beräkna_potentiell_kurs(omsättning_nästa_år, antal_aktier, ps_lista)
        undervärdering_proc = ((pot_kurs_nasta_år - nuvarande_kurs) / nuvarande_kurs) * 100 if nuvarande_kurs else 0

        with st.expander(f"{bolagsnamn} (Nuvarande kurs: {nuvarande_kurs:.2f} SEK)"):
            st.write(f"**Omsättning i år:** {omsättning_i_år:.2f} MSEK")
            st.write(f"**Omsättning nästa år:** {omsättning_nästa_år:.2f} MSEK")
            st.write(f"**Antal aktier:** {antal_aktier} miljoner")
            st.write(f"**P/S-tal:** {ps_lista}")
            st.write(f"**Potentiell kurs idag:** {pot_kurs_idag:.2f} SEK")
            st.write(f"**Potentiell kurs slutet av året:** {pot_kurs_nasta_år:.2f} SEK")
            st.write(f"**Undervärdering:** {undervärdering_proc:.2f} %")

            if st.button(f"Ta bort {bolagsnamn}", key=f"ta_bort_{id}"):
                ta_bort_bolag(id)
                st.success(f"Bolag '{bolagsnamn}' borttaget.")
                trigga_uppdatering()

            # Redigeringsknappen kan du lägga till här med liknande session_state-logik
