import streamlit as st
from database import (
    init_db, insert_company, get_all_companies,
    update_company, delete_company
)
import statistics

st.set_page_config(page_title="Aktieanalys", layout="wide")
init_db()

st.title("📈 Aktieanalys med P/S-tal")

# Formulär för att lägga till bolag
with st.form("Lägg till bolag", clear_on_submit=True):
    st.subheader("Lägg till nytt bolag")
    bolag = st.text_input("Bolag")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    omsättning_år = st.number_input("Förväntad omsättning i år", min_value=0.0, format="%.2f")
    omsättning_nästa_år = st.number_input("Förväntad omsättning nästa år", min_value=0.0, format="%.2f")
    antal_aktier = st.number_input("Antal utestående aktier", min_value=1, format="%d")
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
    ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Lägg till bolag")

    if submitted and bolag:
        insert_company((
            bolag, nuvarande_kurs, omsättning_år, omsättning_nästa_år,
            antal_aktier, ps1, ps2, ps3, ps4, ps5
        ))
        st.success(f"{bolag} har lagts till.")
        st.experimental_rerun()

# Hämta alla bolag
companies = get_all_companies()

# Bearbeta bolagsdata
processed = []
for row in companies:
    (
        company_id, bolag, nuvarande_kurs, omsättning_år, omsättning_nästa_år,
        antal_aktier, ps1, ps2, ps3, ps4, ps5
    ) = row

    ps_snitt = statistics.mean([ps1, ps2, ps3, ps4, ps5])
    potentiell_kurs_idag = (omsättning_år / antal_aktier) * ps_snitt if antal_aktier else 0
    potentiell_kurs_slutåret = (omsättning_nästa_år / antal_aktier) * ps_snitt if antal_aktier else 0

    undervärdering_idag = ((potentiell_kurs_idag - nuvarande_kurs) / nuvarande_kurs * 100) if nuvarande_kurs else 0
    undervärdering_slutåret = ((potentiell_kurs_slutåret - nuvarande_kurs) / nuvarande_kurs * 100) if nuvarande_kurs else 0

    processed.append({
        "id": company_id,
        "bolag": bolag,
        "nuvarande_kurs": nuvarande_kurs,
        "omsättning_år": omsättning_år,
        "omsättning_nästa_år": omsättning_nästa_år,
        "antal_aktier": antal_aktier,
        "ps_snitt": ps_snitt,
        "pot_kurs_idag": potentiell_kurs_idag,
        "pot_kurs_slut": potentiell_kurs_slutåret,
        "undervärdering_idag": undervärdering_idag,
        "undervärdering_slut": undervärdering_slutåret
    })

# Sortera mest undervärderad först
processed.sort(key=lambda x: x["undervärdering_slut"], reverse=True)

# Visa ett bolag i taget med bläddring
if processed:
    st.subheader("📊 Analys: ett bolag i taget")
    index = st.number_input("Välj bolag", min_value=0, max_value=len(processed)-1, step=1)
    data = processed[index]

    st.markdown(f"### {data['bolag']}")
    st.write(f"**Nuvarande kurs:** {data['nuvarande_kurs']:.2f} kr")
    st.write(f"**P/S-snitt:** {data['ps_snitt']:.2f}")
    st.write(f"**Potentiell kurs idag:** {data['pot_kurs_idag']:.2f} kr")
    st.write(f"**Över/undervärdering idag:** {data['undervärdering_idag']:.2f} %")
    st.write(f"**Potentiell kurs i slutet av året:** {data['pot_kurs_slut']:.2f} kr")
    st.write(f"**Över/undervärdering i slutet av året:** {data['undervärdering_slut']:.2f} %")

    # Redigera data inline
    st.markdown("---")
    st.subheader("✏️ Redigera bolagsdata")

    with st.form(f"edit_{data['id']}"):
        nya_data = {
            "nuvarande_kurs": st.number_input("Nuvarande kurs", value=data["nuvarande_kurs"], format="%.2f"),
            "omsättning_år": st.number_input("Omsättning i år", value=data["omsättning_år"], format="%.2f"),
            "omsättning_nästa_år": st.number_input("Omsättning nästa år", value=data["omsättning_nästa_år"], format="%.2f"),
            "antal_aktier": st.number_input("Antal aktier", value=data["antal_aktier"], format="%d"),
            "ps1": st.number_input("P/S 1", value=ps1 := companies[index][6], format="%.2f"),
            "ps2": st.number_input("P/S 2", value=ps2 := companies[index][7], format="%.2f"),
            "ps3": st.number_input("P/S 3", value=ps3 := companies[index][8], format="%.2f"),
            "ps4": st.number_input("P/S 4", value=ps4 := companies[index][9], format="%.2f"),
            "ps5": st.number_input("P/S 5", value=ps5 := companies[index][10], format="%.2f"),
        }

        if st.form_submit_button("Spara ändringar"):
            update_company(data["id"], (
                data["bolag"], nya_data["nuvarande_kurs"], nya_data["omsättning_år"],
                nya_data["omsättning_nästa_år"], nya_data["antal_aktier"],
                nya_data["ps1"], nya_data["ps2"], nya_data["ps3"],
                nya_data["ps4"], nya_data["ps5"]
            ))
            st.success("Bolaget uppdaterades.")
            st.rerun()

    if st.button("🗑️ Ta bort bolag"):
        delete_company(data["id"])
        st.success(f"{data['bolag']} togs bort.")
        st.rerun()
else:
    st.info("Inga bolag har lagts till ännu.")
