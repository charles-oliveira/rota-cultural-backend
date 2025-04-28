"""
Módulo responsável pelos serviços relacionados aos pontos culturais.
"""
from firebase_admin import db
import uuid
import logging
from typing import Dict, Optional, List, Tuple
from models.ponto_cultural import PontoCultural
from utils.cache import Cache
from config import PAGINACAO_LIMITE, LOG_LEVEL, LOG_FORMAT

# Configuração de logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class PontoService:
    """
    Serviço responsável por gerenciar os pontos culturais no Firebase.
    """
    
    def __init__(self):
        """
        Inicializa o serviço com a referência do banco de dados e cache.
        """
        self.ref = db.reference('pontos')
        self.cache = Cache()

    def _get_cache_key(self, prefix: str, **kwargs) -> str:
        """
        Gera uma chave única para o cache baseada nos parâmetros.
        
        Args:
            prefix (str): Prefixo para a chave
            **kwargs: Parâmetros adicionais
            
        Returns:
            str: Chave única para o cache
        """
        params = '_'.join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return f"{prefix}_{params}"

    def cadastrar_ponto(self, dados: dict) -> str:
        """
        Cadastra um novo ponto cultural.
        
        Args:
            dados (dict): Dicionário com os dados do ponto
            
        Returns:
            str: ID do ponto cadastrado
            
        Raises:
            Exception: Se houver erro ao cadastrar o ponto
        """
        try:
            ponto = PontoCultural.from_dict(dados)
            ponto.validar()
            
            id_ponto = str(uuid.uuid4())
            self.ref.child(id_ponto).set(ponto.to_dict())
            
            # Invalida cache após cadastro
            self.cache.clear()
            
            logger.info(f"Ponto cultural cadastrado com sucesso: {id_ponto}")
            return id_ponto
            
        except Exception as e:
            logger.error(f"Erro ao cadastrar ponto cultural: {str(e)}")
            raise

    def listar_pontos(self, pagina: int = 1, tipo: Optional[str] = None, limite: Optional[int] = None) -> Tuple[List[PontoCultural], int]:
        """
        Lista os pontos culturais com paginação e filtros.
        
        Args:
            pagina (int): Número da página
            tipo (Optional[str]): Tipo de ponto para filtrar
            limite (Optional[int]): Limite de pontos por página
            
        Returns:
            Tuple[List[PontoCultural], int]: Lista de pontos e total de páginas
            
        Raises:
            Exception: Se houver erro ao listar os pontos
        """
        try:
            cache_key = self._get_cache_key("listar_pontos", pagina=pagina, tipo=tipo, limite=limite)
            cached_result = self.cache.get(cache_key)
            
            if cached_result:
                return cached_result

            pontos_data = self.ref.get() or {}
            pontos = []
            
            for id_ponto, ponto_data in pontos_data.items():
                if tipo and ponto_data.get("tipo") != tipo:
                    continue
                pontos.append(PontoCultural.from_dict(ponto_data, id_ponto))
            
            # Ordena por nome
            pontos.sort(key=lambda x: x.nome)
            
            # Paginação
            if limite:
                pontos = pontos[:limite]
            else:
                inicio = (pagina - 1) * PAGINACAO_LIMITE
                fim = inicio + PAGINACAO_LIMITE
                pontos = pontos[inicio:fim]
            
            total_paginas = (len(pontos) + PAGINACAO_LIMITE - 1) // PAGINACAO_LIMITE if not limite else 1
            
            result = (pontos, total_paginas)
            self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao listar pontos culturais: {str(e)}")
            raise

    def buscar_pontos(self, termo: str) -> List[PontoCultural]:
        """
        Busca pontos culturais por termo.
        
        Args:
            termo (str): Termo para busca
            
        Returns:
            List[PontoCultural]: Lista de pontos encontrados
            
        Raises:
            Exception: Se houver erro ao buscar os pontos
        """
        try:
            cache_key = self._get_cache_key("buscar_pontos", termo=termo)
            cached_result = self.cache.get(cache_key)
            
            if cached_result:
                return cached_result

            pontos_data = self.ref.get() or {}
            resultados = []
            
            termo = termo.lower()
            for id_ponto, ponto_data in pontos_data.items():
                if (termo in ponto_data.get("nome", "").lower() or 
                    termo in ponto_data.get("descricao", "").lower() or
                    termo in ponto_data.get("tipo", "").lower()):
                    resultados.append(PontoCultural.from_dict(ponto_data, id_ponto))
            
            # Ordena por nome
            resultados.sort(key=lambda x: x.nome)
            
            self.cache.set(cache_key, resultados)
            return resultados
            
        except Exception as e:
            logger.error(f"Erro ao buscar pontos culturais: {str(e)}")
            raise

    def excluir_ponto(self, id_ponto: str) -> None:
        """
        Exclui um ponto cultural.
        
        Args:
            id_ponto (str): ID do ponto a ser excluído
            
        Raises:
            Exception: Se houver erro ao excluir o ponto
        """
        try:
            self.ref.child(id_ponto).delete()
            # Invalida cache após exclusão
            self.cache.clear()
            logger.info(f"Ponto cultural excluído com sucesso: {id_ponto}")
        except Exception as e:
            logger.error(f"Erro ao excluir ponto cultural {id_ponto}: {str(e)}")
            raise

    def buscar_por_id(self, id_ponto: str) -> Optional[PontoCultural]:
        """
        Busca um ponto cultural pelo ID.
        
        Args:
            id_ponto (str): ID do ponto
            
        Returns:
            Optional[PontoCultural]: Ponto encontrado ou None
            
        Raises:
            Exception: Se houver erro ao buscar o ponto
        """
        try:
            cache_key = self._get_cache_key("buscar_por_id", id_ponto=id_ponto)
            cached_result = self.cache.get(cache_key)
            
            if cached_result:
                return cached_result

            ponto_data = self.ref.child(id_ponto).get()
            if ponto_data:
                ponto = PontoCultural.from_dict(ponto_data, id_ponto)
                self.cache.set(cache_key, ponto)
                return ponto
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar ponto cultural {id_ponto}: {str(e)}")
            raise
