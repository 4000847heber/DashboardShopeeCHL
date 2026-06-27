import streamlit as st


def moeda(valor):

    return (

        f"R$ {valor:,.2f}"

        .replace(",", "X")

        .replace(".", ",")

        .replace("X", ".")

    )


def resumir(texto, limite=42):

    texto = str(texto)

    if len(texto) <= limite:

        return texto

    return texto[:limite].rstrip() + "..."


def painel_destaques(df):

    st.subheader("🏆 Destaques")

    if df.empty:

        st.info("Sem dados.")

        return

    produto = (

        df

        .groupby("produto", as_index=False)

        .size()

        .sort_values("size", ascending=False)

        .iloc[0]

    )

    sub = (

        df[
            df["sub_id"].fillna("") != ""
        ]

        .groupby("sub_id", as_index=False)

        .agg(

            Pedidos=("sub_id", "size"),

            Comissao=("comissao", "sum")

        )

        .sort_values("Pedidos", ascending=False)

        .iloc[0]

    )

    cookies = (

        df[
            df["sub_id"].fillna("") == ""
        ]

        .groupby("produto", as_index=False)

        .size()

        .sort_values("size", ascending=False)

        .iloc[0]

    )

    rentavel = (

        df

        .groupby("produto", as_index=False)["comissao"]

        .sum()

        .sort_values("comissao", ascending=False)

        .iloc[0]

    )

    c1, c2 = st.columns(2)

    c3, c4 = st.columns(2)

    with c1:

        st.markdown("##### 🏆 Produto campeão")

        st.markdown(

            f"<div style='font-size:18px;font-weight:600'>{resumir(produto['produto'])}</div>",

            unsafe_allow_html=True

        )

        st.caption(

            f"{produto['size']} pedidos"

        )

    with c2:

        st.markdown("##### 🚀 Melhor Sub_ID")

        st.markdown(

            f"<div style='font-size:18px;font-weight:600'>{sub['sub_id']}</div>",

            unsafe_allow_html=True

        )

        st.caption(

            f"{inteiro(sub['Pedidos'])} pedidos • {moeda(sub['Comissao'])}"

        )

    with c3:

        st.markdown("##### 🍪 Campeão Cookies")

        st.markdown(

            f"<div style='font-size:18px;font-weight:600'>{resumir(cookies['produto'])}</div>",

            unsafe_allow_html=True

        )

        st.caption(

            f"{cookies['size']} pedidos"

        )

    with c4:

        st.markdown("##### 💰 Mais rentável")

        st.markdown(

            f"<div style='font-size:18px;font-weight:600'>{resumir(rentavel['produto'])}</div>",

            unsafe_allow_html=True

        )

        st.caption(

            moeda(rentavel["comissao"])

        )


def inteiro(valor):

    return (

        f"{int(valor):,}"

        .replace(",", ".")

    )