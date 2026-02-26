from fastapi import APIRouter
from connections.redis_client import get_redis_client
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["Auth"])

SESSION_TTL = 60

@router.post("/login/{usuario_id}")
def login(usuario_id: str):
    redis = get_redis_client()
    redis.set(f"sessao:{usuario_id}", "ativa", ex=SESSION_TTL)

    return {"mensagem": "Sessão iniciada"}

@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

