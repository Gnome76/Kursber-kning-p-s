import streamlit as st
from database import init_db, get_connection, update_bolag
import pandas as pd

# Initiera databas
init_db()

st.set_page_config(layout="wide")
st.title("📊 Aktieanalys – Överskådlig presentation")

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
    # Sortera efter mest undervärderad enligt framtida potentiell kurs
    df = df.sort_values("% vs idag - pot kurs slut året")

    # Kolumner att visa
    display_cols = [
        "Bolag", "Kurs",
        "Pot. kurs idag", "% vs idag - pot kurs idag",
        "Pot. kurs slut året", "% vs idag - pot kurs slut året"
    ]

    # Färgmarkering för över-/undervärdering (rött/ grönt)
    def color_val(val):
        if val > 0:
            return 'color: green; font-weight: bold;'
        elif val < 0:
            return 'color: red; font-weight: bold;'
        return ''

    st.subheader("📋 Bolag & analys (sorterat på mest undervärderad)")

    styled_df = df[display_cols].style.format({
        "Kurs": "{:.2f}",
        "Pot. kurs idag": "{:.2f}",
        "% vs idag - pot kurs idag": "{:+.1f}%",
        "Pot. kurs slut året": "{:.2f}",
        "% vs idag - pot kurs slut året": "{:+.1f}%"
    }).applymap(color_val, subset=["% vs idag - pot kurs idag", "% vs idag - pot kurs slut året"])

    st.dataframe(styled_df, use_container_width=True)

    # ✏️ Redigera & ta bort bolag
    st.subheader("✏️ Redigera / Radera bolag")
    for _, row in df.reset_index(drop=True).iterrows():
        with st.expander(f"{row['Bolag']} - {row['% vs idag - pot kurs slut året']:+.1f}%"):
            cols = st.columns(2)
            with cols[0]:
                namn = st.text_input("Bolag", value=row["Bolag"], key=f"e_namn_{row['ID']}")
                kurs = st.number_input("Nuvarande kurs", value=row["Kurs"], step=0.01, key=f"e_kurs_{row['ID']}")
                oms1 = st.number_input("Omsättning i år", value=row["Omsättning år 1"], step=0.1, key=f"e_oms1_{row['ID']}")
                oms2 = st.number_input("Omsättning nästa år", value=row["Omsättning år 2"], step=0.1, key=f"e_oms2_{row['ID']}")
                aktier = st.number_input("Antal utestående aktier", value=row["Aktier"], step=0.01, key=f"e_akt_{row['ID']}")
            with cols[1]:
                ps = [st.number_input(f"P/S {i}", value=row[f"P/S {i}"], step=0.1, key=f"e_ps{i}_{row['ID']}") for i in range(1, 6)]

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
