import streamlit as st
import requests
import pandas as pd

API_URL = "https://crypto-buying-system.onrender.com"

st.set_page_config(page_title="Crypto Buying System", layout="wide")

# ============================================================
# 🔐 CONTROLE DE LOGIN
# ============================================================

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None


def api_request(method, endpoint, **kwargs):
    url = f"{API_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, **kwargs)
    elif method == "POST":
        response = requests.post(url, **kwargs)
    else:
        raise ValueError("Método não suportado")

    if response.status_code == 401:
        st.warning("Sessão expirada. Faça login novamente.")
        st.session_state.usuario_logado = None
        st.rerun()

    return response


# ============================================================
# 🔐 TELA DE LOGIN
# ============================================================

st.title("📊 Crypto Buying System")

if st.session_state.usuario_logado is None:

    st.subheader("🔐 Login")

    usuario_input = st.text_input("Usuário ID")

    if st.button("Entrar"):
        response = requests.post(f"{API_URL}/login/{usuario_input}")

        if response.status_code == 200:
            st.session_state.usuario_logado = usuario_input
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Erro ao realizar login.")

    st.stop()


# ============================================================
# 🔗 MAPEAMENTO CRIPTOMOEDAS
# ============================================================

MAPA_CRIPTO = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "ADA": "Cardano",
    "SOL": "Solana",
    "HBAR": "Hedera",
    "XRP": "Ripple"
}

# ============================================================
# 📌 SIDEBAR
# ============================================================

st.sidebar.header("🔎 Navegação")
st.sidebar.markdown(f"👤 **Logado como:** {st.session_state.usuario_logado}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.usuario_logado = None
    st.rerun()

pagina = st.sidebar.radio(
    "Escolha:",
    ["Dashboard", "Cadastrar Transação", "Lucro/Prejuízo"]
)

# ============================================================
# 📊 DASHBOARD
# ============================================================

if pagina == "Dashboard":

    st.subheader("📊 Resumo da Carteira")

    response = api_request(
        "GET",
        f"/analytics/resumo/{st.session_state.usuario_logado}"
    )

    if response.status_code == 200:
        data = response.json()

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            st.bar_chart(df.set_index("ticker")["valor_atual"])
        else:
            st.info("Nenhuma posição encontrada.")
    else:
        st.error("Erro ao buscar dados.")


# ============================================================
# ➕ CADASTRAR TRANSAÇÃO
# ============================================================

elif pagina == "Cadastrar Transação":

    st.subheader("➕ Executar Trade")

    tab1, tab2 = st.tabs(["Compra", "Venda"])

    def cadastrar(tipo, ticker, quantidade):

        payload = {
            "usuario_id": st.session_state.usuario_logado,
            "ticker": ticker,
            "tipo": tipo,
            "quantidade": quantidade
        }

        response = api_request(
            "POST",
            "/trade/",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()

            st.success(f"{tipo.capitalize()} executada com sucesso!")

            st.write("🆔 ID da transação:", data["_id"])
            st.write("💰 Preço executado:", f"${data['preco_unitario']:,.2f}")
            st.write("📦 Quantidade:", data["quantidade"])
            st.write("🕒 Timestamp:", data["timestamp"])
        else:
            st.error("Erro ao executar transação.")

    # ---------------- COMPRA ----------------
    with tab1:

        ticker_compra = st.selectbox("Ticker", list(MAPA_CRIPTO.keys()), key="c_ticker")
        quantidade_compra = st.number_input("Quantidade", min_value=0.0, key="c_qtd")

        if st.button("Executar Compra"):
            cadastrar("compra", ticker_compra, quantidade_compra)

    # ---------------- VENDA ----------------
    with tab2:

        ticker_venda = st.selectbox("Ticker", list(MAPA_CRIPTO.keys()), key="v_ticker")
        quantidade_venda = st.number_input("Quantidade", min_value=0.0, key="v_qtd")

        if st.button("Executar Venda"):
            cadastrar("venda", ticker_venda, quantidade_venda)


# ============================================================
# 💰 LUCRO / PREJUÍZO
# ============================================================

# ============================================================
# 💰 LUCRO / PREJUÍZO
# ============================================================

elif pagina == "Lucro/Prejuízo":

    st.subheader("💰 Lucro / Prejuízo (Preço Médio)")

    modo = st.radio(
        "Escolha o modo:",
        ["Geral", "Por Moeda"]
    )

    # ---------------- LUCRO GERAL ----------------
    if modo == "Geral":

        response = api_request(
            "GET",
            f"/analytics/lucro-prejuizo/{st.session_state.usuario_logado}"
        )

        if response.status_code == 200:

            data = response.json()

            if not data["moedas"]:
                st.info("Usuário não possui posições.")
            else:
                df = pd.DataFrame(data["moedas"])
                st.dataframe(df, use_container_width=True)

                st.bar_chart(df.set_index("ticker")["lucro_prejuizo"])

                st.divider()

                total = data["lucro_total"]

                if total >= 0:
                    st.success(f"Lucro Total: ${total:,.2f}")
                else:
                    st.error(f"Prejuízo Total: ${total:,.2f}")

        else:
            st.error("Erro ao calcular lucro/prejuízo.")


    # ---------------- LUCRO POR MOEDA ----------------
    else:

        ticker = st.selectbox("Selecione a moeda", list(MAPA_CRIPTO.keys()))

        response = api_request(
            "GET",
            f"/analytics/lucro-prejuizo/{st.session_state.usuario_logado}",
            params={"ticker": ticker}
        )

        if response.status_code == 200:

            data = response.json()

            if not data:
                st.info("Usuário não possui posição nessa moeda.")
            else:
                st.write("📦 Quantidade Atual:", data["quantidade_atual"])
                st.write("💵 Preço Médio:", f"${data['preco_medio']:,.2f}")
                st.write("📈 Preço Atual:", f"${data['preco_atual']:,.2f}")

                lucro = data["lucro_prejuizo"]

                st.divider()

                if lucro >= 0:
                    st.success(f"Lucro: ${lucro:,.2f}")
                else:
                    st.error(f"Prejuízo: ${lucro:,.2f}")

        else:
            st.error("Erro ao calcular lucro/prejuízo.")