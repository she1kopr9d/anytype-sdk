from typing import Optional, List
from ..client import AnytypeClient
from .. import models

class SearchAPI:
    """API для поиска"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def global_search(
        self,
        query: Optional[str] = None,
        types: Optional[List[str]] = None,
        filters: Optional[models.FilterExpression] = None,
        sort: Optional[models.SortOptions] = None,
        offset: int = 0,
        limit: int = 100
    ) -> models.PaginatedResponse[models.Object]:
        """
        Глобальный поиск по всем пространствам
        
        Args:
            query: Текст для поиска
            types: Типы объектов для фильтрации
            filters: Выражение фильтрации
            sort: Параметры сортировки
            offset: Смещение для пагинации
            limit: Количество элементов
        """
        request = models.SearchRequest(
            query=query,
            types=types,
            filters=filters,
            sort=sort
        )
        params = {"offset": offset, "limit": min(limit, 1000)}
        
        return self.client._request(
            "POST",
            "/search",
            params=params,
            data=request,
            response_model=models.PaginatedResponse[models.Object]
        )
    
    def search_in_space(
        self,
        space_id: str,
        query: Optional[str] = None,
        types: Optional[List[str]] = None,
        filters: Optional[models.FilterExpression] = None,
        sort: Optional[models.SortOptions] = None,
        offset: int = 0,
        limit: int = 100
    ) -> models.PaginatedResponse[models.Object]:
        """
        Поиск в конкретном пространстве
        
        Args:
            space_id: ID пространства
            query: Текст для поиска
            types: Типы объектов для фильтрации
            filters: Выражение фильтрации
            sort: Параметры сортировки
            offset: Смещение для пагинации
            limit: Количество элементов
        """
        request = models.SearchRequest(
            query=query,
            types=types,
            filters=filters,
            sort=sort
        )
        params = {"offset": offset, "limit": min(limit, 1000)}
        
        return self.client._request(
            "POST",
            f"/spaces/{space_id}/search",
            params=params,
            data=request,
            response_model=models.PaginatedResponse[models.Object]
        )
