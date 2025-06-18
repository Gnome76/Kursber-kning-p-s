import streamlit as st
from database import init_db, get_connection, update_bolag
import pandas as pd

# Initiera databas
init_db()

st.set_page_config(layout="wide")
st.title("📊 Aktieanalys – Visa bolag ett och ett")

def calculate_df(rows):
    df = pd.DataFrame(rows, columns=[
        "ID", "Bolag", "Kurs", "Omsättning år 1", "Omsättning år 2",
        "Aktier", "P/S 1", "P/S 2", "P/S 3", "P/S 4", "P/S 5"
    ])
    df["P/S snitt"] = df[[f"P/S {i}" for i in range(1, 6)]].mean(axis=1)

    df["Pot. kurs idag"] = (df["Omsättning år 1"] / df["Aktier"]) * df["P/S snitt"]
    df["Pot. kurs slut året"] = (df["Omsättning år 2"] / df["Aktier"]) * df["P/S snitt"]

    df["% vs idag - pot kurs idag"] = (df["Pot. kurs idag"] / df["Kurs"] - 1) * 100
    df["% vs idag - pot kurs slut året"] = (df["Pot. kurs slut året"] / df["Kurs"] - 1) * 100

    return df

# Lägg till bolag
with st.expander("➕ Lägg till nytt bolag", expanded=True):
    with st.form("add_form"):
        namn = st.text_input("Bolag")
        kurs = st.number_input("Nuvarande kurs", step=0.01)
        oms1 = st.number_input("Förväntad omsättning i år (Mkr)", step=0.1)
        oms2 = st.number_input("Förväntad omsättning nästa år (Mkr)", step=0.1)
        aktier = st.number_input("Antal utestående aktier (miljoner)", step=0.01)
        ps = [st.number_input(f"P/S {i}", step=0.1, key=f"add_ps{i}") for i in range(1, 6)]
        submitted = st.form_submit_button("Lägg till bolag")
        if submitted:
            if namn:
                conn = get_connection()
                c = conn.cursor()
                c.execute("""
                    INSERT INTO bolag (namn, kurs, oms1, oms2, aktier, ps1, ps2, ps3, ps4, ps5)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (namn, kurs, oms1, oms2, aktier, *ps))
                conn.commit()
                conn.close()
                st.success(f"{namn} tillagd – ladda om sidan.")
            else:
                st.warning("Bolagsnamn krävs!")

# Hämta & beräkna data
conn = get_connection()
rows = conn.execute("SELECT * FROM bolag").fetchall()
conn.close()

if rows:
    df = calculate_df(rows)
    # Sortera efter mest undervärderad enligt framtida potentiell kurs (mest negativ % först)
    df = df.sort_values("% vs idag - pot kurs slut året", ascending=True).reset_index(drop=True)

    # Session state för index
    if "index" not in st.session_state:
        st.session_state.index = 0

    def prev_bolag():
        if st.session_state.index > 0:
            st.session_state.index -= 1

    def next_bolag():
        if st.session_state.index < len(df) - 1:
            st.session_state.index += 1

    cols_nav = st.columns([1,6,1])
    with cols_nav[0]:
        st.button("⬅️ Föregående", on_click=prev_bolag)
    with cols_nav[2]:
        st.button("Nästa ➡️", on_click=next_bolag)

    i = st.session_state.index
    row = df.iloc[i]

    st.markdown(f"### {row['Bolag']} ({i+1} av {len(df)})")
    st.write(f"**Nuvarande kurs:** {row['Kurs']:.2f} kr")

    def color_val(val):
        if val > 0:
            return 'color: green; font-weight: bold;'
        elif val < 0:
            return 'color: red; font-weight: bold;'
        return ''

    st.markdown(f"**Potentiell kurs idag:** {row['Pot. kurs idag']:.2f} kr")
    st.markdown(f"**Över-/undervärdering idag:** "
                f"<span style='{color_val(row['% vs idag - pot kurs idag'])}'>{row['% vs idag - pot kurs idag']:+.1f}%</span>",
                unsafe_allow_html=True)

    st.markdown(f"**Potentiell kurs i slutet av året:** {row['Pot. kurs slut året']:.2f} kr")
    st.markdown(f"**Över-/undervärdering slut året:** "
                f"<span style='{color_val(row['% vs idag - pot kurs slut året'])}'>{row['% vs idag - pot kurs slut året']:+.1f}%</span>",
                unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("✏️ Redigera bolag")

    with st.form(f"edit_form_{row['ID']}"):
        cols1, cols2 = st.columns(2)
        with cols1:
            namn = st.text_input("Bolag", value=row["Bolag"])
            kurs = st.number_input("Nuvarande kurs", value=row["Kurs"], step=0.01)
            oms1 = st.number_input("Omsättning i år (Mkr)", value=row["Omsättning år 1"], step=0.1)
            oms2 = st.number_input("Omsättning nästa år (Mkr)", value=row["Omsättning år 2"], step=0.1)
            aktier = st.number_input("Antal utestående aktier (miljoner)", value=row["Aktier"], step=0.01)
        with cols2:
            ps = [st.number_input(f"P/S {i}", value=row[f"P/S {i}"], step=0.1) for i in range(1, 6)]

        btn_save = st.form_submit_button("Spara ändringar")

        if btn_save:
            update_bolag(row["ID"], namn, kurs, oms1, oms2, aktier, ps)
            st.success(f"{namn} sparad – ladda om sidan för uppdatering.")

    st.markdown("---")
    if st.button("Radera bolag"):
        conn = get_connection()
        conn.execute("DELETE FROM bolag WHERE id = ?", (row["ID"],))
        conn.commit()
        conn.close()
        st.success(f"{row['Bolag']} raderat – ladda om sidan.")
else:
    st.info("Inga bolag inlagda ännu.")
