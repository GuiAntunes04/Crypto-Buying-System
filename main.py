from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
from database import get_db_client

app = FastAPI(title="Crypto Buying System")

# -------- MODELOS --------

class Localizacao(BaseModel):
    type: str = "Point"
    coordinates: List[float]

class Transacao(BaseModel):
    usuario_id: str
    ativo: str
    ticker: str
    tipo: str
    quantidade: float
    preco_unitario: float
    localizacao: Localizacao


# -------- BANCO (lazy load) --------

def get_collection():
    client = get_db_client()
    if not client:
        raise HTTPException(status_code=500, detail="Erro ao conectar no MongoDB")

    db = client["crypto_db"]
    return db["transacoes"]


# -------- ROTAS --------

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.post("/transacoes/batch")
def inserir_transacoes(transacoes: List[Transacao]):
    try:
        collection = get_collection()

        docs = []
        for t in transacoes:
            doc = t.dict()
            doc["timestamp"] = datetime.utcnow()
            docs.append(doc)

        result = collection.insert_many(docs)
        return {"inseridos": len(result.inserted_ids)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/patrimonio")
def patrimonio():
    try:
        collection = get_collection()

        pipeline = [
    {
        "$project": {
            "ativo": 1,
            "tipo_normalizado": { "$toLower": "$tipo" },
            "valor": {
                "$cond": [
                    { "$eq": [{ "$toLower": "$tipo" }, "compra"] },
                    { "$multiply": ["$quantidade", "$preco_unitario"] },
                    { "$multiply": ["$quantidade", "$preco_unitario", -1] }
                ]
            }
        }
    },
    {
        "$group": {
            "_id": "$ativo",
            "patrimonio_total": { "$sum": "$valor" }
        }
    }
]



        return list(collection.aggregate(pipeline))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/transacoes/usuario/{usuario_id}")
def listar_por_usuario(usuario_id: str):
    collection = get_collection()
    return list(collection.find({"usuario_id": usuario_id}, {"_id": 0}))

@app.delete("/transacoes/usuario/{usuario_id}")
def deletar_usuario(usuario_id: str):
    collection = get_collection()
    result = collection.delete_many({"usuario_id": usuario_id})
    return {"deletados": result.deleted_count}

@app.get("/analytics/usuario")
def patrimonio_por_usuario():
    collection = get_collection()
    pipeline = [
    {
        "$project": {
            "usuario_id": 1,
            "valor": {
                "$cond": [
                    { "$eq": [{ "$toLower": "$tipo" }, "compra"] },
                    { "$multiply": ["$quantidade", "$preco_unitario"] },
                    { "$multiply": ["$quantidade", "$preco_unitario", -1] }
                ]
            }
        }
    },
    {
        "$group": {
            "_id": "$usuario_id",
            "patrimonio": { "$sum": "$valor" }
        }
    }
]

    return list(collection.aggregate(pipeline))

@app.get("/transacoes/busca")
def busca_texto(q: str):
    collection = get_collection()
    return list(collection.find(
        {"$text": {"$search": q}},
        {"_id": 0}
    ))

@app.get("/transacoes/proximas")
def proximas(lat: float, lng: float, km: int = 50):
    collection = get_collection()
    return list(collection.find({
        "localizacao": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "$maxDistance": km * 1000
            }
        }
    }, {"_id": 0}))


