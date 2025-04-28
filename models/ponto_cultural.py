from dataclasses import dataclass
from typing import Optional
from config import (
    LATITUDE_MIN, LATITUDE_MAX,
    LONGITUDE_MIN, LONGITUDE_MAX,
    TIPOS_PONTOS
)

@dataclass
class PontoCultural:
    nome: str
    descricao: str
    tipo: str
    latitude: float
    longitude: float
    criado_por: str
    id: Optional[str] = None

    def validar(self) -> bool:
        # Validação do nome
        if not self.nome or len(self.nome.strip()) == 0:
            raise ValueError("Nome é obrigatório")
        
        # Validação do tipo
        if not self.tipo or len(self.tipo.strip()) == 0:
            raise ValueError("Tipo é obrigatório")
        if self.tipo not in TIPOS_PONTOS:
            raise ValueError(f"Tipo inválido. Deve ser um dos seguintes: {', '.join(TIPOS_PONTOS)}")
        
        # Validação das coordenadas
        if not isinstance(self.latitude, (int, float)) or not isinstance(self.longitude, (int, float)):
            raise ValueError("Latitude e longitude devem ser números")
        
        if not (LATITUDE_MIN <= self.latitude <= LATITUDE_MAX):
            raise ValueError(f"Latitude deve estar entre {LATITUDE_MIN} e {LATITUDE_MAX}")
        
        if not (LONGITUDE_MIN <= self.longitude <= LONGITUDE_MAX):
            raise ValueError(f"Longitude deve estar entre {LONGITUDE_MIN} e {LONGITUDE_MAX}")
        
        # Validação do criador
        if not self.criado_por:
            raise ValueError("ID do criador é obrigatório")
        
        return True

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "latitude": str(self.latitude),
            "longitude": str(self.longitude),
            "criado_por": self.criado_por
        }

    @classmethod
    def from_dict(cls, data: dict, id: str = None) -> 'PontoCultural':
        try:
            latitude = float(data.get("latitude", 0))
            longitude = float(data.get("longitude", 0))
        except (ValueError, TypeError):
            raise ValueError("Latitude e longitude devem ser números válidos")

        return cls(
            id=id,
            nome=data.get("nome", ""),
            descricao=data.get("descricao", ""),
            tipo=data.get("tipo", ""),
            latitude=latitude,
            longitude=longitude,
            criado_por=data.get("criado_por", "")
        ) 