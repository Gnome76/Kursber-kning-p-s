import streamlit as st
from database import init_db, get_connection, update_bolag, DB_PATH
import pandas as pd
import os

# Initiera databasen
init_db()

st.set_page_config(layout="wide")
st.title("📊 Aktieanalys – Bläddra bolag")

# Lägg till nytt bolag
with st.expander("➕ Lägg till nytt bolag", expanded=True):
    with st.form("add_form"):
        namn = st.text_input("Bolag")
        kurs = st.number_input("Nuvarande kurs", step=0.01)
        oms1 = st.number_input("Omsättning i år (Mkr)", step=0.1)
        oms2 = st.number_input("Omsättning nästa år (Mkr)", step=0.1)
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

# Läs in bolagsdata
conn = get_connection()
rows = conn.execute("SELECT * FROM bolag").fetchall()
conn.close()

# Om bolag finns
if rows:
    df = pd.DataFrame(rows, columns=[
        "ID", "Bolag", "Kurs", "Omsättning i år", "Omsättning nästa år",
        "Aktier", "P/S 1", "P/S 2", "P/S 3", "P/S 4", "P/S 5"
    ])

    # Beräkningar
    df["P/S snitt"] = df[[f"P/S {i}" for i in range(1, 6)]].mean(axis=1)
    df["Pot kurs idag"] = (df["Omsättning i år"] / df["Aktier"]) * df["P/S snitt"]
    df["Pot kurs slut året"] = (df["Omsättning nästa år"] / df["Aktier"]) * df["P/S snitt"]
    df["% under/över idag"] = (df["Pot kurs idag"] / df["Kurs"] - 1) * 100
    df["% under/över slut året"] = (df["Pot kurs slut året"] / df["Kurs"] - 1) * 100

    df = df.sort_values("% under/över slut året", ascending=False).reset_index(drop=True)

    if "index" not in st.session_state:
        st.session_state.index = 0

    def prev():
        if st.session_state.index > 0:
            st.session_state.index -= 1

    def next():
        if st.session_state.index < len(df) - 1:
            st.session_state.index += 1

    st.markdown("### 📂 Bläddra mellan bolag")
    cols = st.columns([1, 6, 1])
    with cols[0]: st.button("⬅️ Föregående", on_click=prev)
    with cols[2]: st.button("Nästa ➡️", on_click=next)

    row = df.iloc[st.session_state.index]
    st.subheader(f"{row['Bolag']} ({st.session_state.index + 1} av {len(df)})")

    st.metric("Nuvarande kurs", f"{row['Kurs']:.2f} kr")
    st.metric("Potentiell kurs idag", f"{row['Pot kurs idag']:.2f} kr", delta=f"{row['% under/över idag']:.1f} %")
    st.metric("Potentiell kurs slut året", f"{row['Pot kurs slut året']:.2f} kr", delta=f"{row['% under/över slut året']:.1f} %")

    st.markdown("---")
    st.subheader("✏️ Redigera bolag")

    with st.form(f"edit_form_{row['ID']}"):
        namn = st.text_input("Bolag", value=row["Bolag"])
        kurs = st.number_input("Nuvarande kurs", value=row["Kurs"], step=0.01)
        oms1 = st.number_input("Omsättning i år (Mkr)", value=row["Omsättning i år"], step=0.1)
        oms2 = st.number_input("Omsättning nästa år (Mkr)", value=row["Omsättning nästa år"], step=0.1)
        aktier = st.number_input("Antal utestående aktier (miljoner)", value=row["Aktier"], step=0.01)
        ps = [st.number_input(f"P/S {i}", value=row[f"P/S {i}"], step=0.1) for i in range(1, 6)]

        save = st.form_submit_button("Spara ändringar")
        if save:
            update_bolag(row["ID"], namn, kurs, oms1, oms2, aktier, ps)
            st.success("Uppdaterat! Ladda om sidan.")

    if st.button("🗑️ Radera bolag"):
        conn = get_connection()
        conn.execute("DELETE FROM bolag WHERE id = ?", (row["ID"],))
        conn.commit()
        conn.close()
        st.success("Bolaget raderades – ladda om sidan.")
else:
    st.info("Inga bolag har lagts till ännu.")
