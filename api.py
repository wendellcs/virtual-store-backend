from database.mongo import db
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os 
from routes import admin, products

load_dotenv()
app = FastAPI()

origins = [os.getenv("DEV_URL"), os.getenv('PROD_URL')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(products.router)
