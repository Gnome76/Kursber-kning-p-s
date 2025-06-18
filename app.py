import streamlit as st
from database import initiera_databas, lägg_till_bolag, hämta_alla_bolag, uppdatera_bolag, ta_bort_bolag

# Initiera databasen direkt vid start
initiera_databas()

st.set_page_config(page_title="Aktieanalysapp", page_icon="📈", layout="centered")
st.title("Aktieanalysapp")

# Funktion för att beräkna potentiell kurs
def beräkna_pot_kurs(omsättning, aktier, ps):
    if aktier > 0:
        return (omsättning / aktier) * ps
    else:
        return 0

# --- Lägg till nytt bolag ---
with st.form("nytt_bolag_formulär"):
    st.header("Lägg till nytt bolag")

    bolagsnamn = st.text_input("Bolagsnamn")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    omsättning_i_år = st.number_input("Förväntad omsättning i år (MSEK)", min_value=0.0, format="%.2f")
    omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år (MSEK)", min_value=0.0, format="%.2f")
    antal_aktier = st.number_input("Antal utestående aktier", min_value=1, step=1)
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
    ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f")

    skicka = st.form_submit_button("Lägg till bolag")

    if skicka:
        if bolagsnamn.strip() == "":
            st.error("Vänligen ange ett bolagsnamn.")
        else:
            lägg_till_bolag(bolagsnamn.strip(), nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5)
            st.success(f"Bolaget '{bolagsnamn}' har lagts till.")
            # Triggera uppdatering genom session_state
            st.session_state["uppdatera"] = st.session_state.get("uppdatera", 0) + 1

st.markdown("---")

# --- Visa och hantera registrerade bolag ---
bolag = hämta_alla_bolag()

if "uppdatera" not in st.session_state:
    st.session_state["uppdatera"] = 0

st.header("📊 Registrerade bolag")

if bolag:
    tabell_data = []
    for rad in bolag:
        id, namn, kurs, oms_år, oms_nästa, aktier, ps1, ps2, ps3, ps4, ps5 = rad
        ps_medel = (ps1 + ps2 + ps3 + ps4 + ps5) / 5
        kurs_idag = beräkna_pot_kurs(oms_år, aktier, ps_medel)
        kurs_slutåret = beräkna_pot_kurs(oms_nästa, aktier, ps_medel)
        undervärdering = ((kurs_slutåret - kurs) / kurs) * 100 if kurs > 0 else 0

        tabell_data.append({
            "ID": id,
            "Bolag": namn,
            "Nuvarande kurs": kurs,
            "Potentiell kurs idag": round(kurs_idag, 2),
            "Potentiell kurs slut året": round(kurs_slutåret, 2),
            "Undervärdering (%)": round(undervärdering, 2),
        })

    # Sortera efter mest undervärderad
    tabell_data.sort(key=lambda x: x["Undervärdering (%)"], reverse=True)

    st.dataframe(tabell_data, use_container_width=True)

    st.subheader("✏️ Redigera eller ta bort bolag")

    valt_bolag = st.selectbox("Välj bolag att redigera eller ta bort", bolag, format_func=lambda x: x[1])

    if valt_bolag:
        with st.form("redigera_formulär"):
            ny_kurs = st.number_input("Ny kurs", value=valt_bolag[2])
            ny_oms_år = st.number_input("Ny omsättning i år", value=valt_bolag[3])
            ny_oms_nästa = st.number_input("Ny omsättning nästa år", value=valt_bolag[4])
            ny_aktier = st.number_input("Nytt antal aktier", value=valt_bolag[5])
            ny_ps = [st.number_input(f"P/S {i+1}", value=valt_bolag[6+i]) for i in range(5)]

            uppdatera = st.form_submit_button("Uppdatera")
            ta_bort = st.form_submit_button("Ta bort")

            if uppdatera:
                uppdatera_bolag(valt_bolag[0], ny_kurs, ny_oms_år, ny_oms_nästa, ny_aktier, *ny_ps)
                st.success("Bolaget har uppdaterats.")
                st.session_state["uppdatera"] += 1

            if ta_bort:
                ta_bort_bolag(valt_bolag[0])
                st.warning("Bolaget har tagits bort.")
                st.session_state["uppdatera"] += 1

else:
    st.info("Inga bolag är registrerade ännu.")
