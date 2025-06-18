import streamlit as st
from database import init_db, insert_company, get_all_companies, update_company, delete_company

st.set_page_config(page_title="Aktieanalys", layout="centered")

init_db()

st.title("📊 Aktieanalys")

with st.form("company_form", clear_on_submit=True):
    st.subheader("Lägg till bolag")
    name = st.text_input("Bolag")
    current_price = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    revenue_this_year = st.number_input("Förväntad omsättning i år", min_value=0.0, format="%.0f")
    revenue_next_year = st.number_input("Förväntad omsättning nästa år", min_value=0.0, format="%.0f")
    shares_outstanding = st.number_input("Antal utestående aktier", min_value=1, format="%d")
    ps_values = [st.number_input(f"P/S {i+1}", min_value=0.0, format="%.2f") for i in range(5)]
    
    submitted = st.form_submit_button("Lägg till bolag")
    if submitted:
        if name:
            insert_company(name, current_price, revenue_this_year, revenue_next_year, shares_outstanding, ps_values)
            st.success(f"{name} har lagts till!")
            st.experimental_rerun()
        else:
            st.warning("Du måste ange ett bolagsnamn.")

# Hämta och sortera bolagen
companies = get_all_companies()

# Beräkna potentiell kurs och undervärdering
def calculate(company):
    _, name, current_price, rev_this, rev_next, shares, ps1, ps2, ps3, ps4, ps5 = company
    avg_ps = sum([ps1, ps2, ps3, ps4, ps5]) / 5 if shares else 0

    try:
        potential_today = (rev_this / shares) * avg_ps if shares else 0
        potential_year_end = (rev_next / shares) * avg_ps if shares else 0
    except ZeroDivisionError:
        potential_today = 0
        potential_year_end = 0

    undervalued_today = ((potential_today - current_price) / current_price) * 100 if current_price else 0
    undervalued_year = ((potential_year_end - current_price) / current_price) * 100 if current_price else 0

    return {
        "id": company[0],
        "name": name,
        "current_price": current_price,
        "potential_today": potential_today,
        "potential_year_end": potential_year_end,
        "undervalued_today": undervalued_today,
        "undervalued_year": undervalued_year,
        "rev_this": rev_this,
        "rev_next": rev_next,
        "shares": shares,
        "ps": [ps1, ps2, ps3, ps4, ps5],
    }

calculated = [calculate(c) for c in companies]
sorted_companies = sorted(calculated, key=lambda x: x["undervalued_year"], reverse=True)

# Visa bolag ett och ett
if sorted_companies:
    st.subheader("📈 Analysresultat")

    page = st.number_input("Bläddra mellan bolag", min_value=1, max_value=len(sorted_companies), step=1)
    selected = sorted_companies[page - 1]

    st.markdown(f"### {selected['name']}")
    st.write(f"**Nuvarande kurs:** {selected['current_price']:.2f} kr")
    st.write(f"**Potentiell kurs idag:** {selected['potential_today']:.2f} kr")
    st.write(f"**Potentiell kurs vid årets slut:** {selected['potential_year_end']:.2f} kr")

    undervalue_today = selected['undervalued_today']
    undervalue_year = selected['undervalued_year']
    st.write(f"**Över-/undervärdering idag:** {undervalue_today:+.2f}%")
    st.write(f"**Över-/undervärdering slutet av året:** {undervalue_year:+.2f}%")

    st.markdown("---")
    st.subheader("✏️ Redigera")

    # Redigerbara fält
    fields = {
        "current_price": st.number_input("Redigera: Nuvarande kurs", value=selected["current_price"], key="edit_price"),
        "revenue_this_year": st.number_input("Redigera: Omsättning i år", value=selected["rev_this"], key="edit_rev_this"),
        "revenue_next_year": st.number_input("Redigera: Omsättning nästa år", value=selected["rev_next"], key="edit_rev_next"),
        "shares_outstanding": st.number_input("Redigera: Utestående aktier", value=selected["shares"], key="edit_shares", step=1),
    }

    for i in range(5):
        fields[f"ps{i+1}"] = st.number_input(f"Redigera: P/S {i+1}", value=selected["ps"][i], key=f"edit_ps{i+1}")

    if st.button("Spara ändringar"):
        for field, value in fields.items():
            update_company(selected["id"], field, value)
        st.success("Uppdaterad!")
        st.experimental_rerun()

    if st.button("❌ Ta bort bolag"):
        delete_company(selected["id"])
        st.warning(f"{selected['name']} har tagits bort.")
        st.experimental_rerun()
else:
    st.info("Inga bolag inlagda ännu.")
