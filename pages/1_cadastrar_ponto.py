import streamlit as st
import folium
from streamlit_folium import st_folium
from firebase.firebase_config import init_firebase
from services.ponto_service import PontoService
from firebase.firebase_client import require_auth, get_user
from config import TIPOS_PONTOS

# Verifica autenticação
require_auth()

# Inicializa serviços
init_firebase()
ponto_service = PontoService()

# Cabeçalho com navegação
st.title("📌 Cadastrar Novo Ponto Cultural")

# Botões de navegação
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Página Inicial"):
        st.switch_page("pages/0_login.py")
with col2:
    if st.button("📍 Listar Pontos"):
        st.switch_page("pages/2_listar_pontos.py")
with col3:
    if st.button("🚪 Sair"):
        st.switch_page("pages/0_login.py")

# Mapa interativo
st.subheader("🗺️ Selecione a localização no mapa")
m = folium.Map(location=[-7.0, -37.0], zoom_start=6)

map_data = st_folium(m, width=700, height=500)

latitude = ""
longitude = ""

if map_data and map_data["last_clicked"]:
    latitude = map_data["last_clicked"]["lat"]
    longitude = map_data["last_clicked"]["lng"]
    st.success(f"Localização selecionada: {latitude}, {longitude}")

with st.form("form-cadastro"):
    nome = st.text_input("Nome do ponto")
    descricao = st.text_area("Descrição")
    tipo = st.selectbox("Tipo", TIPOS_PONTOS)

    submit = st.form_submit_button("Cadastrar")

    if submit:
        if nome and latitude and longitude:
            try:
                dados = {
                    "nome": nome,
                    "descricao": descricao,
                    "tipo": tipo,
                    "latitude": latitude,
                    "longitude": longitude,
                    "criado_por": get_user()['uid']
                }
                id_ponto = ponto_service.cadastrar_ponto(dados)
                st.success(f"Ponto cadastrado com sucesso! ID: {id_ponto}")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao cadastrar ponto: {str(e)}")
        else:
            st.warning("Selecione uma localização no mapa e preencha todos os campos obrigatórios.")
