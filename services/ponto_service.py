from firebase_admin import db

def cadastrar_ponto(dados):
    ref = db.reference("pontos")
    novo_ponto_ref = ref.push(dados)
    return novo_ponto_ref.key

def listar_pontos():
    ref = db.reference("pontos")
    return ref.get()