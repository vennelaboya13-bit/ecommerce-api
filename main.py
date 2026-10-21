from fastapi import FastAPI
from app.database import Base, engine

# Import models before creating database tables
from app import models

# Import routers
from app.auth import router as auth_router
from app.products import router as products_router
from app.cart import router as cart_router
from app.orders import router as orders_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce REST API",
    description="E-commerce API built using Python, FastAPI, and MySQL",
    version="1.0.0"
)

# Register routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)


@app.get("/")
def home():
    return {"message": "E-commerce REST API is running"}


@app.get("/health")
def health_check():
    return {"status": "OK"}