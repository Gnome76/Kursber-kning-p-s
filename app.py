import streamlit as st
from database import init_db, hamta_alla_bolag, lagg_till_bolag, uppdatera_bolag, ta_bort_bolag

init_db()

def berakna_potentiell_kurs(omsattning, antal_aktier, ps_varden):
    genomsnitt_ps = sum(ps_varden) / len(ps_varden)
    return (omsattning / antal_aktier) * genomsnitt_ps

st.title("Enkel Aktieanalysapp")

# --- Lägg till nytt bolag ---
with st.expander("Lägg till nytt bolag"):
    namn = st.text_input("Bolag")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    omsattning_ars = st.number_input("Förväntad omsättning i år (MSEK)", min_value=0.0, format="%.2f")
    omsattning_nasta_ar = st.number_input("Förväntad omsättning nästa år (MSEK)", min_value=0.0, format="%.2f")
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", min_value=1, step=1)
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
    ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f")
    if st.button("Lägg till bolag"):
        if namn.strip() == "":
            st.error("Ange ett bolagsnamn.")
        else:
            try:
                lagg_till_bolag(namn.strip(), nuvarande_kurs, omsattning_ars, omsattning_nasta_ar,
                                antal_aktier, ps1, ps2, ps3, ps4, ps5)
                st.success(f"Bolaget {namn} tillagt!")
            except Exception as e:
                st.error(f"Fel vid tillägg: {e}")

# --- Läs in bolag från DB ---
alla_bolag = hamta_alla_bolag()

# --- Sortera på mest undervärderad (baserat på potentiell kurs i slutet av året jämfört med nuvarande kurs) ---
def sortera_bolag(bolag_lista):
    sorterad = []
    for bolag in bolag_lista:
        (
            id_, namn_, nuv_kurs, oms_ars, oms_nast_ars, antal_aktier,
            ps1_, ps2_, ps3_, ps4_, ps5_
        ) = bolag
        ps_varden = [ps1_, ps2_, ps3_, ps4_, ps5_]
        pot_kurs_nu = berakna_potentiell_kurs(oms_ars, antal_aktier, ps_varden)
        pot_kurs_slut = berakna_potentiell_kurs(oms_nast_ars, antal_aktier, ps_varden)
        if nuv_kurs > 0:
            undervardering_pct = ((pot_kurs_slut - nuv_kurs) / nuv_kurs) * 100
        else:
            undervardering_pct = 0
        sorterad.append((undervardering_pct, bolag))
    sorterad.sort(key=lambda x: x[0], reverse=True)  # störst undervärdering först
    return [x[1] for x in sorterad]

sorterade_bolag = sortera_bolag(alla_bolag)

# --- Bläddringsindex ---
if "index" not in st.session_state:
    st.session_state.index = 0

def byt_bolag(ny_index):
    if 0 <= ny_index < len(sorterade_bolag):
        st.session_state.index = ny_index

col1, col2, col3 = st.columns([1,6,1])
with col1:
    if st.button("⬅️ Föregående"):
        byt_bolag(st.session_state.index - 1)
with col3:
    if st.button("Nästa ➡️"):
        byt_bolag(st.session_state.index + 1)

