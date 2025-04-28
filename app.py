import streamlit as st
from auth import autenticar_admin

autenticar_admin()


st.set_page_config(page_title="Rota Cultura Admin", layout="wide")

st.title("🎨 Rota Cultura - Painel de Administração")
st.markdown("""
Bem-vindo ao painel de administração do **Rota Cultura**!

Use o menu lateral para:
- Cadastrar novos pontos culturais
- Visualizar e excluir os pontos já cadastrados
""")
