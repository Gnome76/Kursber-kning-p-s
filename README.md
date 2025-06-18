# Aktieanalysapp 📈

Den här Streamlit-appen låter dig:

- Lägga till och redigera bolagsdata
- Beräkna potentiella aktiekurser baserat på omsättning och P/S-tal
- Se om ett bolag är över- eller undervärderat
- Spara datan i en databas som inte försvinner vid omstart
- Bläddra bland bolag sorterat från mest undervärderad till minst

## 🧩 Funktioner

- CRUD: Lägg till, redigera, ta bort bolag
- Potentiell kurs idag och i slutet av året
- Färgkodad värdering (% över/undervärdering)
- Data sparas i `/data/database.db`

## 🧪 Så här kör du appen

1. Skapa en mappstruktur:
    ```
    /data/.keep
    /.streamlit/config.toml
    ```

2. Kör appen lokalt:
    ```bash
    streamlit run app.py
    ```

3. Ladda upp till GitHub och deploya via [Streamlit Cloud](https://streamlit.io/cloud)

## 📁 Viktiga filer

| Fil | Beskrivning |
|-----|-------------|
| `app.py` | Huvudfilen för Streamlit-appen |
| `database.py` | Databasfunktioner |
| `.streamlit/config.toml` | Anpassad konfiguration för Streamlit |
| `/data/database.db` | SQLite-databas som sparar all inmatad data |
| `.gitignore` | Utesluter databasfil från versionshantering |

---

Klar! 🚀  
Vill du även att jag laddar upp en exempel-CSV för testdata eller lägger till möjlighet att importera/exportera bolagsdata?
