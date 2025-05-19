import streamlit as st
from firebase.firebase_client import login, logout, is_authenticated, get_user
from firebase.firebase_config import init_firebase, is_firebase_initialized
from services.ponto_service import PontoService
from config import TIPOS_PONTOS
import folium
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(
    page_title="Rota Cultural PB - Login",
    page_icon="🎭",
    layout="wide"
)

# Inicializa o Firebase apenas se ainda não estiver inicializado
if not is_firebase_initialized():
    init_firebase()

# Inicializa serviços
ponto_service = PontoService()

def show_login_form():
    """Exibe o formulário de login"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.title("🎭 Rota Cultural PB")
        st.subheader("Login")
        
        with st.form("login_form"):
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if not email or not senha:
                    st.error("Por favor, preencha todos os campos.")
                    return
                    
                sucesso, mensagem = login(email, senha)
                if sucesso:
                    st.success(mensagem)
                    st.experimental_rerun()
                else:
                    st.error(mensagem)
    
    with col2:
        st.subheader("📍 Pontos Culturais Recentes")
        try:
            pontos, _ = ponto_service.listar_pontos(pagina=1, limite=5)
            if pontos:
                # Cria o mapa
                m = folium.Map(location=[-7.0, -37.0], zoom_start=6)
                
                # Adiciona os pontos ao mapa
                for ponto in pontos:
                    folium.Marker(
                        [ponto.latitude, ponto.longitude],
                        popup=f"<b>{ponto.nome}</b><br>{ponto.tipo}",
                        tooltip=ponto.nome
                    ).add_to(m)
                
                # Exibe o mapa
                st_folium(m, width=700, height=400)
                
                # Lista os pontos
                for ponto in pontos:
                    with st.expander(f"📍 {ponto.nome} ({ponto.tipo})"):
                        st.write(f"**Descrição:** {ponto.descricao}")
                        st.write(f"**Localização:** {ponto.latitude}, {ponto.longitude}")
            else:
                st.info("Nenhum ponto cultural cadastrado ainda.")
        except Exception as e:
            st.error(f"Erro ao carregar pontos: {str(e)}")

def show_logout():
    """Exibe a tela de logout com os pontos"""
    user = get_user()
    
    # Cabeçalho
    st.title(f"Bem-vindo, {user['email']}!")
    
    # Botões de navegação
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📌 Cadastrar Ponto"):
            st.switch_page("pages/1_cadastrar_ponto.py")
    with col2:
        if st.button("📍 Listar Pontos"):
            st.switch_page("pages/2_listar_pontos.py")
    with col3:
        if st.button("🚪 Sair"):
            logout()
    
    # Exibe os pontos recentes
    st.subheader("📍 Pontos Culturais Recentes")
    try:
        pontos, _ = ponto_service.listar_pontos(pagina=1, limite=5)
        if pontos:
            # Cria o mapa
            m = folium.Map(location=[-7.0, -37.0], zoom_start=6)
            
            # Adiciona os pontos ao mapa
            for ponto in pontos:
                folium.Marker(
                    [ponto.latitude, ponto.longitude],
                    popup=f"<b>{ponto.nome}</b><br>{ponto.tipo}",
                    tooltip=ponto.nome
                ).add_to(m)
            
            # Exibe o mapa
            st_folium(m, width=700, height=400)
            
            # Lista os pontos
            for ponto in pontos:
                with st.expander(f"📍 {ponto.nome} ({ponto.tipo})"):
                    st.write(f"**Descrição:** {ponto.descricao}")
                    st.write(f"**Localização:** {ponto.latitude}, {ponto.longitude}")
                    
                    # Botão para excluir se for o criador
                    if ponto.criado_por == user['uid']:
                        if st.button("🗑️ Excluir", key=f"excluir_{ponto.id}"):
                            try:
                                ponto_service.excluir_ponto(ponto.id)
                                st.success("Ponto excluído com sucesso!")
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"Erro ao excluir ponto: {str(e)}")
        else:
            st.info("Nenhum ponto cultural cadastrado ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar pontos: {str(e)}")

# Verifica se o usuário está autenticado
if is_authenticated():
    show_logout()
else:
    show_login_form()