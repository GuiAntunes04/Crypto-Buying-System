from fastapi import APIRouter
from services.analytics_service import calcular_lucro_prejuizo, get_resumo_usuario
from typing import Optional

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/resumo/{usuario_id}")
def resumo_usuario(usuario_id: str):
    return get_resumo_usuario(usuario_id)

@router.get("/lucro-prejuizo/{usuario_id}")
def lucro_prejuizo(usuario_id: str, ticker: Optional[str] = None):
    return calcular_lucro_prejuizo(usuario_id, ticker)



