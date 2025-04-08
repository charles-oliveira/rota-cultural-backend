from auth import autenticar_admin
from firebase.firebase_config import init_firebase

import streamlit as st

st.set_page_config(page_title="Rota Cultura", layout="wide")
autenticar_admin()
init_firebase()

st.title("🌎 Rota Cultura - Painel Administrativo")
st.markdown("Use o menu à esquerda para acessar as funcionalidades.")