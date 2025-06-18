import streamlit as st
from database import (
    init_db, insert_company, get_all_companies,
    update_company, delete_company
)

init_db()
st.set_page_config(page_title="Aktieanalys", layout="centered")

st.title("📈 Enkel Aktieanalys")

# Formulär för att lägga till bolag
with st.expander("➕ Lägg till nytt bolag"):
    with st.form("add_company_form"):
        name = st.text_input("Bolagsnamn")
        current_price = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        revenue_this_year = st.number_input("Förväntad omsättning i år", min_value=0.0, format="%.0f")
        revenue_next_year = st.number_input("Förväntad omsättning nästa år", min_value=0.0, format="%.0f")
        shares_outstanding = st.number_input("Antal utestående aktier", min_value=1.0, format="%.0f")
        ps1 = st.number_input("P/S 1", min_value=0.0)
        ps2 = st.number_input("P/S 2", min_value=0.0)
        ps3 = st.number_input("P/S 3", min_value=0.0)
        ps4 = st.number_input("P/S 4", min_value=0.0)
        ps5 = st.number_input("P/S 5", min_value=0.0)

        submitted = st.form_submit_button("Lägg till bolag")
        if submitted and name:
            insert_company(name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps1, ps2, ps3, ps4, ps5)
            st.success(f"{name} har lagts till!")

# Hämta och sortera bolag
companies = get_all_companies()

def calc_values(company):
    avg_ps = sum(company['ps']) / 5
    pot_price_now = (company['rev_this'] / company['shares']) * avg_ps
    pot_price_future = (company['rev_next'] / company['shares']) * avg_ps
    under_over_now = ((pot_price_now - company['price']) / company['price']) * 100 if company['price'] else 0
    under_over_future = ((pot_price_future - company['price']) / company['price']) * 100 if company['price'] else 0
    return pot_price_now, pot_price_future, under_over_now, under_over_future

# Sortera efter mest undervärderad i framtiden
companies = sorted(
    companies,
    key=lambda c: calc_values(c)[3],
    reverse=True
)

# Visa ett bolag i taget
index = st.number_input("Bläddra mellan bolag", 0, len(companies)-1 if companies else 0, 0)
if companies:
    c = companies[index]
    pot_now, pot_future, under_now, under_future = calc_values(c)

    st.subheader(c['name'])
    st.write(f"**Nuvarande kurs:** {c['price']:.2f} kr")
    st.write(f"📌 **Potentiell kurs idag:** {pot_now:.2f} kr ({under_now:+.2f}%)")
    st.write(f"📌 **Potentiell kurs vid årets slut:** {pot_future:.2f} kr ({under_future:+.2f}%)")

    # Redigerbart formulär
    with st.expander("✏️ Redigera bolag"):
        with st.form(f"edit_{c['id']}"):
            new_price = st.number_input("Ny nuvarande kurs", value=c['price'], format="%.2f")
            new_rev_this = st.number_input("Ny omsättning i år", value=c['rev_this'], format="%.0f")
            new_rev_next = st.number_input("Ny omsättning nästa år", value=c['rev_next'], format="%.0f")
            new_shares = st.number_input("Nytt antal aktier", value=c['shares'], format="%.0f")
            new_ps1 = st.number_input("P/S 1", value=c['ps'][0])
            new_ps2 = st.number_input("P/S 2", value=c['ps'][1])
            new_ps3 = st.number_input("P/S 3", value=c['ps'][2])
            new_ps4 = st.number_input("P/S 4", value=c['ps'][3])
            new_ps5 = st.number_input("P/S 5", value=c['ps'][4])
            updated = st.form_submit_button("Uppdatera")
            if updated:
                update_company(c['id'], new_price, new_rev_this, new_rev_next, new_shares, new_ps1, new_ps2, new_ps3, new_ps4, new_ps5)
                st.experimental_rerun()

    # Ta bort
    if st.button("🗑️ Ta bort bolag", key=f"delete_{c['id']}"):
        delete_company(c['id'])
        st.success("Bolaget har tagits bort.")
        st.experimental_rerun()
else:
    st.info("Inga bolag tillagda ännu.")
