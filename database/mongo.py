from pymongo import MongoClient
from dotenv import load_dotenv
import ssl
import os

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')

if not MONGO_URL:
    raise RuntimeError('MONGO_URL não encontrada no .env')

client = MongoClient(
    MONGO_URL,     
    tls=True,
    tlsAllowInvalidCertificates=False,
    ssl_cert_reqs=ssl.CERT_REQUIRED
)

db = client['compra-facil']
collection = db['produtos']
