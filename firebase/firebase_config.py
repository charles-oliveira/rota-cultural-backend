"""
Módulo responsável pela configuração do Firebase Admin SDK.
"""
import firebase_admin
from firebase_admin import credentials, auth, db
from config import FIREBASE_CONFIG

def init_firebase() -> None:
    """
    Inicializa o Firebase Admin SDK com as credenciais fornecidas.
    
    Raises:
        ValueError: Se as credenciais forem inválidas
    """
    try:
        cred = credentials.Certificate("firebase/serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': FIREBASE_CONFIG['databaseURL']
        })
        
        # Cria usuário admin se não existir
        try:
            auth.get_user_by_email("admin@rotacultural.com")
        except auth.UserNotFoundError:
            auth.create_user(
                email="admin@rotacultural.com",
                password="admin123",
                display_name="Administrador"
            )
    except Exception as e:
        raise ValueError(f"Erro ao inicializar Firebase: {str(e)}")
