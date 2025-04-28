"""
Módulo de configuração do sistema.
"""
import os
from typing import List
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Firebase Admin
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase/serviceAccountKey.json")
FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")

# Configurações do Firebase Client
# Substitua os valores abaixo pelos valores do seu projeto Firebase
# Para obter esses valores:
# 1. Acesse https://console.firebase.google.com/
# 2. Selecione seu projeto
# 3. Clique em ⚙️ > Configurações do Projeto
# 4. Role até "Seus aplicativos" e clique no ícone web (</>)
# 5. Registre o app e copie as configurações
FIREBASE_CONFIG = {
    # Configurações do Firebase Client SDK
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

# Configurações da Aplicação
PAGINACAO_LIMITE = int(os.getenv("PAGINACAO_LIMITE", "10"))
TIPOS_PONTOS = ["Museu", "Grafite", "Teatro", "Feira", "Evento"]

# Configurações de Cache
CACHE_TEMPO_EXPIRACAO = 300  # 5 minutos em segundos

# Configurações de Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configurações de Validação
LATITUDE_MIN = -90.0
LATITUDE_MAX = 90.0
LONGITUDE_MIN = -180.0
LONGITUDE_MAX = 180.0 