from fastapi import APIRouter
from models.transacao import TransacaoCreate
from services.transacao_service import executar_transacao
from services.binance_service import get_preco_atual

router = APIRouter(prefix="/trade", tags=["Trade"])

@router.post("/")
def trade(transacao: TransacaoCreate):
    return executar_transacao(
        transacao.usuario_id,
        transacao.ticker,
        transacao.tipo,
        transacao.quantidade
    )

@router.get("/preco/{ticker}")
def preco_atual(ticker: str):
    return {
        "ticker": ticker,
        "preco_atual": get_preco_atual(ticker)
    }