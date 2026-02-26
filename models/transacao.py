from pydantic import BaseModel
from datetime import datetime

class TransacaoCreate(BaseModel):
    usuario_id: str
    ticker: str
    tipo: str  # compra ou venda
    quantidade: float

class TransacaoDB(BaseModel):
    usuario_id: str
    ticker: str
    tipo: str
    quantidade: float
    preco_unitario: float
    timestamp: datetime