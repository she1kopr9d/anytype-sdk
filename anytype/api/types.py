from typing import Optional, List, Dict, Any
from ..client import AnytypeClient
from .. import models

class TypesAPI:
    """API для работы с типами"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def list(
        self,
        space_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> models.PaginatedResponse[models.Type]:
        """Получить список типов"""
        params = {
            "offset": offset,
            "limit": min(limit, 1000),
            **(filters or {})
        }
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/types",
            params=params,
            response_model=models.PaginatedResponse[models.Type]
        )
    
    def get(self, space_id: str, type_id: str) -> models.Type:
        """Получить тип по ID"""
        response = self.client._request(
            "GET",
            f"/spaces/{space_id}/types/{type_id}",
            response_model=models.TypeResponse
        )
        return response.type
    
    def create(
        self,
        space_id: str,
        name: str,
        plural_name: str,
        layout: models.TypeLayout,
        icon: Optional[models.Icon] = None,
        key: Optional[str] = None,
        properties: Optional[List[models.PropertyLink]] = None
    ) -> models.Type:
        """Создать новый тип"""
        request = models.CreateTypeRequest(
            name=name,
            plural_name=plural_name,
            layout=layout,
            icon=icon,
            key=key,
            properties=properties
        )
        response = self.client._request(
            "POST",
            f"/spaces/{space_id}/types",
            data=request,
            response_model=models.TypeResponse
        )
        return response.type
    
    def update(
        self,
        space_id: str,
        type_id: str,
        name: Optional[str] = None,
        plural_name: Optional[str] = None,
        layout: Optional[models.TypeLayout] = None,
        icon: Optional[models.Icon] = None,
        key: Optional[str] = None,
        properties: Optional[List[models.PropertyLink]] = None
    ) -> models.Type:
        """Обновить тип"""
        request = models.UpdateTypeRequest(
            name=name,
            plural_name=plural_name,
            layout=layout,
            icon=icon,
            key=key,
            properties=properties
        )
        response = self.client._request(
            "PATCH",
            f"/spaces/{space_id}/types/{type_id}",
            data=request,
            response_model=models.TypeResponse
        )
        return response.type
    
    def delete(self, space_id: str, type_id: str) -> models.Type:
        """Удалить тип"""
        response = self.client._request(
            "DELETE",
            f"/spaces/{space_id}/types/{type_id}",
            response_model=models.TypeResponse
        )
        return response.type
