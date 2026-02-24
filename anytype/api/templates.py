from typing import Optional, Dict, Any
from ..client import AnytypeClient
from .. import models

class TemplatesAPI:
    """API для работы с шаблонами"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def list(
        self,
        space_id: str,
        type_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> models.PaginatedResponse[models.Object]:
        """Получить список шаблонов для типа"""
        params = {
            "offset": offset,
            "limit": min(limit, 1000),
            **(filters or {})
        }
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/types/{type_id}/templates",
            params=params,
            response_model=models.PaginatedResponse[models.Object]
        )
    
    def get(
        self,
        space_id: str,
        type_id: str,
        template_id: str
    ) -> models.ObjectWithBody:
        """Получить шаблон по ID"""
        response = self.client._request(
            "GET",
            f"/spaces/{space_id}/types/{type_id}/templates/{template_id}",
            response_model=models.TemplateResponse
        )
        return response.template
