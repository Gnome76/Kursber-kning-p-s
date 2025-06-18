import streamlit as st
from database import init_db, get_connection, update_bolag
import pandas as pd

# Initiera databas
init_db()

st.set_page_config(layout="wide")
st.title("📊 Aktieanalys – med editering & övervärdering")

def calculate_df(rows):
    df = pd.DataFrame(rows, columns=[
        "ID", "Bolag", "Kurs", "Omsättning år 1", "Omsättning år 2",
        "Aktier", "P/S 1", "P/S 2", "P/S 3", "P/S 4", "P/S 5"
    ])
    df["P/S snitt"] = df[[f"P/S {i}" for i in range(1, 6)]].mean(axis=1)
    df["Pot. kurs idag"] = (df["Omsättning år 1"] / df["Aktier"]) * df["P/S snitt"]
    df["Pot. kurs slut året"] = (df["Omsättning år 2"] / df["Aktier"]) * df["P/S snitt"]
    df["% vs idag"] = (df["Pot. kurs slut året"] / df["Kurs"] - 1) * 100
    return df

# 🆕 Lägg till bolag
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
    # Sortera efter mest undervärderad (lägst % vs idag först)
    df = df.sort_values("% vs idag")

    st.subheader("📋 Bolag & analys")
    highlight = df.style.applymap(
        lambda v: 'color: green;' if v > 0 else ('color: red;' if v < 0 else ''),
        subset=["% vs idag"]
    ).format({
        "Kurs": "{:.2f}",
        "P/S snitt": "{:.2f}",
        "Pot. kurs idag": "{:.2f}",
        "Pot. kurs slut året": "{:.2f}",
        "% vs idag": "{:+.1f}%"
    })
    st.dataframe(highlight, use_container_width=True)

    # ✏️ Redigering per rad
    st.subheader("✏️ Redigera / Radera bolag")
    for _, row in df.reset_index(drop=True).iterrows():
        with st.expander(f"{row['Bolag']} (ID {row['ID']}) - {row['% vs idag']:+.1f}%"):
            cols = st.columns(2)
            with cols[0]:
                namn = st.text_input("Bolag", value=row["Bolag"], key=f"e_namn_{row['ID']}")
                kurs = st.number_input("Kurs", value=row["Kurs"], step=0.01, key=f"e_kurs_{row['ID']}")
                oms1 = st.number_input("Oms år 1", value=row["Omsättning år 1"], step=0.1, key=f"e_oms1_{row['ID']}")
                oms2 = st.number_input("Oms år 2", value=row["Omsättning år 2"], step=0.1, key=f"e_oms2_{row['ID']}")
                aktier = st.number_input("Aktier", value=row["Aktier"], step=0.01, key=f"e_akt_{row['ID']}")
            with cols[1]:
                ps = [st.number_input(f"P/S {i}", value=row[f"P/S {i}"], step=0.1, key=f"e_ps{ i }_{row['ID']}") for i in range(1, 6)]

            btn_save = st.button("Spara ändringar", key=f"save_{row['ID']}")
            btn_delete = st.button("Radera bolag", key=f"del_{row['ID']}")

            if btn_save:
                update_bolag(row["ID"], namn, kurs, oms1, oms2, aktier, ps)
                st.success(f"{namn} sparad – ladda om sidan.")
            if btn_delete:
                conn = get_connection()
                conn.execute("DELETE FROM bolag WHERE id = ?", (row["ID"],))
                conn.commit()
                conn.close()
                st.success(f"{row['Bolag']} raderat – ladda om sidan.")
else:
    st.info("Inga bolag inlagda ännu.")
