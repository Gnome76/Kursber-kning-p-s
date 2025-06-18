import streamlit as st
from database import init_db, insert_company, get_all_companies, update_company, delete_company

# Initiera databasen (skapa tabell om inte finns)
init_db()

def beräkna_potentiell_kurs(omsättning, antal_aktier, ps_värden):
    if antal_aktier == 0:
        return 0
    ps_genomsnitt = sum(ps_värden) / len(ps_värden)
    return (omsättning / antal_aktier) * ps_genomsnitt

def beräkna_undervärdering(pot_kurs, nuvarande_kurs):
    if nuvarande_kurs == 0:
        return 0
    return ((pot_kurs - nuvarande_kurs) / nuvarande_kurs) * 100

def main():
    st.title("Aktieanalysapp")

    companies = get_all_companies()

    # Sortera listan efter mest undervärderad, dvs störst positiv procent först
    def sort_key(c):
        oms_i_år = c[3]
        oms_nästa_år = c[4]
        antal_aktier = c[5]
        ps_värden = [c[6], c[7], c[8], c[9], c[10]]

        pot_kurs_slutet = beräkna_potentiell_kurs(oms_nästa_år, antal_aktier, ps_värden)
        nuv_kurs = c[2]
        undervärdering = beräkna_undervärdering(pot_kurs_slutet, nuv_kurs)
        return -undervärdering  # Negativ för att sortera fallande

    companies = sorted(companies, key=sort_key)

    # Välj bolag att visa/ändra
    index = st.number_input("Välj bolagsnummer att redigera (0 baserat)", min_value=0, max_value=max(0,len(companies)-1), value=0, step=1)

    if companies:
        # Läs in värden från databasen
        bolag = companies[index][1]
        nuvarande_kurs = companies[index][2]
        omsättning_i_år = companies[index][3]
        omsättning_nästa_år = companies[index][4]
        antal_aktier = companies[index][5]
        ps1 = companies[index][6]
        ps2 = companies[index][7]
        ps3 = companies[index][8]
        ps4 = companies[index][9]
        ps5 = companies[index][10]

        # Formulär med tilldelning utan walrus-operator
        nytt_bolag = st.text_input("Bolag", value=bolag)
        ny_nuvarande_kurs = st.number_input("Nuvarande kurs", value=nuvarande_kurs, format="%.2f")
        ny_oms_i_år = st.number_input("Förväntad omsättning i år", value=omsättning_i_år, format="%.0f")
        ny_oms_nästa_år = st.number_input("Förväntad omsättning nästa år", value=omsättning_nästa_år, format="%.0f")
        ny_antal_aktier = st.number_input("Antal utestående aktier", value=antal_aktier, format="%.0f")
        ny_ps1 = st.number_input("P/S 1", value=ps1, format="%.2f")
        ny_ps2 = st.number_input("P/S 2", value=ps2, format="%.2f")
        ny_ps3 = st.number_input("P/S 3", value=ps3, format="%.2f")
        ny_ps4 = st.number_input("P/S 4", value=ps4, format="%.2f")
        ny_ps5 = st.number_input("P/S 5", value=ps5, format="%.2f")

        if st.button("Uppdatera bolag"):
            update_company(
                companies[index][0],
                nytt_bolag,
                ny_nuvarande_kurs,
                ny_oms_i_år,
                ny_oms_nästa_år,
                ny_antal_aktier,
                ny_ps1,
                ny_ps2,
                ny_ps3,
                ny_ps4,
                ny_ps5
            )
            st.experimental_rerun()

        # Visa potentiella kurser och undervärdering
        ps_lista = [ny_ps1, ny_ps2, ny_ps3, ny_ps4, ny_ps5]

        pot_kurs_idag = beräkna_potentiell_kurs(ny_oms_i_år, ny_antal_aktier, ps_lista)
        pot_kurs_slutet = beräkna_potentiell_kurs(ny_oms_nästa_år, ny_antal_aktier, ps_lista)

        undervärdering_idag = beräkna_undervärdering(pot_kurs_idag, ny_nuvarande_kurs)
        undervärdering_slutet = beräkna_undervärdering(pot_kurs_slutet, ny_nuvarande_kurs)

        st.markdown(f"### Potentiell kurs idag: {pot_kurs_idag:.2f} SEK")
        st.markdown(f"Under-/övervärdering idag: {undervärdering_idag:.2f} %")
        st.markdown(f"### Potentiell kurs i slutet av året: {pot_kurs_slutet:.2f} SEK")
        st.markdown(f"Under-/övervärdering i slutet av året: {undervärdering_slutet:.2f} %")

        if st.button("Radera bolag"):
            delete_company(companies[index][0])
            st.experimental_rerun()

    else:
        st.write("Inga bolag tillagda än.")

    st.markdown("---")

    # Lägg till nytt bolag-formulär
    with st.form("nytt_bolag_form"):
        nytt_namn = st.text_input("Bolagsnamn")
        nytt_nuvarande_kurs = st.number_input("Nuvarande kurs", format="%.2f")
        nytt_oms_i_år = st.number_input("Förväntad omsättning i år", format="%.0f")
        nytt_oms_nästa_år = st.number_input("Förväntad omsättning nästa år", format="%.0f")
        nytt_antal_aktier = st.number_input("Antal utestående aktier", format="%.0f")
        nytt_ps1 = st.number_input("P/S 1", format="%.2f")
        nytt_ps2 = st.number_input("P/S 2", format="%.2f")
        nytt_ps3 = st.number_input("P/S 3", format="%.2f")
        nytt_ps4 = st.number_input("P/S 4", format="%.2f")
        nytt_ps5 = st.number_input("P/S 5", format="%.2f")

        submitted = st.form_submit_button("Lägg till bolag")

        if submitted:
            insert_company(
                nytt_namn,
                nytt_nuvarande_kurs,
                nytt_oms_i_år,
                nytt_oms_nästa_år,
                nytt_antal_aktier,
                nytt_ps1,
                nytt_ps2,
                nytt_ps3,
                nytt_ps4,
                nytt_ps5
            )
            st.experimental_rerun()

if __name__ == "__main__":
    main()
