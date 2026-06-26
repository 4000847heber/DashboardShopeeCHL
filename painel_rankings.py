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


def painel_rankings(df):

    st.subheader("📊 Rankings")

    if df.empty:

        st.info("Sem dados.")

        return

    top_vendas = (

        df

        .groupby(

            "produto",

            as_index=False

        )

        .size()

        .rename(

            columns={

                "produto": "Produto",

                "size": "Pedidos"

            }

        )

        .sort_values(

            "Pedidos",

            ascending=False

        )

        .head(10)

    )

    top_vendas["Pedidos"] = top_vendas["Pedidos"].map(inteiro)

    top_comissao = (

        df

        .groupby(

            "produto",

            as_index=False

        )["comissao"]

        .sum()

        .rename(

            columns={

                "produto": "Produto",

                "comissao": "Comissão"

            }

        )

        .sort_values(

            "Comissão",

            ascending=False

        )

        .head(10)

    )

    top_comissao["Comissão"] = top_comissao["Comissão"].map(moeda)

    top_subid = (

        df[

            df["sub_id"].fillna("") != ""

        ]

        .groupby(

            "sub_id",

            as_index=False

        )

        .agg(

            Pedidos=("sub_id", "size"),

            Valor=("valor_vendido", "sum")

        )

        .rename(

            columns={

                "sub_id": "Sub_ID"

            }

        )

        .sort_values(

            "Pedidos",

            ascending=False

        )

        .head(10)

    )

    top_subid["Pedidos"] = top_subid["Pedidos"].map(inteiro)

    top_subid["Valor"] = top_subid["Valor"].map(moeda)

    top_cookies = (

        df[

            df["sub_id"].fillna("") == ""

        ]

        .groupby(

            "produto",

            as_index=False

        )

        .size()

        .rename(

            columns={

                "produto": "Produto",

                "size": "Pedidos"

            }

        )

        .sort_values(

            "Pedidos",

            ascending=False

        )

        .head(10)

    )

    top_cookies["Pedidos"] = top_cookies["Pedidos"].map(inteiro)

    with st.expander(

        "🏆 Top Vendas",

        expanded=True

    ):

        st.dataframe(

            top_vendas[

                [

                    "Pedidos",

                    "Produto"

                ]

            ],

            hide_index=True,

            use_container_width=True

        )

    with st.expander(

        "💰 Top Comissão"

    ):

        st.dataframe(

            top_comissao[

                [

                    "Comissão",

                    "Produto"

                ]

            ],

            hide_index=True,

            use_container_width=True

        )

    with st.expander(

        "🚀 Top Sub_ID"

    ):

        st.dataframe(

            top_subid[

                [

                    "Pedidos",

                    "Sub_ID",

                    "Valor"

                ]

            ],

            hide_index=True,

            use_container_width=True

        )

    with st.expander(

        "🍪 Top Cookies"

    ):

        st.dataframe(

            top_cookies[

                [

                    "Pedidos",

                    "Produto"

                ]

            ],

            hide_index=True,

            use_container_width=True

        )