import streamlit as st
from database import init_db, insert_company, get_all_companies, update_company, delete_company

st.set_page_config(page_title="Aktieanalysapp", layout="centered")

# Initiera alla session_state-nycklar som används i formulären
nycklar = [
    "ny_bolag", "ny_nuv_kurs", "ny_oms_i_ar", "ny_oms_nasta_ar",
    "ny_antal_aktier", "ny_ps1", "ny_ps2", "ny_ps3", "ny_ps4", "ny_ps5"
]

for nyckel in nycklar:
    if nyckel not in st.session_state:
        st.session_state[nyckel] = "" if "bolag" in nyckel else 0

# Initiera databasen (skapar tabell om den inte finns)
init_db()

def berakna_potentiell_kurs(omsattning, antal_aktier, ps_tal_lista):
    ps_genomsnitt = sum(ps_tal_lista) / len(ps_tal_lista)
    return (omsattning / antal_aktier) * ps_genomsnitt if antal_aktier > 0 else 0

st.title("Aktieanalysapp")

# Hämta alla bolag från databasen
bolag_lista = get_all_companies()

# Sortera bolag efter mest undervärderad (störst potentiell kurs i slutet av året jämfört med nuvarande kurs)
bolag_lista.sort(
    key=lambda c: (
        berakna_potentiell_kurs(
            c[4], c[5], [c[6], c[7], c[8], c[9], c[10]]
        ) - c[2]
    ) / c[2] if c[2] > 0 else -float('inf'),
    reverse=True
)

# För bläddring - index i session_state
if "index" not in st.session_state:
    st.session_state.index = 0

def visa_bolag(index):
    if not bolag_lista:
        st.info("Inga bolag registrerade än.")
        return

    c = bolag_lista[index]
    ps_lista = [c[6], c[7], c[8], c[9], c[10]]
    nuvarande_kurs = c[2]

    pot_kurs_idag = berakna_potentiell_kurs(c[3], c[5], ps_lista)
    pot_kurs_arskiftet = berakna_potentiell_kurs(c[4], c[5], ps_lista)
    undervardering = ((pot_kurs_arskiftet - nuvarande_kurs) / nuvarande_kurs) * 100 if nuvarande_kurs > 0 else 0

    st.header(f"Bolag: {c[1]}")

    st.write(f"- Nuvarande kurs: {nuvarande_kurs:.2f} SEK")
    st.write(f"- Förväntad omsättning i år: {c[3]:,.0f} SEK")
    st.write(f"- Förväntad omsättning nästa år: {c[4]:,.0f} SEK")
    st.write(f"- Antal utestående aktier: {c[5]:,.0f}")
    st.write(f"- P/S-tal 1–5: {ps_lista}")
    st.markdown("---")

    st.markdown(f"### Potentiell kurs idag: {pot_kurs_idag:.2f} SEK")
    st.markdown(f"### Potentiell kurs i slutet av året: {pot_kurs_arskiftet:.2f} SEK")

    if undervardering > 0:
        st.success(f"Undervärderad med {undervardering:.2f} %")
    else:
        st.warning(f"Övervärderad med {abs(undervardering):.2f} %")

    # Redigera och ta bort knappar
    if st.button("Redigera detta bolag"):
        st.session_state["redigera_index"] = index

    if st.button("Ta bort detta bolag"):
        delete_company(c[0])
        st.experimental_rerun()

st.write("### Bläddra bland bolagen")
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("⬅️ Föregående") and st.session_state.index > 0:
        st.session_state.index -= 1

with col3:
    if st.button("Nästa ➡️") and st.session_state.index < len(bolag_lista) - 1:
        st.session_state.index += 1

visa_bolag(st.session_state.index)

def nollstall_formular():
    for key in nycklar:
        st.session_state[key] = "" if "bolag" in key else 0

