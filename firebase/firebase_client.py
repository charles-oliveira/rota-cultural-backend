"""
Módulo responsável pela configuração e autenticação do cliente Firebase.
"""
import streamlit as st
import pyrebase
from config import FIREBASE_CONFIG
from typing import Optional, Dict, Tuple

# Inicializa o Firebase
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()

def login(email: str, senha: str) -> Tuple[bool, str]:
    """
    Realiza o login do usuário no Firebase.
    
    Args:
        email (str): Email do usuário
        senha (str): Senha do usuário
        
    Returns:
        Tuple[bool, str]: Tupla contendo status do login e mensagem
    """
    try:
        user = auth.sign_in_with_email_and_password(email, senha)
        st.session_state["user"] = user
        return True, "Login realizado com sucesso!"
    except Exception as e:
        return False, f"Erro ao fazer login: {str(e)}"

def logout() -> None:
    """
    Realiza o logout do usuário e limpa a sessão.
    """
    if "user" in st.session_state:
        del st.session_state["user"]

def is_authenticated() -> bool:
    """
    Verifica se o usuário está autenticado.
    
    Returns:
        bool: True se o usuário estiver autenticado, False caso contrário
    """
    return "user" in st.session_state

def get_user() -> Optional[Dict]:
    """
    Obtém as informações do usuário autenticado.
    
    Returns:
        Optional[Dict]: Dicionário com informações do usuário se autenticado, None caso contrário
    """
    return st.session_state.get("user")

def require_auth():
    """
    Verifica se o usuário está autenticado.
    Se não estiver, exibe uma mensagem de erro e interrompe a execução.
    """
    if not is_authenticated():
        st.error("Você precisa estar logado para acessar esta página.")
        st.stop() 