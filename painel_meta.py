import calendar
import json
from datetime import date

import pandas as pd
import streamlit as st


def moeda(valor):

    if abs(valor) >= 1_000_000:

        return (

            f"R$ {valor / 1_000_000:.2f} mi"

            .replace(".", ",")

        )

    if abs(valor) >= 100_000:

        return (

            f"R$ {valor / 1_000:.1f} mil"

            .replace(".", ",")

        )

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


def card(titulo, valor):

    st.markdown(

        f"""
        <div style="
            border:1px solid rgba(128,128,128,.25);
            border-radius:12px;
            padding:14px;
            min-height:95px;
            margin-bottom:10px;
        ">
            <div style="
                font-size:14px;
                opacity:.75;
                margin-bottom:8px;
            ">
                {titulo}
            </div>

            <div style="
                font-size:clamp(18px,2vw,32px);
                font-weight:700;
                line-height:1.15;
                word-break:break-word;
            ">
                {valor}
            </div>
        </div>
        """,

        unsafe_allow_html=True

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

        bonus_estimado = valor_vendido * (bonus / 100)

    with col_barra:

        st.write("")
        st.write("")

        col_prog, col_bonus = st.columns([3, 1])

        with col_prog:

            st.markdown(

                f"**Progresso da Meta: {percentual:.1f}%**"

            )

            st.progress(

                min(percentual / 150, 1.0)

            )

        with col_bonus:

            st.markdown("**🏆 Bônus Estimado**")

            st.markdown(

                f"### {moeda(bonus_estimado)}"

            )

    linha1 = st.columns(4)

    with linha1[0]:

        card(

            "🛒 Valor Vendido",

            moeda(valor_vendido)

        )

    with linha1[1]:

        card(

            "💰 Comissão",

            moeda(comissao)

        )

    with linha1[2]:

        card(

            "📦 Pedidos",

            inteiro(pedidos)

        )

    with linha1[3]:

        card(

            "📈 Projeção Comissão",

            moeda(projecao_comissao)

        )

    linha2 = st.columns(4)

    with linha2[0]:

        card(

            "🎯 Meta",

            f"{percentual:.1f}%"

        )

    with linha2[1]:

        card(

            "🏆 Bônus",

            f"{bonus}%"

        )

    with linha2[2]:

        card(

            "📉 Faltam",

            moeda(restante)

        )

    with linha2[3]:

        card(

            "📅 Média diária",

            moeda(media_necessaria)

        )