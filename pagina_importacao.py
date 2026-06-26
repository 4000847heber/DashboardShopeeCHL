from pathlib import Path

import streamlit as st

from importador_func import importar


BASE_DIR = Path(__file__).parent

DB = BASE_DIR / "banco.db"


st.title("📥 Atualizar Dados")

shopee = st.file_uploader(

    "Relatório da Shopee",

    type=["csv"]

)

col1, col2 = st.columns(2)

with col1:

    if st.button("📥 Importar"):

        if shopee is None:

            st.error(

                "Selecione o relatório da Shopee."

            )

            st.stop()

        with st.spinner("Importando..."):

            resultado = importar(

                shopee

            )

        st.success(

            "Importação concluída."

        )

        st.info(

            f"""
Última data importada: {resultado['ultima_data']}

Pedidos importados: {resultado['linhas']}
"""

        )

with col2:

    if st.button(

        "🗑 Zerar Banco de Dados",

        type="secondary"

    ):

        if DB.exists():

            DB.unlink()

            st.success(

                "Banco de dados apagado com sucesso."

            )

            st.rerun()

        else:

            st.info(

                "O banco já está vazio."

            )