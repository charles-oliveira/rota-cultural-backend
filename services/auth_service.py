"""
Módulo responsável pelos serviços de autenticação.
"""
import firebase_admin
from firebase_admin import auth
from typing import Optional, Dict, Tuple
import logging
from config import LOG_LEVEL, LOG_FORMAT

# Configuração de logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class AuthService:
    """
    Serviço responsável por gerenciar a autenticação de usuários.
    """
    
    def __init__(self):
        """
        Inicializa o serviço de autenticação.
        """
        if not firebase_admin._apps:
            raise Exception("Firebase não inicializado. Chame init_firebase() primeiro.")

    def criar_usuario(self, email: str, senha: str) -> Dict:
        """
        Cria um novo usuário no Firebase Authentication.
        
        Args:
            email (str): Email do usuário
            senha (str): Senha do usuário
            
        Returns:
            Dict: Dicionário com informações do usuário criado
            
        Raises:
            Exception: Se houver erro ao criar o usuário
        """
        try:
            user = auth.create_user(
                email=email,
                password=senha
            )
            logger.info(f"Usuário criado com sucesso: {user.uid}")
            return {
                "uid": user.uid,
                "email": user.email
            }
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise

    def autenticar_usuario(self, email: str, senha: str) -> Tuple[Optional[str], str]:
        """
        Autentica um usuário com email e senha.
        Retorna o uid do usuário e uma mensagem de sucesso/erro.
        """
        try:
            user = auth.get_user_by_email(email)
            # Verifica se a senha está correta tentando fazer login
            auth.verify_password(email, senha)
            logger.info(f"Usuário autenticado com sucesso: {user.uid}")
            return user.uid, "Login realizado com sucesso!"
        except auth.UserNotFoundError:
            return None, "Usuário não encontrado."
        except auth.InvalidPasswordError:
            return None, "Senha incorreta."
        except Exception as e:
            logger.error(f"Erro ao autenticar usuário: {str(e)}")
            return None, f"Erro ao autenticar: {str(e)}"

    def verificar_token(self, token: str) -> Optional[Dict]:
        """
        Verifica a validade de um token de autenticação.
        
        Args:
            token (str): Token JWT a ser verificado
            
        Returns:
            Optional[Dict]: Informações do usuário se o token for válido, None caso contrário
            
        Raises:
            Exception: Se houver erro ao verificar o token
        """
        try:
            decoded_token = auth.verify_id_token(token)
            return {
                "uid": decoded_token["uid"],
                "email": decoded_token["email"]
            }
        except Exception as e:
            logger.error(f"Erro ao verificar token: {str(e)}")
            return None

    def obter_usuario(self, uid: str) -> Optional[Dict]:
        """
        Obtém informações de um usuário pelo UID.
        
        Args:
            uid (str): UID do usuário
            
        Returns:
            Optional[Dict]: Informações do usuário se encontrado, None caso contrário
            
        Raises:
            Exception: Se houver erro ao obter o usuário
        """
        try:
            user = auth.get_user(uid)
            return {
                "uid": user.uid,
                "email": user.email
            }
        except Exception as e:
            logger.error(f"Erro ao obter usuário {uid}: {str(e)}")
            return None

    def excluir_usuario(self, uid: str) -> None:
        """
        Exclui um usuário do Firebase Authentication.
        
        Args:
            uid (str): UID do usuário a ser excluído
            
        Raises:
            Exception: Se houver erro ao excluir o usuário
        """
        try:
            auth.delete_user(uid)
            logger.info(f"Usuário excluído com sucesso: {uid}")
        except Exception as e:
            logger.error(f"Erro ao excluir usuário {uid}: {str(e)}")
            raise 