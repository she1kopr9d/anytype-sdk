from typing import Optional, Dict, Any, List
from ..client import AnytypeClient
from .. import models

class PropertiesAPI:
    """API для работы со свойствами"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def list(
        self,
        space_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> models.PaginatedResponse[models.Property]:
        """Получить список свойств"""
        params = {
            "offset": offset,
            "limit": min(limit, 1000),
            **(filters or {})
        }
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/properties",
            params=params,
            response_model=models.PaginatedResponse[models.Property]
        )
    
    def get(self, space_id: str, property_id: str) -> models.Property:
        """Получить свойство по ID"""
        response = self.client._request(
            "GET",
            f"/spaces/{space_id}/properties/{property_id}",
            response_model=models.PropertyResponse
        )
        return response.property
    
    def create(
        self,
        space_id: str,
        name: str,
        format: models.PropertyFormat,
        key: Optional[str] = None,
        tags: Optional[List[models.CreateTagRequest]] = None
    ) -> models.Property:
        """Создать новое свойство"""
        request = models.CreatePropertyRequest(
            name=name,
            format=format,
            key=key,
            tags=tags
        )
        response = self.client._request(
            "POST",
            f"/spaces/{space_id}/properties",
            data=request,
            response_model=models.PropertyResponse
        )
        return response.property
    
    def update(
        self,
        space_id: str,
        property_id: str,
        name: str,
        key: Optional[str] = None
    ) -> models.Property:
        """Обновить свойство"""
        request = models.UpdatePropertyRequest(name=name, key=key)
        response = self.client._request(
            "PATCH",
            f"/spaces/{space_id}/properties/{property_id}",
            data=request,
            response_model=models.PropertyResponse
        )
        return response.property
    
    def delete(self, space_id: str, property_id: str) -> models.Property:
        """Удалить свойство"""
        response = self.client._request(
            "DELETE",
            f"/spaces/{space_id}/properties/{property_id}",
            response_model=models.PropertyResponse
        )
        return response.property
