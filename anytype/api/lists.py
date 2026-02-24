from typing import List, Optional
from ..client import AnytypeClient
from .. import models

class ListsAPI:
    """API для работы со списками (коллекции и сеты)"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def add_objects(
        self,
        space_id: str,
        list_id: str,
        object_ids: List[str]
    ) -> str:
        """Добавить объекты в список"""
        request = models.AddObjectsToListRequest(objects=object_ids)
        return self.client._request(
            "POST",
            f"/spaces/{space_id}/lists/{list_id}/objects",
            data=request
        )
    
    def remove_object(
        self,
        space_id: str,
        list_id: str,
        object_id: str
    ) -> str:
        """Удалить объект из списка"""
        return self.client._request(
            "DELETE",
            f"/spaces/{space_id}/lists/{list_id}/objects/{object_id}"
        )
    
    def get_views(
        self,
        space_id: str,
        list_id: str,
        offset: int = 0,
        limit: int = 100
    ) -> models.PaginatedResponse[models.View]:
        """Получить представления списка"""
        params = {"offset": offset, "limit": limit}
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/lists/{list_id}/views",
            params=params,
            response_model=models.PaginatedResponse[models.View]
        )
    
    def get_objects(
        self,
        space_id: str,
        list_id: str,
        view_id: str,
        offset: int = 0,
        limit: int = 100
    ) -> models.PaginatedResponse[models.Object]:
        """Получить объекты в представлении списка"""
        params = {"offset": offset, "limit": limit}
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/lists/{list_id}/views/{view_id}/objects",
            params=params,
            response_model=models.PaginatedResponse[models.Object]
        )
