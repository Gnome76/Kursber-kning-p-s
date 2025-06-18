import streamlit as st
from database import init_db, get_connection
import pandas as pd

# Initiera databasen
init_db()

st.title("📊 Enkel Aktieanalys App")

# Formulär för att lägga till nytt bolag
with st.form("add_form"):
    namn = st.text_input("Bolag")
    kurs = st.number_input("Nuvarande kurs", step=0.01)
    oms1 = st.number_input("Förväntad omsättning i år (Mkr)", step=0.1)
    oms2 = st.number_input("Förväntad omsättning nästa år (Mkr)", step=0.1)
    aktier = st.number_input("Antal utestående aktier (miljoner)", step=0.01)
    ps = [st.number_input(f"P/S {i}", step=0.1, key=f"ps{i}") for i in range(1, 6)]

    submitted = st.form_submit_button("Lägg till bolag")
    if submitted and namn:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO bolag (namn, kurs, oms1, oms2, aktier, ps1, ps2, ps3, ps4, ps5)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (namn, kurs, oms1, oms2, aktier, *ps))
        conn.commit()
        conn.close()
        st.success(f"{namn} tillagd!")

# Visa alla bolag
conn = get_connection()
rows = conn.execute("SELECT * FROM bolag").fetchall()
conn.close()

if rows:
    df = pd.DataFrame(rows, columns=[
        "ID", "Bolag", "Kurs", "Omsättning år 1", "Omsättning år 2",
        "Aktier", "P/S 1", "P/S 2", "P/S 3", "P/S 4", "P/S 5"
    ])

    # Beräkna genomsnittligt P/S
    df["P/S snitt"] = df[["P/S 1", "P/S 2", "P/S 3", "P/S 4", "P/S 5"]].mean(axis=1)

    # Potentiell kurs idag
    df["Pot. kurs idag"] = (df["Omsättning år 1"] / df["Aktier"]) * df["P/S snitt"]

    # Potentiell kurs i slutet av året
    df["Pot. kurs slut året"] = (df["Omsättning år 2"] / df["Aktier"]) * df["P/S snitt"]

    st.subheader("📄 Alla bolag")
    st.dataframe(df)

    # Radera en rad
    ids = df["ID"].tolist()
    val = st.selectbox("Välj ID att ta bort", ids)
    if st.button("Ta bort bolag"):
        conn = get_connection()
        conn.execute("DELETE FROM bolag WHERE id = ?", (val,))
        conn.commit()
        conn.close()
        st.success("Bolaget raderat. Ladda om sidan.")
else:
    st.info("Inga bolag inlagda ännu.")
