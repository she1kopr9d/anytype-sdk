import httpx
from typing import Optional, Dict, Any, List, Union, TypeVar, Generic
from pydantic import BaseModel
from . import models
from .exceptions import (
    AnytypeAPIError, 
    UnauthorizedError, 
    NotFoundError, 
    ValidationError,
    RateLimitError,
    ForbiddenError,
    ResourceGoneError
)

T = TypeVar('T')

class AnytypeClient:
    """
    Главный клиент для работы с Anytype API.
    
    Пример использования:
    ```python
    client = AnytypeClient(api_key="your-api-key")
    
    # Получить все пространства
    spaces = client.spaces.list()
    
    # Создать объект
    obj = client.objects.create(
        space_id=spaces.data[0].id,
        type_key="page",
        name="Моя страница",
        body="Содержимое страницы"
    )
    ```
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "http://127.0.0.1:31009",
        api_version: str = "2025-11-08",
        timeout: float = 30.0
    ):
        self.base_url = base_url.rstrip('/')
        self.api_version = api_version
        self.timeout = timeout
        
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._build_headers(api_key)
        )
        
        # Инициализация API модулей
        from .api import (
            AuthAPI, SpacesAPI, ObjectsAPI, PropertiesAPI,
            TypesAPI, TemplatesAPI, ListsAPI, MembersAPI,
            SearchAPI, TagsAPI
        )
        
        self.auth = AuthAPI(self)
        self.spaces = SpacesAPI(self)
        self.objects = ObjectsAPI(self)
        self.properties = PropertiesAPI(self)
        self.types = TypesAPI(self)
        self.templates = TemplatesAPI(self)
        self.lists = ListsAPI(self)
        self.members = MembersAPI(self)
        self.search = SearchAPI(self)
        self.tags = TagsAPI(self)
    
    def _build_headers(self, api_key: Optional[str]) -> Dict[str, str]:
        headers = {
            "Anytype-Version": self.api_version,
            "Content-Type": "application/json",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        return headers
    
    def set_api_key(self, api_key: str):
        """Обновить API ключ"""
        self.client.headers["Authorization"] = f"Bearer {api_key}"
    
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[BaseModel] = None,
        response_model: Optional[Type[T]] = None
    ) -> Union[Dict[str, Any], T]:
        """Базовый метод для выполнения HTTP запросов"""
        url = f"/v1{path}"
        
        # Convert params to proper format
        if params:
            # Convert enum values to strings
            clean_params = {}
            for key, value in params.items():
                if value is not None:
                    clean_params[key] = value
            params = clean_params
        
        # Convert data to dict
        json_data = None
        if data:
            json_data = data.model_dump(exclude_none=True)
        
        try:
            response = self.client.request(
                method=method,
                url=url,
                params=params,
                json=json_data
            )
            
            # Handle errors
            if response.status_code >= 400:
                self._handle_error(response)
            
            # Parse response
            if response.status_code == 200 or response.status_code == 201:
                if response_model:
                    return response_model.model_validate(response.json())
                return response.json()
            elif response.status_code == 204:
                return None
            
            return response.json()
            
        except httpx.TimeoutException:
            raise AnytypeAPIError("Request timeout")
        except httpx.HTTPError as e:
            raise AnytypeAPIError(f"HTTP error: {str(e)}")
    
    def _handle_error(self, response: httpx.Response):
        """Обработка ошибок API"""
        try:
            error_data = response.json()
        except:
            error_data = {}
        
        status = response.status_code
        message = error_data.get('message', 'Unknown error')
        code = error_data.get('code', 'unknown_error')
        
        if status == 400:
            raise ValidationError(message, status, code, error_data)
        elif status == 401:
            raise UnauthorizedError(message, status, code, error_data)
        elif status == 403:
            raise ForbiddenError(message, status, code, error_data)
        elif status == 404:
            raise NotFoundError(message, status, code, error_data)
        elif status == 410:
            raise ResourceGoneError(message, status, code, error_data)
        elif status == 429:
            raise RateLimitError(message, status, code, error_data)
        else:
            raise AnytypeAPIError(message, status, code, error_data)
    
    def close(self):
        """Закрыть HTTP клиент"""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
