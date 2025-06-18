import streamlit as st
from database import init_db, lagg_till_bolag, hamta_alla_bolag, uppdatera_bolag, ta_bort_bolag
import statistics

st.set_page_config(page_title="Aktieanalys", layout="centered")
init_db()

st.title("📈 Aktieanalys med P/S-tal")
st.markdown("Analysera om ett bolag är över- eller undervärderat baserat på omsättning och P/S-tal.")

# Nytt bolag – formulär
with st.expander("➕ Lägg till nytt bolag"):
    with st.form("nytt_bolag_formulär"):
        bolag = st.text_input("Bolag")
        nuvarande_kurs = st.number_input("Nuvarande kurs", format="%.2f")
        omsättning_år = st.number_input("Förväntad omsättning i år (MSEK)", format="%.0f")
        omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år (MSEK)", format="%.0f")
        antal_aktier = st.number_input("Antal utestående aktier (miljoner)", format="%.2f")
        ps1 = st.number_input("P/S 1", format="%.2f")
        ps2 = st.number_input("P/S 2", format="%.2f")
        ps3 = st.number_input("P/S 3", format="%.2f")
        ps4 = st.number_input("P/S 4", format="%.2f")
        ps5 = st.number_input("P/S 5", format="%.2f")
        submitted = st.form_submit_button("Spara bolag")

        if submitted and bolag:
            lagg_till_bolag(bolag, nuvarande_kurs, omsättning_år, omsättning_nästa_år,
                            antal_aktier, ps1, ps2, ps3, ps4, ps5)
            st.success(f"{bolag} har lagts till!")

# Hämta alla bolag
bolag_lista = hamta_alla_bolag()

# Sortera efter högst % undervärdering framtida
def beräkna_data(bolag):
    medel_ps = statistics.mean(bolag[6:11])
    potentiell_kurs_idag = (bolag[3] / bolag[5]) * medel_ps
    potentiell_kurs_framtid = (bolag[4] / bolag[5]) * medel_ps
    undervärdering_idag = ((potentiell_kurs_idag - bolag[2]) / bolag[2]) * 100
    undervärdering_framtid = ((potentiell_kurs_framtid - bolag[2]) / bolag[2]) * 100
    return potentiell_kurs_idag, potentiell_kurs_framtid, undervärdering_idag, undervärdering_framtid

bolag_lista.sort(key=lambda x: beräkna_data(x)[3], reverse=True)

if "index" not in st.session_state:
    st.session_state.index = 0

index = st.session_state.index
antal = len(bolag_lista)

if antal > 0:
    bolag = bolag_lista[index]
    potentiell_idag, potentiell_framtid, diff_idag, diff_framtid = beräkna_data(bolag)

    st.subheader(f"{bolag[1]} ({index + 1}/{antal})")

    with st.form(f"uppdatera_{bolag[0]}"):
        ny_kurs = st.number_input("Nuvarande kurs", value=float(bolag[2]), format="%.2f", key=f"kurs_{bolag[0]}")
        ny_oms_år = st.number_input("Förväntad omsättning i år", value=float(bolag[3]), format="%.0f", key=f"omsår_{bolag[0]}")
        ny_oms_nästa = st.number_input("Förväntad omsättning nästa år", value=float(bolag[4]), format="%.0f", key=f"omsnext_{bolag[0]}")
        ny_aktier = st.number_input("Antal aktier", value=float(bolag[5]), format="%.2f", key=f"aktier_{bolag[0]}")
        ny_ps = [st.number_input(f"P/S {i+1}", value=float(bolag[6+i]), format="%.2f", key=f"ps{i}_{bolag[0]}")
                 for i in range(5)]

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Uppdatera"):
                uppdatera_bolag(bolag[0], ny_kurs, ny_oms_år, ny_oms_nästa, ny_aktier, *ny_ps)
                st.success("Bolaget har uppdaterats.")
        with col2:
            if st.form_submit_button("🗑️ Ta bort"):
                ta_bort_bolag(bolag[0])
                st.success("Bolaget har tagits bort.")
                if st.session_state.index > 0:
                    st.session_state.index -= 1

    st.markdown(f"""
    **Potentiell kurs idag:** {potentiell_idag:.2f} kr  
    **Över-/Undervärdering idag:** {diff_idag:.1f} %

    **Potentiell kurs framtid:** {potentiell_framtid:.2f} kr  
    **Över-/Undervärdering framtid:** {diff_framtid:.1f} %
    """)

    bläddra = st.columns([1, 6, 1])
    with bläddra[0]:
        if st.button("⬅️ Föregående") and index > 0:
            st.session_state.index -= 1
    with bläddra[2]:
        if st.button("Nästa ➡️") and index < antal - 1:
            st.session_state.index += 1
else:
    st.info("Inga bolag har lagts till ännu.")
