import streamlit as st
from streamlit.runtime.scriptrunner import rerun
from database import init_db, insert_bolag, hamta_alla_bolag, uppdatera_bolag, ta_bort_bolag

init_db()

st.title("Enkel Aktieanalysapp")

# Funktion för att räkna genomsnittet av P/S-värdena
def berakna_ps_medel(ps1, ps2, ps3, ps4, ps5):
    return (ps1 + ps2 + ps3 + ps4 + ps5) / 5

# Funktion för att beräkna potentiell kurs idag
def potentiell_kurs_idag(omsättning_i_år, antal_aktier, ps_medel):
    if antal_aktier == 0:
        return 0
    return (omsättning_i_år / antal_aktier) * ps_medel

# Funktion för att beräkna potentiell kurs i slutet av året
def potentiell_kurs_slutet_året(omsättning_nästa_år, antal_aktier, ps_medel):
    if antal_aktier == 0:
        return 0
    return (omsättning_nästa_år / antal_aktier) * ps_medel

# Funktion för att beräkna % över-/undervärdering
def over_under_värdering(pot_kurs, nuvarande_kurs):
    if nuvarande_kurs == 0:
        return 0
    return (pot_kurs - nuvarande_kurs) / nuvarande_kurs * 100

# Formulär för att lägga till nytt bolag
with st.expander("Lägg till nytt bolag"):
    with st.form("form_lagg_till_bolag"):
        bolag = st.text_input("Bolag")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        omsattning_år = st.number_input("Förväntad omsättning i år", min_value=0.0, format="%.0f")
        omsattning_nasta_år = st.number_input("Förväntad omsättning nästa år", min_value=0.0, format="%.0f")
        antal_aktier = st.number_input("Antal utestående aktier", min_value=1, step=1)
        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
        ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f")

        skickaknapp = st.form_submit_button("Lägg till bolag")

        if skickaknapp:
            if bolag.strip() == "":
                st.error("Vänligen ange ett bolagsnamn.")
            else:
                insert_bolag(bolag.strip(), nuvarande_kurs, omsattning_år, omsattning_nasta_år,
                             antal_aktier, ps1, ps2, ps3, ps4, ps5)
                st.success(f"Bolaget '{bolag}' har lagts till.")
                rerun()

# Hämta alla bolag och sortera på mest undervärderad (störst % undervärdering först)
bolag_lista = hamta_alla_bolag()

for bolag_dict in bolag_lista:
    ps_med = berakna_ps_medel(bolag_dict["ps1"], bolag_dict["ps2"], bolag_dict["ps3"],
                              bolag_dict["ps4"], bolag_dict["ps5"])
    bolag_dict["pot_kurs_idag"] = potentiell_kurs_idag(bolag_dict["omsattning_i_år"], bolag_dict["antal_aktier"], ps_med)
    bolag_dict["pot_kurs_årsslut"] = potentiell_kurs_slutet_året(bolag_dict["omsattning_nasta_år"], bolag_dict["antal_aktier"], ps_med)
    bolag_dict["undervardering_%"] = over_under_värdering(bolag_dict["pot_kurs_årsslut"], bolag_dict["nuvarande_kurs"])

# Sortera på undervärdering (störst undervärdering först)
bolag_lista.sort(key=lambda x: x["undervardering_%"], reverse=True)

# Visar bolagen ett och ett med bläddring
if bolag_lista:
    index = st.session_state.get("index", 0)
    if "index" not in st.session_state:
        st.session_state.index = 0

    bolag_vald = bolag_lista[index]

    st.subheader(f"Bolag: {bolag_vald['bolag']}")

    # Formulär för redigering av valt bolag
    with st.form("form_redigera_bolag"):
        nuv_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f", value=bolag_vald["nuvarande_kurs"])
        oms_år = st.number_input("Förväntad omsättning i år", min_value=0.0, format="%.0f", value=bolag_vald["omsattning_i_år"])
        oms_nasta = st.number_input("Förväntad omsättning nästa år", min_value=0.0, format="%.0f", value=bolag_vald["omsattning_nasta_år"])
        antal = st.number_input("Antal utestående aktier", min_value=1, step=1, value=bolag_vald["antal_aktier"])
        p1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", value=bolag_vald["ps1"])
        p2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", value=bolag_vald["ps2"])
        p3 = st.number_input("P/S 3", min_value=0.0, format="%.2f", value=bolag_vald["ps3"])
        p4 = st.number_input("P/S 4", min_value=0.0, format="%.2f", value=bolag_vald["ps4"])
        p5 = st.number_input("P/S 5", min_value=0.0, format="%.2f", value=bolag_vald["ps5"])

        knapp_update = st.form_submit_button("Uppdatera bolag")

        if knapp_update:
            uppdatera_bolag(bolag_vald["id"], nuv_kurs, oms_år, oms_nasta, antal, p1, p2, p3, p4, p5)
            st.success("Bolag uppdaterat.")
            rerun()

    st.markdown("---")

    # Visa beräkningar snyggt
    ps_med = berakna_ps_medel(bolag_vald["ps1"], bolag_vald["ps2"], bolag_vald["ps3"], bolag_vald["ps4"], bolag_vald["ps5"])
    pot_kurs_idag = potentiell_kurs_idag(bolag_vald["omsattning_i_år"], bolag_vald["antal_aktier"], ps_med)
    pot_kurs_slut = potentiell_kurs_slutet_året(bolag_vald["omsattning_nasta_år"], bolag_vald["antal_aktier"], ps_med)
    undervärdering_idag = over_under_värdering(pot_kurs_idag, bolag_vald["nuvarande_kurs"])
    undervärdering_slut = over_under_värdering(pot_kurs_slut, bolag_vald["nuvarande_kurs"])

    st.markdown(f"**Potentiell kurs idag:** {pot_kurs_idag:.2f} SEK ({undervärdering_idag:+.2f} % jämfört med nuvarande kurs)")
    st.markdown(f"**Potentiell kurs i slutet av året:** {pot_kurs_slut:.2f} SEK ({undervärdering_slut:+.2f} % jämfört med nuvarande kurs)")

    # Ta bort bolag
    if st.button("Ta bort detta bolag"):
        ta_bort_bolag(bolag_vald["id"])
        st.success(f"Bolaget '{bolag_vald['bolag']}' är borttaget.")
        # Justera index om det var sista bolaget
        if index >= len(bolag_lista) - 1 and index > 0:
            st.session_state.index = index - 1
        rerun()

    # Bläddringsknappar
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        if st.button("⬅️ Föregående") and index > 0:
            st.session_state.index = index - 1
            rerun()
    with col3:
        if st.button("Nästa ➡️") and index < len(bolag_lista) -1:
            st.session_state.index = index + 1
            rerun()
else:
    st.info("Inga bolag registrerade ännu. Lägg till bolag ovan.")
