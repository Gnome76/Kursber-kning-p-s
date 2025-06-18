import streamlit as st
from database import init_db, insert_company, get_all_companies, update_company, delete_company
import os

# Initiera databas
init_db()

st.set_page_config(page_title="Aktieanalys", layout="centered")

st.title("📊 Aktieanalysapp")

# Första inmatningsformuläret
with st.form("add_company_form"):
    st.subheader("Lägg till nytt bolag")
    namn = st.text_input("Bolag")
    nuvarande_kurs = st.number_input("Nuvarande kurs", format="%.2f")
    omsättning_i_år = st.number_input("Förväntad omsättning i år", format="%.0f")
    omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år", format="%.0f")
    antal_aktier = st.number_input("Antal utestående aktier", format="%.0f")
    ps1 = st.number_input("P/S 1", format="%.2f")
    ps2 = st.number_input("P/S 2", format="%.2f")
    ps3 = st.number_input("P/S 3", format="%.2f")
    ps4 = st.number_input("P/S 4", format="%.2f")
    ps5 = st.number_input("P/S 5", format="%.2f")

    submitted = st.form_submit_button("Lägg till bolag")
    if submitted and namn:
        insert_company(namn, nuvarande_kurs, omsättning_i_år, omsättning_nästa_år, antal_aktier, ps1, ps2, ps3, ps4, ps5)
        st.success(f"{namn} har lagts till.")
        st.session_state.data_changed = True

# Läs in data
if "data_changed" not in st.session_state:
    st.session_state.data_changed = True

if st.session_state.data_changed:
    companies = get_all_companies()
    st.session_state.data_changed = False
else:
    companies = get_all_companies()

# Sortera efter mest undervärderad (framtida potentiell kurs)
def beräkna_procent_uppgång(omsättning, aktier, ps, nuvarande_kurs):
    if aktier == 0:
        return 0
    genomsnitt_ps = sum(ps) / 5
    potentiell_kurs = omsättning / aktier * genomsnitt_ps
    return (potentiell_kurs - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs != 0 else 0

companies = sorted(
    companies,
    key=lambda x: beräkna_procent_uppgång(x[3], x[4], x[5:10], x[2]),
    reverse=True
)

st.subheader("📌 Bolag (sorterade efter mest undervärderade)")

if not companies:
    st.info("Inga bolag inlagda ännu.")
else:
    for index, company in enumerate(companies):
        with st.expander(company[1], expanded=True):
            nuvarande_kurs = company[2]
            oms_år = company[3]
            oms_nästa = company[4]
            aktier = company[5]
            ps_tal = company[6:11]

            if aktier == 0:
                continue

            genomsnitt_ps = sum(ps_tal) / 5

            potentiell_kurs_idag = oms_år / aktier * genomsnitt_ps
            potentiell_kurs_slutåret = oms_nästa / aktier * genomsnitt_ps

            övervärdering_idag = (potentiell_kurs_idag - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs else 0
            övervärdering_slutåret = (potentiell_kurs_slutåret - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs else 0

            st.write(f"**Potentiell kurs idag:** {potentiell_kurs_idag:.2f} ({övervärdering_idag:+.1f} %)")
            st.write(f"**Potentiell kurs i slutet av året:** {potentiell_kurs_slutåret:.2f} ({övervärdering_slutåret:+.1f} %)")

            with st.form(f"edit_form_{index}"):
                ny_kurs = st.number_input("Nuvarande kurs", value=nuvarande_kurs, format="%.2f", key=f"kurs_{index}")
                ny_oms_år = st.number_input("Omsättning i år", value=oms_år, format="%.0f", key=f"omsår_{index}")
                ny_oms_nästa = st.number_input("Omsättning nästa år", value=oms_nästa, format="%.0f", key=f"omsnästa_{index}")
                ny_aktier = st.number_input("Antal aktier", value=aktier, format="%.0f", key=f"aktier_{index}")
                ny_ps1 = st.number_input("P/S 1", value=ps_tal[0], format="%.2f", key=f"ps1_{index}")
                ny_ps2 = st.number_input("P/S 2", value=ps_tal[1], format="%.2f", key=f"ps2_{index}")
                ny_ps3 = st.number_input("P/S 3", value=ps_tal[2], format="%.2f", key=f"ps3_{index}")
                ny_ps4 = st.number_input("P/S 4", value=ps_tal[3], format="%.2f", key=f"ps4_{index}")
                ny_ps5 = st.number_input("P/S 5", value=ps_tal[4], format="%.2f", key=f"ps5_{index}")
                spara = st.form_submit_button("Spara ändringar")

                if spara:
                    update_company(
                        company[0],
                        ny_kurs,
                        ny_oms_år,
                        ny_oms_nästa,
                        ny_aktier,
                        ny_ps1,
                        ny_ps2,
                        ny_ps3,
                        ny_ps4,
                        ny_ps5,
                    )
                    st.success("Uppdaterat!")
                    st.session_state.data_changed = True

            if st.button("❌ Ta bort", key=f"delete_{index}"):
                delete_company(company[0])
                st.warning(f"{company[1]} borttaget.")
                st.session_state.data_changed = True
