from typing import Optional, Dict, Any
from ..client import AnytypeClient
from .. import models

class MembersAPI:
    """API для работы с участниками пространства"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def list(
        self,
        space_id: str,
        offset: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> models.PaginatedResponse[models.Member]:
        """Получить список участников пространства"""
        params = {
            "offset": offset,
            "limit": min(limit, 1000),
            **(filters or {})
        }
        return self.client._request(
            "GET",
            f"/spaces/{space_id}/members",
            params=params,
            response_model=models.PaginatedResponse[models.Member]
        )
    
    def get(self, space_id: str, member_id: str) -> models.Member:
        """Получить информацию об участнике"""
        response = self.client._request(
            "GET",
            f"/spaces/{space_id}/members/{member_id}",
            response_model=models.MemberResponse
        )
        return response.member
