from ..client import AnytypeClient
from .. import models
from typing import Optional

class AuthAPI:
    """API для аутентификации"""
    
    def __init__(self, client: AnytypeClient):
        self.client = client
    
    def create_challenge(self, app_name: str) -> models.CreateChallengeResponse:
        """
        Создать challenge для аутентификации
        
        Args:
            app_name: Название приложения
            
        Returns:
            Challenge ID
        """
        request = models.CreateChallengeRequest(app_name=app_name)
        return self.client._request(
            "POST",
            "/auth/challenges",
            data=request,
            response_model=models.CreateChallengeResponse
        )
    
    def create_api_key(self, challenge_id: str, code: str) -> str:
        """
        Создать API ключ используя код из десктоп приложения
        
        Args:
            challenge_id: ID из create_challenge
            code: 4-значный код из десктоп приложения
            
        Returns:
            API ключ
        """
        request = models.CreateApiKeyRequest(
            challenge_id=challenge_id,
            code=code
        )
        response = self.client._request(
            "POST",
            "/auth/api_keys",
            data=request,
            response_model=models.CreateApiKeyResponse
        )
        return response.api_key
