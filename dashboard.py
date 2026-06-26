import streamlit as st
import sqlite3

from pathlib import Path

import pandas as pd
import json
from painel_meta import painel_meta
from painel_destaques import painel_destaques
from painel_rankings import painel_rankings
from painel_grafico import painel_grafico

BASE_DIR = Path(__file__).parent

DB = BASE_DIR / "banco.db"

CONFIG = BASE_DIR / "config.json"


with open(

    CONFIG,

    encoding="utf-8"

) as f:

    config = json.load(f)


con = sqlite3.connect(DB)

df = pd.read_sql(

    "SELECT * FROM shopee",

    con

)

con.close()


df["data"] = pd.to_datetime(

    df["data"]

).dt.normalize()


ultima_data = df["data"].max().date()


tipo_periodo = st.sidebar.radio(

    "Período",

    [

        "Hoje",

        "Mês Atual",

        "Personalizado"

    ]

)


if tipo_periodo == "Hoje":

    data_inicial = ultima_data

    data_final = ultima_data


elif tipo_periodo == "Mês Atual":

    data_inicial = ultima_data.replace(

        day=1

    )

    data_final = ultima_data


else:

    data_inicial = st.sidebar.date_input(

        "Data inicial",

        ultima_data.replace(day=1)

    )

    data_final = st.sidebar.date_input(

        "Data final",

        ultima_data

    )


df = df[

    (df["data"] >= pd.to_datetime(data_inicial))

    &

    (df["data"] <= pd.to_datetime(data_final))

]


painel_meta(

    df,

    config,

    CONFIG

)

painel_destaques(

    df

)

painel_rankings(

    df

)

painel_grafico(

    df,

    config["meta_mensal"]

)