if "redigera_index" in st.session_state:
    idx = st.session_state.redigera_index
    c = bolag_lista[idx]

    st.header(f"Redigera bolag: {c[1]}")

    st.session_state["ny_bolag"] = c[1]
    st.session_state["ny_nuv_kurs"] = c[2]
    st.session_state["ny_oms_i_ar"] = c[3]
    st.session_state["ny_oms_nasta_ar"] = c[4]
    st.session_state["ny_antal_aktier"] = c[5]
    st.session_state["ny_ps1"] = c[6]
    st.session_state["ny_ps2"] = c[7]
    st.session_state["ny_ps3"] = c[8]
    st.session_state["ny_ps4"] = c[9]
    st.session_state["ny_ps5"] = c[10]

    with st.form("redigera_form"):
        ny_bolag = st.text_input("Bolag", value=st.session_state["ny_bolag"], key="ny_bolag")
        ny_nuv_kurs = st.number_input("Nuvarande kurs", value=st.session_state["ny_nuv_kurs"], format="%.2f", key="ny_nuv_kurs")
        ny_oms_i_ar = st.number_input("Förväntad omsättning i år", value=st.session_state["ny_oms_i_ar"], format="%.0f", key="ny_oms_i_ar")
        ny_oms_nasta_ar = st.number_input("Förväntad omsättning nästa år", value=st.session_state["ny_oms_nasta_ar"], format="%.0f", key="ny_oms_nasta_ar")
        ny_antal_aktier = st.number_input("Antal utestående aktier", value=st.session_state["ny_antal_aktier"], format="%.0f", key="ny_antal_aktier")
        ny_ps1 = st.number_input("P/S 1", value=st.session_state["ny_ps1"], format="%.2f", key="ny_ps1")
        ny_ps2 = st.number_input("P/S 2", value=st.session_state["ny_ps2"], format="%.2f", key="ny_ps2")
        ny_ps3 = st.number_input("P/S 3", value=st.session_state["ny_ps3"], format="%.2f", key="ny_ps3")
        ny_ps4 = st.number_input("P/S 4", value=st.session_state["ny_ps4"], format="%.2f", key="ny_ps4")
        ny_ps5 = st.number_input("P/S 5", value=st.session_state["ny_ps5"], format="%.2f", key="ny_ps5")

        if st.form_submit_button("Spara ändringar"):
            update_company(
                c[0], ny_bolag, ny_nuv_kurs, ny_oms_i_ar, ny_oms_nasta_ar,
                ny_antal_aktier, ny_ps1, ny_ps2, ny_ps3, ny_ps4, ny_ps5
            )
            st.success("Bolaget har uppdaterats.")
            del st.session_state["redigera_index"]
            nollstall_formular()
            st.experimental_rerun()

    if st.button("Avbryt redigering"):
        del st.session_state["redigera_index"]
        nollstall_formular()
        st.experimental_rerun()

else:
    st.header("Lägg till nytt bolag")

    with st.form("nytt_bolag_form"):
        ny_bolag = st.text_input("Bolag", key="ny_bolag")
        ny_nuv_kurs = st.number_input("Nuvarande kurs", format="%.2f", key="ny_nuv_kurs")
        ny_oms_i_ar = st.number_input("Förväntad omsättning i år", format="%.0f", key="ny_oms_i_ar")
        ny_oms_nasta_ar = st.number_input("Förväntad omsättning nästa år", format="%.0f", key="ny_oms_nasta_ar")
        ny_antal_aktier = st.number_input("Antal utestående aktier", format="%.0f", key="ny_antal_aktier")
        ny_ps1 = st.number_input("P/S 1", format="%.2f", key="ny_ps1")
        ny_ps2 = st.number_input("P/S 2", format="%.2f", key="ny_ps2")
        ny_ps3 = st.number_input("P/S 3", format="%.2f", key="ny_ps3")
        ny_ps4 = st.number_input("P/S 4", format="%.2f", key="ny_ps4")
        ny_ps5 = st.number_input("P/S 5", format="%.2f", key="ny_ps5")

        if st.form_submit_button("Lägg till bolag"):
            insert_company(
                ny_bolag, ny_nuv_kurs, ny_oms_i_ar, ny_oms_nasta_ar,
                ny_antal_aktier, ny_ps1, ny_ps2, ny_ps3, ny_ps4, ny_ps5
            )
            st.success("Bolaget har lagts till.")
            nollstall_formular()
            st.experimental_rerun()
