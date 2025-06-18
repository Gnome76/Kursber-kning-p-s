import streamlit as st
from database import (
    initiera_databas,
    lägg_till_bolag,
    hämta_alla_bolag,
    uppdatera_bolag,
    ta_bort_bolag,
)

st.set_page_config(page_title="Aktieanalys", layout="wide")
initiera_databas()

st.title("📊 Aktieanalys baserat på P/S-tal")

st.header("➕ Lägg till nytt bolag")
with st.form("lägg_till_form"):
    kol1, kol2 = st.columns(2)

    with kol1:
        bolagsnamn = st.text_input("Bolagsnamn")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, value=100.0)
        omsättning_i_år = st.number_input("Förväntad omsättning i år", min_value=0.0)
        omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år", min_value=0.0)

    with kol2:
        antal_aktier = st.number_input("Antal utestående aktier", min_value=1)
        ps1 = st.number_input("P/S-tal 1", min_value=0.0, value=5.0)
        ps2 = st.number_input("P/S-tal 2", min_value=0.0, value=5.0)
        ps3 = st.number_input("P/S-tal 3", min_value=0.0, value=5.0)
        ps4 = st.number_input("P/S-tal 4", min_value=0.0, value=5.0)
        ps5 = st.number_input("P/S-tal 5", min_value=0.0, value=5.0)

    submitted = st.form_submit_button("Spara bolag")

    if submitted:
        lägg_till_bolag(
            bolagsnamn,
            nuvarande_kurs,
            omsättning_i_år,
            omsättning_nästa_år,
            antal_aktier,
            ps1, ps2, ps3, ps4, ps5
        )
        st.success(f"{bolagsnamn} har sparats.")
        st.session_state["dummy"] = st.session_state.get("dummy", 0) + 1

# Funktion för att beräkna potentiell kurs
def beräkna_pot_kurs(omsättning, aktier, ps):
    return (omsättning / aktier) * ps if aktier > 0 else 0

bolag = hämta_alla_bolag()
st.header("📈 Registrerade bolag")

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

    tabell_data.sort(key=lambda x: x["Undervärdering (%)"], reverse=True)

    st.dataframe(tabell_data, use_container_width=True)

    st.subheader("✏️ Redigera eller ta bort bolag")
    valt_bolag = st.selectbox("Välj bolag att redigera/ta bort", bolag, format_func=lambda x: x[1])

    if valt_bolag:
        with st.form("redigera_form"):
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
                st.session_state["dummy"] = st.session_state.get("dummy", 0) + 1

            if ta_bort:
                ta_bort_bolag(valt_bolag[0])
                st.warning("Bolaget har tagits bort.")
                st.session_state["dummy"] = st.session_state.get("dummy", 0) + 1
else:
    st.info("Inga bolag är registrerade ännu.")
