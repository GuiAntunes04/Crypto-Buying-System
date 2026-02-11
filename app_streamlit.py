import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Crypto Buying System", layout="wide")

st.title("📊 Crypto Buying System – Dashboard")

# ============================================================
# 🔗 MAPEAMENTO CRIPTOMOEDAS
# ============================================================

MAPA_CRIPTO = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "ADA": "Cardano"
}

MAPA_REVERSO = {v: k for k, v in MAPA_CRIPTO.items()}

# ============================================================
# 📌 SIDEBAR
# ============================================================

st.sidebar.header("🔎 Navegação")

pagina = st.sidebar.radio(
    "Escolha:",
    ["Dashboard", "Cadastrar Transação", "Lucro/Prejuízo"]
)

# ============================================================
# 📊 DASHBOARD
# ============================================================

if pagina == "Dashboard":

    st.subheader("👤 Patrimônio por Usuário")

    response = requests.get(f"{API_URL}/analytics/usuario")

    if response.status_code == 200:
        data = response.json()

        if data:
            df = pd.DataFrame(data)
            df.rename(columns={"_id": "Usuário"}, inplace=True)

            st.dataframe(df, use_container_width=True)

            if "patrimonio" in df.columns:
                st.bar_chart(
                    df.set_index("Usuário")["patrimonio"]
                )
        else:
            st.info("Nenhum dado encontrado.")
    else:
        st.error("Erro ao buscar dados da API.")


# ============================================================
# ➕ CADASTRAR TRANSAÇÃO
# ============================================================

elif pagina == "Cadastrar Transação":

    st.subheader("➕ Inserir Transação")

    tab1, tab2 = st.tabs(["Compra", "Venda"])

    # ---------------- COMPRA ----------------
    with tab1:
        st.subheader("🟢 Cadastrar Compra")

        # Inicialização segura
        if "c_ticker" not in st.session_state:
            st.session_state.c_ticker = "BTC"

        if "c_ativo" not in st.session_state:
            st.session_state.c_ativo = MAPA_CRIPTO[st.session_state.c_ticker]


        def atualizar_ativo():
            st.session_state.c_ativo = MAPA_CRIPTO[st.session_state.c_ticker]


        def atualizar_ticker():
            st.session_state.c_ticker = MAPA_REVERSO[st.session_state.c_ativo]


        usuario = st.text_input("Usuário ID", key="c_usuario")

        col1, col2 = st.columns(2)

        with col1:
            st.selectbox(
                "Ticker",
                options=list(MAPA_CRIPTO.keys()),
                key="c_ticker",
                on_change=atualizar_ativo
            )

        with col2:
            st.selectbox(
                "Ativo",
                options=list(MAPA_CRIPTO.values()),
                key="c_ativo",
                on_change=atualizar_ticker
            )

        quantidade = st.number_input("Quantidade", min_value=0.0, key="c_qtd")
        preco = st.number_input("Preço Unitário", min_value=0.0, key="c_preco")


        if st.button("Cadastrar Compra"):
            payload = [{
                "usuario_id": usuario,
                "ativo": st.session_state["c_ativo"],
                "ticker": st.session_state["c_ticker"],
                "tipo": "compra",
                "quantidade": quantidade,
                "preco_unitario": preco,
                "localizacao": {
                    "type": "Point",
                    "coordinates": [0, 0]
                }
            }]

            response = requests.post(
                f"{API_URL}/transacoes/batch",
                json=payload
            )

            if response.status_code == 200:
                st.success("Compra cadastrada com sucesso!")
            else:
                st.error("Erro ao cadastrar compra.")

    # ---------------- VENDA ----------------
    with tab2:
        st.subheader("🔴 Cadastrar Venda")

        if "v_ticker" not in st.session_state:
            st.session_state.v_ticker = "BTC"

        if "v_ativo" not in st.session_state:
            st.session_state.v_ativo = MAPA_CRIPTO[st.session_state.v_ticker]


        def atualizar_ativo_v():
            st.session_state.v_ativo = MAPA_CRIPTO[st.session_state.v_ticker]


        def atualizar_ticker_v():
            st.session_state.v_ticker = MAPA_REVERSO[st.session_state.v_ativo]


        usuario = st.text_input("Usuário ID", key="v_usuario")

        col1, col2 = st.columns(2)

        with col1:
            st.selectbox(
                "Ticker",
                options=list(MAPA_CRIPTO.keys()),
                key="v_ticker",
                on_change=atualizar_ativo_v
            )

        with col2:
            st.selectbox(
                "Ativo",
                options=list(MAPA_CRIPTO.values()),
                key="v_ativo",
                on_change=atualizar_ticker_v
            )

        quantidade = st.number_input("Quantidade", min_value=0.0, key="v_qtd")
        preco = st.number_input("Preço Unitário", min_value=0.0, key="v_preco")


        if st.button("Cadastrar Venda"):
            payload = [{
                "usuario_id": usuario,
                "ativo": st.session_state["v_ativo"],
                "ticker": st.session_state["v_ticker"],
                "tipo": "venda",
                "quantidade": quantidade,
                "preco_unitario": preco,
                "localizacao": {
                    "type": "Point",
                    "coordinates": [0, 0]
                }
            }]

            response = requests.post(
                f"{API_URL}/transacoes/batch",
                json=payload
            )

            if response.status_code == 200:
                st.success("Venda cadastrada com sucesso!")
            else:
                st.error("Erro ao cadastrar venda.")


# ============================================================
# 💰 LUCRO / PREJUÍZO (FIFO POR TICKER)
# ============================================================

elif pagina == "Lucro/Prejuízo":

    st.subheader("💰 Calcular Lucro/Prejuízo (Modelo FIFO)")

    usuario = st.text_input("Usuário ID")

    ticker = st.selectbox(
        "Ticker",
        options=list(MAPA_CRIPTO.keys())
    )

    preco_atual = st.number_input(
        "Preço Atual da Criptomoeda",
        min_value=0.0
    )

    if st.button("Calcular"):
        response = requests.get(
            f"{API_URL}/analytics/lucro-prejuizo/usuario/{usuario}",
            params={
                "ticker": ticker,
                "preco_atual": preco_atual
            }
        )

        if response.status_code == 200:
            data = response.json()

            if data["lucro_prejuizo"] is None:
                st.warning("Usuário não possui saldo dessa criptomoeda.")
            else:
                valor = data["lucro_prejuizo"]

                if valor >= 0:
                    st.success(f"Lucro: ${valor:,.2f}")
                else:
                    st.error(f"Prejuízo: ${valor:,.2f}")

        else:
            st.error("Erro ao calcular lucro/prejuízo.")
