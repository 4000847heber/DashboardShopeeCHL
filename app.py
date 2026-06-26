import json
import sqlite3

from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(

    page_title="Dashboard Shopee CHL",

    page_icon="📈",

    layout="wide"

)

st.title("📈 Dashboard Shopee CHL")

pagina = st.sidebar.radio(

    "Menu",

    [

        "Dashboard",

        "Atualizar Dados"

    ]

)

if pagina == "Atualizar Dados":

    exec(

        open(

            "pagina_importacao.py",

            encoding="utf-8"

        ).read()

    )

    st.stop()


BASE_DIR = Path(__file__).parent

DB = BASE_DIR / "banco.db"

CONFIG = BASE_DIR / "config.json"


if not DB.exists():

    st.warning(

        "Nenhum dado encontrado.\n\nImporte o primeiro relatório da Shopee."

    )

    st.stop()


with open(

    CONFIG,

    encoding="utf-8"

) as f:

    config = json.load(f)

exec(

    open(

        "dashboard.py",

        encoding="utf-8"

    ).read()

)