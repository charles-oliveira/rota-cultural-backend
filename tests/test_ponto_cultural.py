import pytest
from models.ponto_cultural import PontoCultural
from config import TIPOS_PONTOS

def test_criacao_ponto_valido():
    ponto = PontoCultural(
        nome="Museu do Amanhã",
        descricao="Museu de ciências",
        tipo="Museu",
        latitude=-22.8947,
        longitude=-43.1802
    )
    assert ponto.validar() is True
    assert ponto.nome == "Museu do Amanhã"
    assert ponto.tipo == "Museu"

def test_validacao_nome_obrigatorio():
    with pytest.raises(ValueError, match="Nome é obrigatório"):
        PontoCultural(
            nome="",
            descricao="Descrição",
            tipo="Museu",
            latitude=-22.8947,
            longitude=-43.1802
        ).validar()

def test_validacao_tipo_obrigatorio():
    with pytest.raises(ValueError, match="Tipo é obrigatório"):
        PontoCultural(
            nome="Nome",
            descricao="Descrição",
            tipo="",
            latitude=-22.8947,
            longitude=-43.1802
        ).validar()

def test_validacao_tipo_invalido():
    with pytest.raises(ValueError, match=f"Tipo inválido"):
        PontoCultural(
            nome="Nome",
            descricao="Descrição",
            tipo="Tipo Inválido",
            latitude=-22.8947,
            longitude=-43.1802
        ).validar()

def test_validacao_latitude_invalida():
    with pytest.raises(ValueError, match="Latitude deve estar entre"):
        PontoCultural(
            nome="Nome",
            descricao="Descrição",
            tipo="Museu",
            latitude=100.0,
            longitude=-43.1802
        ).validar()

def test_validacao_longitude_invalida():
    with pytest.raises(ValueError, match="Longitude deve estar entre"):
        PontoCultural(
            nome="Nome",
            descricao="Descrição",
            tipo="Museu",
            latitude=-22.8947,
            longitude=200.0
        ).validar()

def test_conversao_para_dict():
    ponto = PontoCultural(
        nome="Museu do Amanhã",
        descricao="Museu de ciências",
        tipo="Museu",
        latitude=-22.8947,
        longitude=-43.1802
    )
    dict_ponto = ponto.to_dict()
    assert dict_ponto["nome"] == "Museu do Amanhã"
    assert dict_ponto["tipo"] == "Museu"
    assert dict_ponto["latitude"] == "-22.8947"
    assert dict_ponto["longitude"] == "-43.1802"

def test_criacao_a_partir_de_dict():
    dict_ponto = {
        "nome": "Museu do Amanhã",
        "descricao": "Museu de ciências",
        "tipo": "Museu",
        "latitude": "-22.8947",
        "longitude": "-43.1802"
    }
    ponto = PontoCultural.from_dict(dict_ponto, "123")
    assert ponto.id == "123"
    assert ponto.nome == "Museu do Amanhã"
    assert ponto.tipo == "Museu"
    assert ponto.latitude == -22.8947
    assert ponto.longitude == -43.1802 