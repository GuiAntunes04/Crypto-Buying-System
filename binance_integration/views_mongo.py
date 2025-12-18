from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .mongo import market_logs
from datetime import datetime
from bson import ObjectId

class MongoMarketLogView(APIView):
    permission_classes = [IsAuthenticated]

    # CREATE: Salva um log de monitoramento de preço
    def post(self, request):
        data = {
            "user_id": request.user.id,
            "symbol": request.data.get("symbol"),
            "price": request.data.get("price"),
            "note": request.data.get("note", ""), # Campo extra para update
            "created_at": datetime.utcnow()
        }
        result = market_logs.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return Response(data, status=status.HTTP_201_CREATED)

    # READ: Lista apenas os logs do usuário autenticado
    def get(self, request):
        logs = []
        for doc in market_logs.find({"user_id": request.user.id}):
            doc["_id"] = str(doc["_id"])
            logs.append(doc)
        return Response(logs)

    # UPDATE: Atualiza uma nota ou preço de um log específico
    def put(self, request):
        log_id = request.data.get("id")
        if not log_id:
            return Response({"error": "ID é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        # Garante que o usuário só edite o que é dele
        query = {"_id": ObjectId(log_id), "user_id": request.user.id}
        update_data = {
            "$set": {
                "price": request.data.get("price"),
                "note": request.data.get("note"),
                "updated_at": datetime.utcnow()
            }
        }
        
        result = market_logs.update_one(query, update_data)
        
        if result.matched_count == 0:
            return Response({"error": "Log não encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({"message": "Log atualizado com sucesso"})

    # DELETE: Remove um log específico
    def delete(self, request):
        log_id = request.data.get("id")
        if not log_id:
            return Response({"error": "ID é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        # Garante que o usuário só delete o que é dele
        query = {"_id": ObjectId(log_id), "user_id": request.user.id}
        result = market_logs.delete_one(query)

        if result.deleted_count == 0:
            return Response({"error": "Documento não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Log atualizado com sucesso"}, status=status.HTTP_204_NO_CONTENT)