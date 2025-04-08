import streamlit as st
import folium
from streamlit_folium import st_folium
from firebase.firebase_config import init_firebase
from services.ponto_service import cadastrar_ponto
from auth import autenticar_admin

autenticar_admin()
init_firebase()

st.title("📌 Cadastrar Novo Ponto Cultural")

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
    tipo = st.selectbox("Tipo", ["Museu", "Grafite", "Teatro", "Feira", "Evento"])

    submit = st.form_submit_button("Cadastrar")

    if submit:
        if nome and latitude and longitude:
            dados = {
                "nome": nome,
                "descricao": descricao,
                "tipo": tipo,
                "latitude": str(latitude),
                "longitude": str(longitude)
            }
            id_ponto = cadastrar_ponto(dados)
            st.success(f"Ponto cadastrado com sucesso! ID: {id_ponto}")
        else:
            st.warning("Selecione uma localização no mapa.")