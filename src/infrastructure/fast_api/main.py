from fastapi import FastAPI

from src.infrastructure.fast_api.views.product import router as products_router
from src.infrastructure.fast_api.views.order import router as orders_router


app = FastAPI()
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
