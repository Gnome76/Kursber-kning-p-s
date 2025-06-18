import streamlit as st
from database import (
    init_db,
    lägg_till_bolag,
    hämta_bolag,
    uppdatera_bolag,
    ta_bort_bolag
)

st.set_page_config(page_title="Aktieanalys", layout="centered")

# Initiera databas
init_db()

# Initiera omritningsflagga
if st.session_state.get("omritning"):
    st.session_state["omritning"] = False
    st.experimental_rerun()

st.title("📊 Enkel Aktieanalys")

# Formulär för att lägga till nytt bolag
st.header("Lägg till bolag")
with st.form("lägg_till_formulär", clear_on_submit=True):
    namn = st.text_input("Bolag")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, step=1.0, format="%.2f")
    omsättning_i_år = st.number_input("Förväntad omsättning i år (MSEK)", min_value=0.0, step=1.0, format="%.2f")
    omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år (MSEK)", min_value=0.0, step=1.0, format="%.2f")
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", min_value=0.0001, step=0.1, format="%.4f")
    ps_tal = [st.number_input(f"P/S {i+1}", min_value=0.0, step=0.1, format="%.2f") for i in range(5)]

    submit = st.form_submit_button("Lägg till bolag")
    if submit and namn:
        lägg_till_bolag(namn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, *ps_tal)
        st.session_state["omritning"] = True

# Visa bolag en och en
st.header("📈 Analys av bolag")

bolag_lista = hämta_bolag()

def beräkna_potentiell_kurs(omsättning, aktier, ps_värden):
    return (omsättning / aktier) * (sum(ps_värden) / len(ps_värden))

# Sortera efter mest undervärderad potentiell kurs nästa år
bolag_lista.sort(key=lambda b: (
    beräkna_potentiell_kurs(b["omsättning_nästa_år"], b["antal_aktier"], [b[f"ps_{i+1}"] for i in range(5)])
    - b["nuvarande_kurs"]
) / b["nuvarande_kurs"], reverse=True)

if bolag_lista:
    index = st.number_input("Bläddra mellan bolag", min_value=0, max_value=len(bolag_lista) - 1, step=1, format="%d")
    bolag = bolag_lista[index]

    st.subheader(f"🔍 {bolag['namn']}")
    nuvarande_kurs = st.number_input("Nuvarande kurs", value=bolag["nuvarande_kurs"], key=f"kurs_{bolag['id']}")
    omsättning_i_år = st.number_input("Omsättning i år", value=bolag["omsättning_i_år"], key=f"oiår_{bolag['id']}")
    omsättning_nästa_år = st.number_input("Omsättning nästa år", value=bolag["omsättning_nästa_år"], key=f"onästa_{bolag['id']}")
    antal_aktier = st.number_input("Antal aktier (miljoner)", value=bolag["antal_aktier"], key=f"aktier_{bolag['id']}")
    ps_värden = [st.number_input(f"P/S {i+1}", value=bolag[f"ps_{i+1}"], key=f"ps_{i+1}_{bolag['id']}") for i in range(5)]

    if st.button("Spara ändringar"):
        uppdatera_bolag(bolag["id"], nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, *ps_värden)
        st.session_state["omritning"] = True

    if st.button("❌ Ta bort bolag"):
        ta_bort_bolag(bolag["id"])
        st.session_state["omritning"] = True

    # Beräkningar
    potentiell_idag = beräkna_potentiell_kurs(omsättning_i_år, antal_aktier, ps_värden)
    potentiell_slutår = beräkna_potentiell_kurs(omsättning_nästa_år, antal_aktier, ps_värden)

    diff_idag = ((potentiell_idag - nuvarande_kurs) / nuvarande_kurs) * 100
    diff_slutår = ((potentiell_slutår - nuvarande_kurs) / nuvarande_kurs) * 100

    st.markdown("### 📌 Potentiella kurser")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Potentiell kurs idag", f"{potentiell_idag:.2f} kr", f"{diff_idag:.1f} %")
    with col2:
        st.metric("Potentiell kurs slutet av året", f"{potentiell_slutår:.2f} kr", f"{diff_slutår:.1f} %")
else:
    st.info("Inga bolag tillagda än.")
