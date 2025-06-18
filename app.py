import streamlit as st
from database import initiera_databas, lägg_till_bolag, hämta_alla_bolag, uppdatera_bolag, ta_bort_bolag

# Initiera databas vid appstart
initiera_databas()

# Session state för att trigga uppdatering av bolagslistan
if "uppdatera" not in st.session_state:
    st.session_state["uppdatera"] = 0

st.title("📊 Aktieanalysapp")

# Funktion för att beräkna potentiell kurs
def beräkna_pot_kurs(omsättning, aktier, ps):
    return (omsättning / aktier) * ps if aktier > 0 else 0

# -------------------- Lägg till nytt bolag --------------------
st.header("➕ Lägg till nytt bolag")

with st.form("lägg_till_formulär"):
    nytt_bolag = st.text_input("Bolagsnamn")
    kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    oms_år = st.number_input("Omsättning i år", min_value=0.0, format="%.2f")
    oms_nästa = st.number_input("Omsättning nästa år", min_value=0.0, format="%.2f")
    aktier = st.number_input("Antal utestående aktier", min_value=1, step=1)
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", value=1.0)
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", value=1.0)
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f", value=1.0)
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f", value=1.0)
    ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f", value=1.0)

    lägg_till_knapp = st.form_submit_button("Lägg till bolag")

    if lägg_till_knapp:
        if nytt_bolag.strip() == "":
            st.error("Ange ett giltigt bolagsnamn.")
        else:
            lägg_till_bolag(
                nytt_bolag.strip(),
                kurs,
                oms_år,
                oms_nästa,
                aktier,
                ps1,
                ps2,
                ps3,
                ps4,
                ps5
            )
            st.success(f"Bolaget '{nytt_bolag}' har lagts till.")
            st.session_state["uppdatera"] += 1

# -------------------- Hämta och visa bolag --------------------
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

    # Sortera efter mest undervärderad (högst undervärdering först)
    tabell_data.sort(key=lambda x: x["Undervärdering (%)"], reverse=True)

    st.dataframe(tabell_data, use_container_width=True)
else:
    st.info("Inga bolag är registrerade ännu.")

# -------------------- Redigera eller ta bort bolag --------------------
if bolag:
    st.subheader("✏️ Redigera eller ta bort bolag")

    valt_bolag = st.selectbox("Välj bolag att redigera/ta bort", bolag, format_func=lambda x: x[1])

    if valt_bolag:
        with st.form("redigera_formulär"):
            ny_kurs = st.number_input("Ny kurs", value=valt_bolag[2], format="%.2f")
            ny_oms_år = st.number_input("Ny omsättning i år", value=valt_bolag[3], format="%.2f")
            ny_oms_nästa = st.number_input("Ny omsättning nästa år", value=valt_bolag[4], format="%.2f")
            ny_aktier = st.number_input("Nytt antal aktier", value=valt_bolag[5], step=1)
            ny_ps = [st.number_input(f"P/S {i+1}", value=valt_bolag[6 + i], format="%.2f") for i in range(5)]

            uppdatera_knapp = st.form_submit_button("Uppdatera")
            ta_bort_knapp = st.form_submit_button("Ta bort")

            if uppdatera_knapp:
                uppdatera_bolag(
                    valt_bolag[0],
                    ny_kurs,
                    ny_oms_år,
                    ny_oms_nästa,
                    ny_aktier,
                    *ny_ps
                )
                st.success("Bolaget har uppdaterats.")
                st.session_state["uppdatera"] += 1

            if ta_bort_knapp:
                ta_bort_bolag(valt_bolag[0])
                st.warning("Bolaget har tagits bort.")
                st.session_state["uppdatera"] += 1

    # Hämta bolag igen efter eventuell ändring
    bolag = hämta_alla_bolag()
