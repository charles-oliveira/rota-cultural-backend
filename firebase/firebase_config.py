import firebase_admin
from firebase_admin import credentials, auth, db
from config import FIREBASE_CONFIG

def init_firebase() -> None:
    """
    Inicializa o Firebase Admin SDK com as credenciais fornecidas.
    """
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase/serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_CONFIG['databaseURL']
            })
        else:
            print("Firebase já foi inicializado.")
    except Exception as e:
        raise ValueError(f"Erro ao inicializar Firebase: {str(e)}")

def is_firebase_initialized() -> bool:
    """
    Verifica se o Firebase já foi inicializado.
    
    Returns:
        bool: True se inicializado, False caso contrário.
    """
    return bool(firebase_admin._apps)