from services.transacao_service import get_collection
from services.binance_service import get_preco_atual
from collections import defaultdict
from typing import Optional

def calcular_lucro_prejuizo(usuario_id: str, ticker: Optional[str] = None):

    collection = get_collection()

    # 🔹 Se for individual
    if ticker:
        transacoes = list(collection.find(
            {"usuario_id": usuario_id, "ticker": ticker}
        ))

        if not transacoes:
            return None

        total_qtd = 0
        custo_total = 0

        for t in transacoes:
            qtd = t["quantidade"]
            preco = t["preco_unitario"]

            if t["tipo"] == "compra":
                total_qtd += qtd
                custo_total += qtd * preco
            else:
                total_qtd -= qtd
                custo_total -= qtd * preco

        if total_qtd <= 0:
            return None

        preco_medio = custo_total / total_qtd
        preco_atual = get_preco_atual(ticker)

        lucro = (preco_atual - preco_medio) * total_qtd

        return {
            "usuario_id": usuario_id,
            "ticker": ticker,
            "quantidade_atual": total_qtd,
            "preco_medio": round(preco_medio, 2),
            "preco_atual": round(preco_atual, 2),
            "lucro_prejuizo": round(lucro, 2)
        }

    # 🔹 Se for geral
    transacoes = list(collection.find({"usuario_id": usuario_id}))

    if not transacoes:
        return {"moedas": [], "lucro_total": 0}

    dados = defaultdict(lambda: {
        "quantidade": 0,
        "custo_total": 0
    })

    for t in transacoes:
        ticker_db = t["ticker"]
        qtd = t["quantidade"]
        preco = t["preco_unitario"]

        if t["tipo"] == "compra":
            dados[ticker_db]["quantidade"] += qtd
            dados[ticker_db]["custo_total"] += qtd * preco
        else:
            dados[ticker_db]["quantidade"] -= qtd
            dados[ticker_db]["custo_total"] -= qtd * preco

    moedas = []
    lucro_total = 0

    for ticker_db, info in dados.items():

        if info["quantidade"] <= 0:
            continue

        preco_medio = info["custo_total"] / info["quantidade"]
        preco_atual = get_preco_atual(ticker_db)

        lucro = (preco_atual - preco_medio) * info["quantidade"]
        lucro_total += lucro

        moedas.append({
            "ticker": ticker_db,
            "lucro_prejuizo": round(lucro, 2)
        })

    return {
        "moedas": moedas,
        "lucro_total": round(lucro_total, 2)
    }

def get_resumo_usuario(usuario_id: str):

    collection = get_collection()
    transacoes = list(collection.find({"usuario_id": usuario_id}))

    if not transacoes:
        return []

    dados = defaultdict(lambda: {
        "quantidade": 0,
        "custo_total": 0
    })

    # 🔹 Calcula posição líquida e custo
    for t in transacoes:
        ticker = t["ticker"]
        qtd = t["quantidade"]
        preco = t["preco_unitario"]

        if t["tipo"] == "compra":
            dados[ticker]["quantidade"] += qtd
            dados[ticker]["custo_total"] += qtd * preco
        else:
            dados[ticker]["quantidade"] -= qtd
            dados[ticker]["custo_total"] -= qtd * preco

    resultado = []

    for ticker, info in dados.items():

        if info["quantidade"] <= 0:
            continue

        preco_medio = info["custo_total"] / info["quantidade"]
        preco_atual = get_preco_atual(ticker)

        resultado.append({
            "ticker": ticker,
            "quantidade": info["quantidade"],
            "preco_medio": round(preco_medio, 2),
            "preco_atual": round(preco_atual, 2),
            "valor_atual": round(info["quantidade"] * preco_atual, 2)
        })

    return resultado

