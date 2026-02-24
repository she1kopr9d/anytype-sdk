from typing import Optional, Dict, Any
from ..client import AnytypeClient
from .. import models

class SpacesAPI:
    """API для работы с пространствами"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def list(
        self,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> models.PaginatedResponse[models.Space]:
        """
        Получить список пространств
        
        Args:
            offset: Смещение для пагинации
            limit: Количество элементов (макс 1000)
            filters: Фильтры в формате {"name[contains]": "project"}
        """
        params = {
            "offset": offset,
            "limit": min(limit, 1000),
            **(filters or {})
        }
        return self.client._request(
            "GET",
            "/spaces",
            params=params,
            response_model=models.PaginatedResponse[models.Space]
        )
    
    def get(self, space_id: str) -> models.Space:
        """Получить пространство по ID"""
        response = self.client._request(
            "GET",
            f"/spaces/{space_id}",
            response_model=models.SpaceResponse
        )
        return response.space
    
    def create(self, name: str, description: Optional[str] = None) -> models.Space:
        """Создать новое пространство"""
        request = models.CreateSpaceRequest(name=name, description=description)
        response = self.client._request(
            "POST",
            "/spaces",
            data=request,
            response_model=models.SpaceResponse
        )
        return response.space
    
    def update(
        self,
        space_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> models.Space:
        """Обновить пространство"""
        request = models.UpdateSpaceRequest(name=name, description=description)
        response = self.client._request(
            "PATCH",
            f"/spaces/{space_id}",
            data=request,
            response_model=models.SpaceResponse
        )
        return response.space