if sorterade_bolag:
    bolag = sorterade_bolag[st.session_state.index]
    (
        id_, namn_, nuv_kurs, oms_ars, oms_nast_ars, antal_aktier,
        ps1_, ps2_, ps3_, ps4_, ps5_
    ) = bolag
    ps_varden = [ps1_, ps2_, ps3_, ps4_, ps5_]

    # Visa info + redigera
    st.subheader(f"Bolag: {namn_}")

    # Editable fält - direkt uppdatering ger ny beräkning
    ny_nuv_kurs = st.number_input("Nuvarande kurs", value=nuv_kurs, format="%.2f", key=f"nuv_kurs_{id_}")
    ny_oms_ars = st.number_input("Förväntad omsättning i år (MSEK)", value=oms_ars, format="%.2f", key=f"oms_ars_{id_}")
    ny_oms_nasta = st.number_input("Förväntad omsättning nästa år (MSEK)", value=oms_nast_ars, format="%.2f", key=f"oms_nasta_{id_}")
    ny_antal_aktier = st.number_input("Antal utestående aktier (miljoner)", value=antal_aktier, step=1, key=f"antal_aktier_{id_}")
    ny_ps1 = st.number_input("P/S 1", value=ps1_, format="%.2f", key=f"ps1_{id_}")
    ny_ps2 = st.number_input("P/S 2", value=ps2_, format="%.2f", key=f"ps2_{id_}")
    ny_ps3 = st.number_input("P/S 3", value=ps3_, format="%.2f", key=f"ps3_{id_}")
    ny_ps4 = st.number_input("P/S 4", value=ps4_, format="%.2f", key=f"ps4_{id_}")
    ny_ps5 = st.number_input("P/S 5", value=ps5_, format="%.2f", key=f"ps5_{id_}")

    # Spara knappar
    if st.button("Spara ändringar", key=f"spara_{id_}"):
        uppdatera_bolag(id_, "nuvarande_kurs", ny_nuv_kurs)
        uppdatera_bolag(id_, "omsattning_ars", ny_oms_ars)
        uppdatera_bolag(id_, "omsattning_nasta_ar", ny_oms_nasta)
        uppdatera_bolag(id_, "antal_aktier", ny_antal_aktier)
        uppdatera_bolag(id_, "ps1", ny_ps1)
        uppdatera_bolag(id_, "ps2", ny_ps2)
        uppdatera_bolag(id_, "ps3", ny_ps3)
        uppdatera_bolag(id_, "ps4", ny_ps4)
        uppdatera_bolag(id_, "ps5", ny_ps5)
        st.success("Ändringar sparade!")
        st.experimental_rerun()

    if st.button("Ta bort bolag", key=f"ta_bort_{id_}"):
        ta_bort_bolag(id_)
        st.success(f"Bolaget {namn_} borttaget!")
        st.experimental_rerun()

    # Beräkningar
    pot_kurs_nu = berakna_potentiell_kurs(ny_oms_ars, ny_antal_aktier, [ny_ps1, ny_ps2, ny_ps3, ny_ps4, ny_ps5])
    pot_kurs_slut = berakna_potentiell_kurs(ny_oms_nasta, ny_antal_aktier, [ny_ps1, ny_ps2, ny_ps3, ny_ps4, ny_ps5])
    
    # Procentuell under/övervärdering
    def berakna_procentuell(nuvarande, potentiell):
        if nuvarande == 0:
            return 0
        return ((potentiell - nuvarande) / nuvarande) * 100

    over_undervard_nu = berakna_procentuell(ny_nuv_kurs, pot_kurs_nu)
    over_undervard_slut = berakna_procentuell(ny_nuv_kurs, pot_kurs_slut)

    st.markdown(f"### Potentiell kurs idag: {pot_kurs_nu:.2f} SEK")
    st.markdown(f"**Under-/övervärdering idag:** {over_undervard_nu:+.2f} %")
    st.markdown(f"### Potentiell kurs i slutet av året: {pot_kurs_slut:.2f} SEK")
    st.markdown(f"**Under-/övervärdering i slutet av året:** {over_undervard_slut:+.2f} %")
else:
    st.info("Inga bolag inlagda ännu.")

# --- Debug: Visa antal bolag i DB ---
if st.button("Visa antal bolag i databasen"):
    bolag = hamta_alla_bolag()
    st.write(f"Antal bolag sparade i databasen: {len(bolag)}")

# --- Debug: Visa databasens storlek ---
import os
if st.button("Visa databasens plats och storlek"):
    db_path = "/mnt/data/database.db"
    if os.path.exists(db_path):
        storlek = os.path.getsize(db_path)
        st.write(f"Databas finns på: {db_path}")
        st.write(f"Databasstorlek: {storlek} bytes")
    else:
        st.write("Databasfilen finns inte.")
