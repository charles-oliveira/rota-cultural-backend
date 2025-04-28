import streamlit as st
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
st.title("📍 Pontos Culturais Cadastrados")

# Botões de navegação
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Página Inicial"):
        st.switch_page("pages/0_login.py")
with col2:
    if st.button("📌 Cadastrar Ponto"):
        st.switch_page("pages/1_cadastrar_ponto.py")
with col3:
    if st.button("🚪 Sair"):
        st.switch_page("pages/0_login.py")

# Filtros e busca
col1, col2 = st.columns([3, 1])
with col1:
    termo_busca = st.text_input("Buscar pontos", placeholder="Digite para buscar por nome, descrição ou tipo")
with col2:
    tipo_filtro = st.selectbox("Filtrar por tipo", ["Todos"] + TIPOS_PONTOS)

# Paginação
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = 1

try:
    if termo_busca:
        pontos = ponto_service.buscar_pontos(termo_busca)
        total_paginas = 1
    else:
        tipo = tipo_filtro if tipo_filtro != "Todos" else None
        pontos, total_paginas = ponto_service.listar_pontos(
            pagina=st.session_state.pagina_atual,
            tipo=tipo
        )

    if pontos:
        # Exibe os pontos
        for ponto in pontos:
            with st.expander(f"{ponto.nome} ({ponto.tipo})"):
                st.write(f"**Descrição:** {ponto.descricao}")
                st.write(f"**Localização:** {ponto.latitude}, {ponto.longitude}")
                
                # Só permite excluir pontos criados pelo usuário atual
                if ponto.criado_por == get_user()['uid']:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("Excluir", key=f"excluir_{ponto.id}"):
                            try:
                                ponto_service.excluir_ponto(ponto.id)
                                st.success("Ponto excluído com sucesso!")
                                st.experimental_rerun()
                            except Exception as e:
                                st.error(f"Erro ao excluir ponto: {str(e)}")

        # Controles de paginação
        if total_paginas > 1 and not termo_busca:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("Anterior") and st.session_state.pagina_atual > 1:
                    st.session_state.pagina_atual -= 1
                    st.experimental_rerun()
            with col2:
                st.write(f"Página {st.session_state.pagina_atual} de {total_paginas}")
            with col3:
                if st.button("Próxima") and st.session_state.pagina_atual < total_paginas:
                    st.session_state.pagina_atual += 1
                    st.experimental_rerun()
    else:
        st.info("Nenhum ponto encontrado.")

except Exception as e:
    st.error(f"Erro ao carregar pontos: {str(e)}")
