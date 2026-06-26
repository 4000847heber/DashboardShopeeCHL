import calendar

import pandas as pd

import plotly.graph_objects as go

import streamlit as st


def moeda(valor):

    return (

        f"R$ {valor:,.2f}"

        .replace(",", "X")

        .replace(".", ",")

        .replace("X", ".")

    )


def painel_grafico(

    df,

    meta

):

    st.subheader(

        "📈 Meta × Realizado"

    )

    if df.empty or meta <= 0:

        st.info(

            "Defina uma meta mensal para visualizar o gráfico."

        )

        return

    dados = (

        df

        .groupby(

            "data",

            as_index=False

        )["valor_vendido"]

        .sum()

        .sort_values(

            "data"

        )

    )

    dados["Realizado"] = dados["valor_vendido"].cumsum()

    ultima = dados["data"].max()

    dias_mes = calendar.monthrange(

        ultima.year,

        ultima.month

    )[1]

    meta_dia = meta / dias_mes

    dados["Meta"] = [

        meta_dia * (i + 1)

        for i in range(

            len(dados)

        )

    ]

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=dados["data"],

            y=dados["Meta"],

            mode="lines",

            name="🎯 Meta",

            line=dict(

                color="#1f77b4",

                width=3,

                dash="dash"

            )

        )

    )

    fig.add_trace(

        go.Scatter(

            x=dados["data"],

            y=dados["Realizado"],

            mode="lines+markers",

            name="🛒 Realizado",

            line=dict(

                color="#d62728",

                width=4

            )

        )

    )

    fig.update_layout(

        height=480,

        legend_title="",

        hovermode="x unified",

        margin=dict(

            l=10,

            r=10,

            t=20,

            b=10

        ),

        yaxis=dict(

            tickprefix="R$ ",

            separatethousands=True

        )

    )

    fig.update_yaxes(

        tickformat=",.0f"

    )

    fig.update_traces(

        hovertemplate="R$ %{y:,.2f}<extra></extra>"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )