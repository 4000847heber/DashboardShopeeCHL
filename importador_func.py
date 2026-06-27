import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).parent
DB = BASE_DIR / "banco.db"


def criar_banco():

    con = sqlite3.connect(DB)

    con.execute("""
        CREATE TABLE IF NOT EXISTS shopee(

            data TEXT,
            pedido TEXT,
            produto TEXT,
            sub_id TEXT,
            canal TEXT,
            status TEXT,
            valor_vendido REAL,
            comissao REAL

        )
    """)

    con.commit()
    con.close()


def importar(shopee_file):

    criar_banco()

    con = sqlite3.connect(DB)

    try:

        df = pd.read_csv(
            shopee_file,
            encoding="utf-8-sig"
        )

    except:

        df = pd.read_csv(
            shopee_file,
            encoding="latin1"
        )

    colunas = [

        "Horário do pedido",
        "ID do pedido",
        "Nome do Item",
        "Sub_id1",
        "Canal",
        "Status do Pedido",
        "Valor de Compra(R$)",
        "Comissão líquida do afiliado(R$)"

    ]

    for coluna in colunas:

        if coluna not in df.columns:

            raise Exception(

                f"""
Coluna não encontrada:

{coluna}

Colunas encontradas:

{list(df.columns)}
"""

            )

    df = df.rename(columns={

        "Horário do pedido": "data",
        "ID do pedido": "pedido",
        "Nome do Item": "produto",
        "Categoria Principal": "categoria",
        "Sub_id1": "sub_id",
        "Canal": "canal",
        "Status do Pedido": "status",
        "Valor de Compra(R$)": "valor_vendido",
        "Comissão líquida do afiliado(R$)": "comissao"

    })

    df = df[
        df["status"].isin([
            "Pendente",
            "Concluído"
        ])
    ].copy()

    df["data"] = pd.to_datetime(
        df["data"]
    ).dt.normalize()

    df = df[
        [
            "data",
            "pedido",
            "produto",
            "sub_id",
            "canal",
            "status",
            "valor_vendido",
            "comissao"
        ]
    ]

    df = (

        df

        .groupby(

            "pedido",

            as_index=False

        )

        .agg(

            data=("data", "first"),

            produto=("produto", "first"),

            sub_id=("sub_id", "first"),

            canal=("canal", "first"),

            status=("status", "first"),

            valor_vendido=("valor_vendido", "sum"),

            comissao=("comissao", "sum")

        )

    )

    datas = (
        df["data"]
        .dt.strftime("%Y-%m-%d")
        .unique()
    )

    cur = con.cursor()

    for data in datas:

        cur.execute(
            "DELETE FROM shopee WHERE data=?",
            (data,)
        )

    df["data"] = df["data"].dt.strftime("%Y-%m-%d")

    df.to_sql(
        "shopee",
        con,
        if_exists="append",
        index=False
    )

    con.commit()
    con.close()

    return {

        "ultima_data": pd.to_datetime(df["data"]).max().strftime("%d/%m/%Y"),
        "linhas": len(df)

    }