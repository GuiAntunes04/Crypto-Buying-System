from fastapi import APIRouter
from connections.redis_client import get_redis_client
from fastapi.responses import RedirectResponse
from redis_structures.hyperlog import add_user

router = APIRouter(tags=["Auth"])

SESSION_TTL = 60

@router.post("/login/{usuario_id}")
def login(usuario_id: str):

    redis = get_redis_client()

    # cria sessão
    redis.set(f"sessao:{usuario_id}", "ativa", ex=SESSION_TTL)

    # registra usuário único do dia
    add_user(usuario_id)

    return {"mensagem": "Sessão iniciada"}


@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")