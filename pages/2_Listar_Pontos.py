import streamlit as st
from firebase.firebase_config import init_firebase
from services.ponto_service import listar_pontos
from auth import autenticar_admin

autenticar_admin()
init_firebase()

st.title("📍 Pontos Cadastrados")

pontos = listar_pontos()

if pontos:
    for key, ponto in pontos.items():
        st.subheader(ponto.get("nome", "Sem nome"))
        st.markdown(f"**Tipo:** {ponto.get('tipo', 'Não informado')}")
        st.markdown(f"**Descrição:** {ponto.get('descricao', '')}")
        st.markdown(f"**Localização:** {ponto.get('latitude')}, {ponto.get('longitude')}")
        st.markdown("---")
else:
    st.info("Nenhum ponto cadastrado ainda.")