from typing import Optional, Dict, Any
from ..client import AnytypeClient
from .. import models

class TagsAPI:
    """API для работы с тегами"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def list(
        self,
        space_id: str,
        property_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> models.PaginatedResponse[models.Tag]:
        """Получить список тегов для свойства"""
        params = {
            "offset": offset,
            "limit": min(limit, 1000),
            **(filters or {})
        }
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/properties/{property_id}/tags",
            params=params,
            response_model=models.PaginatedResponse[models.Tag]
        )
    
    def get(self, space_id: str, property_id: str, tag_id: str) -> models.Tag:
        """Получить тег по ID"""
        response = self.client._request(
            "GET",
            f"/spaces/{space_id}/properties/{property_id}/tags/{tag_id}",
            response_model=models.TagResponse
        )
        return response.tag
    
    def create(
        self,
        space_id: str,
        property_id: str,
        name: str,
        color: models.Color,
        key: Optional[str] = None
    ) -> models.Tag:
        """Создать новый тег"""
        request = models.CreateTagRequest(name=name, color=color, key=key)
        response = self.client._request(
            "POST",
            f"/spaces/{space_id}/properties/{property_id}/tags",
            data=request,
            response_model=models.TagResponse
        )
        return response.tag
    
    def update(
        self,
        space_id: str,
        property_id: str,
        tag_id: str,
        name: Optional[str] = None,
        color: Optional[models.Color] = None,
        key: Optional[str] = None
    ) -> models.Tag:
        """Обновить тег"""
        request = models.UpdateTagRequest(name=name, color=color, key=key)
        response = self.client._request(
            "PATCH",
            f"/spaces/{space_id}/properties/{property_id}/tags/{tag_id}",
            data=request,
            response_model=models.TagResponse
        )
        return response.tag
    
    def delete(self, space_id: str, property_id: str, tag_id: str) -> models.Tag:
        """Удалить тег"""
        response = self.client._request(
            "DELETE",
            f"/spaces/{space_id}/properties/{property_id}/tags/{tag_id}",
            response_model=models.TagResponse
        )
        return response.tag
