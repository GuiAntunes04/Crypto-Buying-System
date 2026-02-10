import streamlit as st
import requests
import pandas as pd

API_URL = "https://crypto-buying-system.onrender.com"

st.set_page_config(page_title="Crypto Buying System", layout="wide")

st.title("📊 Crypto Buying System – Dashboard")

# -------- SIDEBAR --------
st.sidebar.header("🔎 Navegação")
pagina = st.sidebar.radio(
    "Escolha a visualização:",
    ["Patrimônio Geral", "Patrimônio por Usuário", "Buscar por Usuário"]
)

# -------- PATRIMÔNIO GERAL --------
if pagina == "Patrimônio Geral":
    st.subheader("💰 Patrimônio Total por Ativo")

    response = requests.get(f"{API_URL}/analytics/patrimonio")

    if response.status_code == 200:
        data = response.json()

        if data:
            df = pd.DataFrame(data)
            df.rename(columns={"_id": "Ativo"}, inplace=True)

            st.dataframe(df, use_container_width=True)

            st.bar_chart(
                df.set_index("Ativo")["total_investido"]
            )
        else:
            st.info("Nenhum dado encontrado.")
    else:
        st.error("Erro ao buscar dados da API.")

# -------- PATRIMÔNIO POR USUÁRIO --------
elif pagina == "Patrimônio por Usuário":
    st.subheader("👤 Patrimônio por Usuário")

    response = requests.get(f"{API_URL}/analytics/usuario")

    if response.status_code == 200:
        data = response.json()

        if data:
            df = pd.DataFrame(data)
            df.rename(columns={"_id": "Usuário"}, inplace=True)

            st.dataframe(df, use_container_width=True)

            st.bar_chart(
                df.set_index("Usuário")["total_investido"]
            )
        else:
            st.info("Nenhum dado encontrado.")
    else:
        st.error("Erro ao buscar dados da API.")

# -------- BUSCAR TRANSAÇÕES POR USUÁRIO --------
elif pagina == "Buscar por Usuário":
    st.subheader("📄 Transações por Usuário")

    usuario_id = st.text_input("Digite o ID do usuário:")

    if st.button("Buscar"):
        response = requests.get(f"{API_URL}/transacoes/usuario/{usuario_id}")

        if response.status_code == 200:
            data = response.json()

            if data:
                df = pd.DataFrame(data)
                df.drop(columns=["_id"], errors="ignore", inplace=True)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhuma transação encontrada.")
        else:
            st.error("Erro ao consultar usuário.")
