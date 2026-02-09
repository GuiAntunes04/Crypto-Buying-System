from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    type: str = "Point"
    coordinates: List[float]

class TransactionIn(BaseModel):
    usuario_id: str
    ativo: str
    ticker: str
    tipo: str
    quantidade: float
    preco_unitario: float
    localizacao: Location
