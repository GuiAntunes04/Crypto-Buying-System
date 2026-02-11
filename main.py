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

# ------------ ÍNDICES ---------------

def criar_indices():
    collection = get_collection()

    # Índice composto (usuario + ticker)
    collection.create_index(
        [("usuario_id", 1), ("ticker", 1)]
    )

    # Índice geoespacial
    collection.create_index(
        [("localizacao", "2dsphere")]
    )

    # Índice de texto
    collection.create_index(
        [
            ("usuario_id", "text"),
            ("ativo", "text"),
            ("ticker", "text")
        ]
    )


@app.on_event("startup")
def startup_event():
    criar_indices()


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
    
@app.post("/seed")
def popular_base():
    try:
        collection = get_collection()

        collection.delete_many({})

        dados_json = [
            {
                "usuario_id": "user1",
                "ativo": "Bitcoin",
                "ticker": "BTC",
                "tipo": "compra",
                "quantidade": 0.5,
                "preco_unitario": 30000,
                "localizacao": {
                    "type": "Point",
                    "coordinates": [-46.6333, -23.5505]
                },
                "timestamp": datetime.utcnow()
            },
            {
                "usuario_id": "user1",
                "ativo": "Bitcoin",
                "ticker": "BTC",
                "tipo": "venda",
                "quantidade": 0.2,
                "preco_unitario": 35000,
                "localizacao": {
                    "type": "Point",
                    "coordinates": [-46.6333, -23.5505]
                },
                "timestamp": datetime.utcnow()
            },
            {
                "usuario_id": "user2",
                "ativo": "Ethereum",
                "ticker": "ETH",
                "tipo": "compra",
                "quantidade": 2,
                "preco_unitario": 2000,
                "localizacao": {
                    "type": "Point",
                    "coordinates": [-43.2096, -22.9035]
                },
                "timestamp": datetime.utcnow()
            },
            {
                "usuario_id": "user2",
                "ativo": "Ethereum",
                "ticker": "ETH",
                "tipo": "compra",
                "quantidade": 1,
                "preco_unitario": 2500,
                "localizacao": {
                    "type": "Point",
                    "coordinates": [-43.2096, -22.9035]
                },
                "timestamp": datetime.utcnow()
            },
            {
                "usuario_id": "user3",
                "ativo": "Cardano",
                "ticker": "ADA",
                "tipo": "compra",
                "quantidade": 1000,
                "preco_unitario": 0.50,
                "localizacao": {
                    "type": "Point",
                    "coordinates": [-51.2300, -30.0331]
                },
                "timestamp": datetime.utcnow()
            }
        ]

        result = collection.insert_many(dados_json)

        return {
            "mensagem": "Base populada com sucesso",
            "total_inserido": len(result.inserted_ids)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/lucro-prejuizo/usuario/{usuario_id}")
def lucro_prejuizo_usuario(usuario_id: str, ticker: str, preco_atual: float):
    try:
        collection = get_collection()

        transacoes = list(collection.find(
            {
                "usuario_id": usuario_id,
                "ticker": ticker
            },
            {"_id": 0}
        ).sort("timestamp", 1))

        if not transacoes:
            return {
                "usuario_id": usuario_id,
                "ticker": ticker,
                "lucro_prejuizo": None
            }

        fila = []

        for t in transacoes:
            tipo = t["tipo"].lower()

            if tipo == "compra":
                fila.append({
                    "quantidade": t["quantidade"],
                    "preco": t["preco_unitario"]
                })

            elif tipo == "venda":
                qtd_venda = t["quantidade"]

                while qtd_venda > 0 and fila:
                    lote = fila[0]

                    if lote["quantidade"] <= qtd_venda:
                        qtd_venda -= lote["quantidade"]
                        fila.pop(0)
                    else:
                        lote["quantidade"] -= qtd_venda
                        qtd_venda = 0

        # Se não sobrou nada
        if not fila:
            return {
                "usuario_id": usuario_id,
                "ticker": ticker,
                "lucro_prejuizo": None
            }

        lucro_total = 0

        for lote in fila:
            lucro_total += (preco_atual - lote["preco"]) * lote["quantidade"]

        return {
            "usuario_id": usuario_id,
            "ticker": ticker,
            "lucro_prejuizo": lucro_total
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
@app.get("/transacoes/usuario/{usuario_id}")
def listar_por_usuario(usuario_id: str):
    collection = get_collection()
    return list(collection.find({"usuario_id": usuario_id}, {"_id": 0}))


@app.get("/patrimonio/usuario")
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

@app.get("/analytics/ativo-resumo")
def resumo_por_ativo():
    try:
        collection = get_collection()

        pipeline = [
            {
                "$project": {
                    "ticker": 1,
                    "quantidade_compra": {
                        "$cond": [
                            { "$eq": [{ "$toLower": "$tipo" }, "compra"] },
                            "$quantidade",
                            0
                        ]
                    },
                    "quantidade_venda": {
                        "$cond": [
                            { "$eq": [{ "$toLower": "$tipo" }, "venda"] },
                            "$quantidade",
                            0
                        ]
                    },
                    "valor_movimentado": {
                        "$multiply": ["$quantidade", "$preco_unitario"]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$ticker",
                    "total_comprado": { "$sum": "$quantidade_compra" },
                    "total_vendido": { "$sum": "$quantidade_venda" },
                    "volume_financeiro": { "$sum": "$valor_movimentado" }
                }
            },
            {
                "$project": {
                    "ticker": "$_id",
                    "total_comprado": 1,
                    "total_vendido": 1,
                    "saldo_atual": {
                        "$subtract": ["$total_comprado", "$total_vendido"]
                    },
                    "volume_financeiro": 1,
                    "_id": 0
                }
            }
        ]

        return list(collection.aggregate(pipeline))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

@app.delete("/transacoes/usuario/{usuario_id}")
def deletar_usuario(usuario_id: str):
    collection = get_collection()
    result = collection.delete_many({"usuario_id": usuario_id})
    return {"deletados": result.deleted_count}


