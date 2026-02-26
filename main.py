from fastapi import FastAPI
from routes import trade_routes, analytics_routes, auth_routes

app = FastAPI(title="Crypto Trading System")

app.include_router(auth_routes.router)
app.include_router(trade_routes.router)
app.include_router(analytics_routes.router)