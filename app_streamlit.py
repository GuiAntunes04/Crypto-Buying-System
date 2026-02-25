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
    """
    Função central para requisições protegidas.
    Trata automaticamente sessão expirada.
    """
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
    "ADA": "Cardano"
}

MAPA_REVERSO = {v: k for k, v in MAPA_CRIPTO.items()}

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

    st.subheader("👤 Patrimônio por Usuário")

    response = api_request("GET", "/patrimonio/usuario")

    if response.status_code == 200:
        data = response.json()

        if data:
            df = pd.DataFrame(data)
            df.rename(columns={"_id": "Usuário"}, inplace=True)

            st.dataframe(df, use_container_width=True)

            if "patrimonio" in df.columns:
                st.bar_chart(df.set_index("Usuário")["patrimonio"])
        else:
            st.info("Nenhum dado encontrado.")
    else:
        st.error("Erro ao buscar dados.")


# ============================================================
# ➕ CADASTRAR TRANSAÇÃO
# ============================================================

elif pagina == "Cadastrar Transação":

    st.subheader("➕ Inserir Transação")

    tab1, tab2 = st.tabs(["Compra", "Venda"])

    def cadastrar(tipo):
        payload = [{
            "usuario_id": st.session_state.usuario_logado,
            "ativo": MAPA_CRIPTO[ticker],
            "ticker": ticker,
            "tipo": tipo,
            "quantidade": quantidade,
            "preco_unitario": preco,
            "localizacao": {
                "type": "Point",
                "coordinates": [0, 0]
            }
        }]

        response = api_request(
            "POST",
            "/transacoes/batch",
            json=payload
        )

        if response.status_code == 200:
            st.success(f"{tipo.capitalize()} cadastrada com sucesso!")
        else:
            st.error("Erro ao cadastrar transação.")

    # ---------------- COMPRA ----------------
    with tab1:

        ticker = st.selectbox("Ticker", list(MAPA_CRIPTO.keys()), key="c_ticker")
        quantidade = st.number_input("Quantidade", min_value=0.0, key="c_qtd")
        preco = st.number_input("Preço Unitário", min_value=0.0, key="c_preco")

        if st.button("Cadastrar Compra"):
            cadastrar("compra")

    # ---------------- VENDA ----------------
    with tab2:

        ticker = st.selectbox("Ticker", list(MAPA_CRIPTO.keys()), key="v_ticker")
        quantidade = st.number_input("Quantidade", min_value=0.0, key="v_qtd")
        preco = st.number_input("Preço Unitário", min_value=0.0, key="v_preco")

        if st.button("Cadastrar Venda"):
            cadastrar("venda")


# ============================================================
# 💰 LUCRO / PREJUÍZO
# ============================================================

elif pagina == "Lucro/Prejuízo":

    st.subheader("💰 Calcular Lucro/Prejuízo (FIFO)")

    ticker = st.selectbox("Ticker", list(MAPA_CRIPTO.keys()))
    preco_atual = st.number_input("Preço Atual", min_value=0.0)

    if st.button("Calcular"):

        response = api_request(
            "GET",
            f"/analytics/lucro-prejuizo/usuario/{st.session_state.usuario_logado}",
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