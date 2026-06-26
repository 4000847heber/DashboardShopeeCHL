import sqlite3

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).parent

DB = BASE_DIR / "banco.db"


def carregar_dados():

    con = sqlite3.connect(DB)

    df = pd.read_sql(

        "SELECT * FROM shopee",

        con

    )

    con.close()

    df["data"] = pd.to_datetime(

        df["data"]

    ).dt.normalize()

    return df