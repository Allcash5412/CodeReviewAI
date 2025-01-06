from fastapi import FastAPI
from src.api.routes.review_router import review as review_router

app = FastAPI(root_path='/api/v1')


app.include_router(review_router, tags=['Code Review'])
