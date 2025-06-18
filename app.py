import streamlit as st
from database import init_db, insert_company, get_all_companies, update_company, delete_company
import numpy as np

# Initiera databasen
init_db()

st.title("Enkel Aktieanalys")

# Ladda bolagsdata från db
companies = get_all_companies()

# Om inga bolag finns
if not companies:
    st.info("Inga bolag i databasen, vänligen lägg till.")

# Hjälpfunktion för att beräkna potentiella kurser och undervärdering
def calculate(company):
    _, name, current_price, rev_this_year, rev_next_year, shares_out, ps1, ps2, ps3, ps4, ps5 = company
    ps_values = [ps1, ps2, ps3, ps4, ps5]
    ps_avg = np.mean(ps_values)
    pot_kurs_idag = (rev_this_year / shares_out) * ps_avg if shares_out else 0
    pot_kurs_slut_året = (rev_next_year / shares_out) * ps_avg if shares_out else 0
    undervärdering = ((pot_kurs_slut_året - current_price) / current_price * 100) if current_price else 0
    return pot_kurs_idag, pot_kurs_slut_året, undervärdering

# Beräkna och sortera bolag efter mest undervärderad (högst undervärderings%)
companies_calc = []
for comp in companies:
    pot_idag, pot_år, underv = calculate(comp)
    companies_calc.append((comp, pot_idag, pot_år, underv))

# Sortera fallande på undervärdering (mest undervärderad först)
companies_calc.sort(key=lambda x: x[3], reverse=True)

# Välj index för bläddring i session state
if "idx" not in st.session_state:
    st.session_state.idx = 0

# Navigeringsknappar
col1, col2, col3 = st.columns([1,3,1])
with col1:
    if st.button("⬅️ Föregående"):
        st.session_state.idx = max(st.session_state.idx - 1, 0)
with col3:
    if st.button("Nästa ➡️"):
        st.session_state.idx = min(st.session_state.idx + 1, len(companies_calc) - 1)

if companies_calc:
    comp, pot_idag, pot_år, underv = companies_calc[st.session_state.idx]
    id, name, current_price, rev_this_year, rev_next_year, shares_out, ps1, ps2, ps3, ps4, ps5 = comp

    st.subheader(f"Bolag: {name}")

    with st.form("edit_form", clear_on_submit=False):
        new_name = st.text_input("Bolag", value=name)
        new_current_price = st.number_input("Nuvarande kurs", value=current_price, format="%.4f", step=0.01)
        new_rev_this_year = st.number_input("Förväntad omsättning i år", value=rev_this_year, format="%.2f", step=0.01)
        new_rev_next_year = st.number_input("Förväntad omsättning nästa år", value=rev_next_year, format="%.2f", step=0.01)
        new_shares_out = st.number_input("Antal utestående aktier", value=shares_out, format="%.0f", step=1)
        new_ps1 = st.number_input("P/S 1", value=ps1, format="%.2f", step=0.01)
        new_ps2 = st.number_input("P/S 2", value=ps2, format="%.2f", step=0.01)
        new_ps3 = st.number_input("P/S 3", value=ps3, format="%.2f", step=0.01)
        new_ps4 = st.number_input("P/S 4", value=ps4, format="%.2f", step=0.01)
        new_ps5 = st.number_input("P/S 5", value=ps5, format="%.2f", step=0.01)

        submitted = st.form_submit_button("Uppdatera bolag")
        if submitted:
            update_company(id, new_name, new_current_price, new_rev_this_year, new_rev_next_year, new_shares_out, new_ps1, new_ps2, new_ps3, new_ps4, new_ps5)
            st.success("Bolag uppdaterat!")
            st.experimental_rerun()

    if st.button("Ta bort bolag"):
        delete_company(id)
        st.success("Bolag borttaget!")
        # Justera index om sista bolaget togs bort
        if st.session_state.idx > 0:
            st.session_state.idx -= 1
        st.experimental_rerun()

    # Visa beräkningar snyggt
    st.markdown("---")
    st.markdown(f"**Potentiell kurs idag:** {pot_idag:.2f} SEK")
    st.markdown(f"**Potentiell kurs i slutet av året:** {pot_år:.2f} SEK")
    st.markdown(f"**Under-/övervärdering (i %):** {underv:.2f} %")

else:
    st.info("Inga bolag att visa.")

st.markdown("---")
st.header("Lägg till nytt bolag")

with st.form("add_form", clear_on_submit=True):
    name = st.text_input("Bolag")
    current_price = st.number_input("Nuvarande kurs", format="%.4f", step=0.01)
    revenue_this_year = st.number_input("Förväntad omsättning i år", format="%.2f", step=0.01)
    revenue_next_year = st.number_input("Förväntad omsättning nästa år", format="%.2f", step=0.01)
    shares_outstanding = st.number_input("Antal utestående aktier", format="%.0f", step=1)
    ps1 = st.number_input("P/S 1", format="%.2f", step=0.01)
    ps2 = st.number_input("P/S 2", format="%.2f", step=0.01)
    ps3 = st.number_input("P/S 3", format="%.2f", step=0.01)
    ps4 = st.number_input("P/S 4", format="%.2f", step=0.01)
    ps5 = st.number_input("P/S 5", format="%.2f", step=0.01)

    submitted = st.form_submit_button("Lägg till bolag")
    if submitted:
        try:
            insert_company(name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5)
            st.success("Bolag tillagt!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Något gick fel: {e}")
