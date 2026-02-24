from typing import Optional, List, Dict, Any
from ..client import AnytypeClient
from .. import models

class ObjectsAPI:
    """API для работы с объектами"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def list(
        self,
        space_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> models.PaginatedResponse[models.Object]:
        """
        Получить список объектов в пространстве
        
        Args:
            space_id: ID пространства
            offset: Смещение для пагинации
            limit: Количество элементов (макс 1000)
            filters: Фильтры в формате {"done": false, "tags[in]": ["urgent"]}
        """
        params = {
            "offset": offset,
            "limit": min(limit, 1000),
            **(filters or {})
        }
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/objects",
            params=params,
            response_model=models.PaginatedResponse[models.Object]
        )
    
    def get(
        self,
        space_id: str,
        object_id: str,
        format: str = "md"
    ) -> models.ObjectWithBody:
        """Получить объект по ID"""
        params = {"format": format} if format else {}
        response = self.client._request(
            "GET",
            f"/spaces/{space_id}/objects/{object_id}",
            params=params,
            response_model=models.ObjectResponse
        )
        return response.object
    
    def create(
        self,
        space_id: str,
        type_key: str,
        name: Optional[str] = None,
        body: Optional[str] = None,
        icon: Optional[models.Icon] = None,
        template_id: Optional[str] = None,
        properties: Optional[List[models.PropertyLink]] = None
    ) -> models.ObjectWithBody:
        """Создать новый объект"""
        request = models.CreateObjectRequest(
            type_key=type_key,
            name=name,
            body=body,
            icon=icon,
            template_id=template_id,
            properties=properties
        )
        response = self.client._request(
            "POST",
            f"/spaces/{space_id}/objects",
            data=request,
            response_model=models.ObjectResponse
        )
        return response.object
    
    def update(
        self,
        space_id: str,
        object_id: str,
        name: Optional[str] = None,
        markdown: Optional[str] = None,
        icon: Optional[models.Icon] = None,
        type_key: Optional[str] = None,
        properties: Optional[List[models.PropertyLink]] = None
    ) -> models.ObjectWithBody:
        """Обновить объект"""
        request = models.UpdateObjectRequest(
            name=name,
            markdown=markdown,
            icon=icon,
            type_key=type_key,
            properties=properties
        )
        response = self.client._request(
            "PATCH",
            f"/spaces/{space_id}/objects/{object_id}",
            data=request,
            response_model=models.ObjectResponse
        )
        return response.object
    
    def delete(self, space_id: str, object_id: str) -> models.ObjectWithBody:
        """Удалить объект (архивировать)"""
        response = self.client._request(
            "DELETE",
            f"/spaces/{space_id}/objects/{object_id}",
            response_model=models.ObjectResponse
        )
        return response.object
