import streamlit as st

def autenticar_admin():
    st.sidebar.title("🔐 Login do Administrador")
    usuario = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")
    login = st.sidebar.button("Entrar")

    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if login:
        if usuario == "admin" and senha == "123456":
            st.session_state.autenticado = True
        else:
            st.sidebar.error("Credenciais inválidas.")

    if not st.session_state.autenticado:
        st.stop()
