import calendar
import json
from datetime import date

import pandas as pd
import streamlit as st


def moeda(valor):

    return (

        f"R$ {valor:,.2f}"

        .replace(",", "X")

        .replace(".", ",")

        .replace("X", ".")

    )


def inteiro(valor):

    return (

        f"{int(valor):,}"

        .replace(",", ".")

    )


def painel_meta(

    df,

    config,

    CONFIG

):

    st.subheader("🎯 Meta do Mês")

    col_meta, col_barra = st.columns([1, 3])

    with col_meta:

        meta = st.number_input(

            "Meta mensal (R$)",

            min_value=0.0,

            value=float(config["meta_mensal"]),

            step=1000.0,

            format="%.2f"

        )

        if meta != config["meta_mensal"]:

            config["meta_mensal"] = meta

            with open(

                CONFIG,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    config,

                    f,

                    indent=4

                )

        valor_vendido = df["valor_vendido"].sum()

        comissao = df["comissao"].sum()

        pedidos = len(df)

        percentual = (

            (valor_vendido / meta) * 100

            if meta > 0

            else 0

        )

        restante = max(

            meta - valor_vendido,

            0

        )

        ultima_data = df["data"].max().date()

        ultimo_dia = calendar.monthrange(

            ultima_data.year,

            ultima_data.month

        )[1]

        dias_restantes = (

            date(

                ultima_data.year,

                ultima_data.month,

                ultimo_dia

            )

            - ultima_data

        ).days

        media_necessaria = (

            restante / dias_restantes

            if dias_restantes > 0

            else restante

        )

        dia_atual = ultima_data.day

        projecao_comissao = (

            (comissao / dia_atual) * ultimo_dia

            if dia_atual > 0

            else 0

        )

        if percentual >= 150:

            bonus = 3

        elif percentual >= 125:

            bonus = 2

        elif percentual >= 100:

            bonus = 1

        else:

            bonus = 0

    with col_barra:

        st.write("")

        st.write("")

        progresso = min(

            percentual / 150,

            1.0

        )

        st.markdown(

            f"**Progresso da Meta: {percentual:.1f}%**"

        )

        st.progress(

            progresso

        )

    linha1 = st.columns(4)

    linha1[0].metric(

        "🛒 Valor Vendido",

        moeda(valor_vendido)

    )

    linha1[1].metric(

        "💰 Comissão",

        moeda(comissao)

    )

    linha1[2].metric(

        "📦 Pedidos",

        inteiro(pedidos)

    )

    linha1[3].metric(

        "📈 Projeção Comissão",

        moeda(projecao_comissao)

    )

    linha2 = st.columns(4)

    linha2[0].metric(

        "🎯 Meta",

        f"{percentual:.1f}%"

    )

    linha2[1].metric(

        "🏆 Bônus",

        f"{bonus}%"

    )

    linha2[2].metric(

        "📉 Faltam",

        moeda(restante)

    )

    linha2[3].metric(

        "📅 Média diária",

        moeda(media_necessaria)

    )