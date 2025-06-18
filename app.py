import streamlit as st
from database import init_db, insert_company, get_all_companies, update_company, delete_company

# Initiera databas (skapar tabell om den inte finns)
init_db()

# Initiera session_state flagga för omrendering
if "uppdatera" not in st.session_state:
    st.session_state["uppdatera"] = False

def trigga_omrendering():
    st.session_state["uppdatera"] = not st.session_state["uppdatera"]

st.title("Aktieanalysapp")

st.header("Lägg till nytt bolag")

with st.form("lagg_till_form"):
    bolag = st.text_input("Bolag")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    omsattning_i_ar = st.number_input("Förväntad omsättning i år (MSEK)", min_value=0.0, format="%.2f")
    omsattning_nasta_ar = st.number_input("Förväntad omsättning nästa år (MSEK)", min_value=0.0, format="%.2f")
    antal_aktier = st.number_input("Antal utestående aktier (miljoner)", min_value=0.0, format="%.2f")
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
    ps5 = st.number_input("P/S 5", min_value=0.0, format="%.2f")
    
    submit = st.form_submit_button("Lägg till bolag")
    if submit:
        if bolag.strip() == "":
            st.error("Ange bolagsnamn!")
        else:
            insert_company(
                bolag.strip(),
                nuvarande_kurs,
                omsattning_i_ar,
                omsattning_nasta_ar,
                antal_aktier,
                ps1, ps2, ps3, ps4, ps5
            )
            st.success(f"Bolag '{bolag}' tillagt!")
            trigga_omrendering()

st.header("Hantera bolag")

companies = get_all_companies()

def berakna_undervardering(c):
    # c = (id, bolag, nuvarande_kurs, oms_i_ar, oms_nasta_ar, antal_aktier, ps1, ps2, ps3, ps4, ps5)
    ps_medel = (c[6] + c[7] + c[8] + c[9] + c[10]) / 5
    potentiell_slut_ar = (c[4] / c[5]) * ps_medel if c[5] > 0 else 0
    if c[2] == 0:
        return -999999
    return potentiell_slut_ar / c[2]

companies = sorted(companies, key=berakna_undervardering, reverse=True)

if companies:
    index = st.number_input("Välj bolagsindex", min_value=0, max_value=len(companies)-1, value=0, step=1)
    c = companies[index]

    st.subheader(f"Redigera bolag: {c[1]}")

    with st.form("redigera_form"):
        bolag = st.text_input("Bolag", value=c[1])
        nuvarande_kurs = st.number_input("Nuvarande kurs", value=c[2], format="%.2f")
        oms_i_ar = st.number_input("Förväntad omsättning i år (MSEK)", value=c[3], format="%.2f")
        oms_nasta_ar = st.number_input("Förväntad omsättning nästa år (MSEK)", value=c[4], format="%.2f")
        antal_aktier = st.number_input("Antal utestående aktier (miljoner)", value=c[5], format="%.2f")
        ps1 = st.number_input("P/S 1", value=c[6], format="%.2f")
        ps2 = st.number_input("P/S 2", value=c[7], format="%.2f")
        ps3 = st.number_input("P/S 3", value=c[8], format="%.2f")
        ps4 = st.number_input("P/S 4", value=c[9], format="%.2f")
        ps5 = st.number_input("P/S 5", value=c[10], format="%.2f")

        submit = st.form_submit_button("Uppdatera bolag")
        if submit:
            if bolag.strip() == "":
                st.error("Ange bolagsnamn!")
            else:
                update_company(
                    c[0],
                    bolag.strip(),
                    nuvarande_kurs,
                    oms_i_ar,
                    oms_nasta_ar,
                    antal_aktier,
                    ps1, ps2, ps3, ps4, ps5
                )
                st.success(f"Bolag '{bolag}' uppdaterat!")
                trigga_omrendering()

    if st.button(f"Radera bolag {c[1]}"):
        delete_company(c[0])
        st.success(f"Bolag '{c[1]}' raderat!")
        trigga_omrendering()

    ps_medel = (c[6] + c[7] + c[8] + c[9] + c[10]) / 5
    if c[5] > 0:
        potentiell_kurs_idag = (c[3] / c[5]) * ps_medel
        potentiell_kurs_slut_ar = (c[4] / c[5]) * ps_medel
    else:
        potentiell_kurs_idag = 0
        potentiell_kurs_slut_ar = 0

    def procent_overundervarde(pot_kurs, nuv_kurs):
        if nuv_kurs == 0:
            return 0
        return ((pot_kurs / nuv_kurs) - 1) * 100

    procent_idag = procent_overundervarde(potentiell_kurs_idag, c[2])
    procent_slut_ar = procent_overundervarde(potentiell_kurs_slut_ar, c[2])

    st.markdown("---")
    st.markdown(f"**Potentiell kurs idag:** {potentiell_kurs_idag:.2f} SEK ({procent_idag:+.1f} %)")
    st.markdown(f"**Potentiell kurs i slutet av året:** {potentiell_kurs_slut_ar:.2f} SEK ({procent_slut_ar:+.1f} %)")
else:
    st.info("Inga bolag tillagda ännu.")
