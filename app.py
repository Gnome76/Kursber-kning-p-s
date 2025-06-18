import streamlit as st
import os
from database import init_db, insert_bolag, get_alla_bolag, uppdatera_bolag, ta_bort_bolag

# Initiera databas och säkerställ att databasfilen skapas
init_db()

st.set_page_config(page_title="Aktieanalysapp", layout="centered")
st.title("📊 Enkel Aktieanalysapp")

# Hjälpfunktioner för beräkningar
def medel_ps(ps1, ps2, ps3, ps4, ps5):
    return (ps1 + ps2 + ps3 + ps4 + ps5) / 5

def potentiell_kurs(oms, antal, ps_med):
    return (oms / antal) * ps_med if antal else 0

def procentuell_avvikelse(nuv, potentiell):
    return (potentiell / nuv - 1) * 100 if nuv else 0

# ➕ Lägg till nytt bolag
with st.expander("Lägg till nytt bolag"):
    with st.form("nytt_bolag"):
        namn = st.text_input("Bolagsnamn")
        nuv = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        oms_i_ar = st.number_input("Omsättning i år", min_value=0.0, format="%.2f")
        oms_n_ar = st.number_input("Omsättning nästa år", min_value=0.0, format="%.2f")
        antal = st.number_input("Antal aktier", min_value=1, format="%d")
        ps_vals = [st.number_input(f"P/S {i+1}", min_value=0.0, format="%.2f", key=f"ps{i}") for i in range(5)]
        submit_new = st.form_submit_button("Lägg till bolag")
        if submit_new:
            if not namn.strip():
                st.error("Ange ett bolagsnamn.")
            else:
                insert_bolag(namn.strip(), nuv, oms_i_ar, oms_n_ar, antal, *ps_vals)
                st.success(f"Bolaget '{namn}' tillagt!")
                st.experimental_rerun()

# 📄 Visa/redigera existerande bolag
alla = get_alla_bolag()

if alla:
    # Sortering efter framtida undervärdering
    def key_fn(b):
        _, _, nuv, oms_i, oms_n, antal, *psv = b
        ps_med = medel_ps(*psv)
        pot = potentiell_kurs(oms_n, antal, ps_med)
        return pot / nuv if nuv else 0
    alla.sort(key=key_fn, reverse=True)

    idx = st.number_input("Välj bolag", min_value=1, max_value=len(alla), value=1, step=1) - 1
    rec = alla[idx]
    id_, namn, nuv, oms_i, oms_n, antal, *psv = rec

    st.subheader(f"Bolag: {namn}")
    with st.form("redigera"):
        nuv_n = st.number_input("Nuvarande kurs", value=nuv, format="%.2f", key=f"nuv_{id_}")
        oms_i_n = st.number_input("Omsättning i år", value=oms_i, format="%.2f", key=f"oms_i_{id_}")
        oms_n_n = st.number_input("Omsättning nästa år", value=oms_n, format="%.2f", key=f"oms_n_{id_}")
        antal_n = st.number_input("Antal aktier", value=antal, format="%d", key=f"antal_{id_}")
        ps_n = [st.number_input(f"P/S {i+1}", value=psv[i], format="%.2f", key=f"ps_n_{id_}_{i}") for i in range(5)]
        save = st.form_submit_button("Spara ändringar")
        delete = st.form_submit_button("Ta bort bolag")
        if save:
            uppdatera_bolag(id_, namn, nuv_n, oms_i_n, oms_n_n, antal_n, *ps_n)
            st.success("Ändringar sparade!")
            st.experimental_rerun()
        if delete:
            ta_bort_bolag(id_)
            st.success(f"'{namn}' tagits bort.")
            st.experimental_rerun()

    ps_med = medel_ps(*ps_n)
    pot_i = potentiell_kurs(oms_i_n, antal_n, ps_med)
    pot_n = potentiell_kurs(oms_n_n, antal_n, ps_med)
    av_i = procentuell_avvikelse(nuv_n, pot_i)
    av_n = procentuell_avvikelse(nuv_n, pot_n)

    st.markdown(f"**Potentiell kurs idag:** {pot_i:.2f} SEK ({av_i:+.1f} %)")
    st.markdown(f"**Potentiell kurs slutet av året:** {pot_n:.2f} SEK ({av_n:+.1f} %)")
else:
    st.info("Inga bolag tillagda.")

# ⚙️ Debug-knappar
if st.button("Visa antal bolag"):
    st.write(f"Antal bolag i databas: {len(alla)}")
if st.button("Visa databasinfo"):
    path = os.path.join("data", "database.db")
    if os.path.exists(path):
        st.write(f"Databas: {path}, {os.path.getsize(path)} bytes")
    else:
        st.write("Ingen databas hittad.")
