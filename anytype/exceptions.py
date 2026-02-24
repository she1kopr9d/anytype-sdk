from typing import Optional, Dict, Any

class AnytypeAPIError(Exception):
    """Базовое исключение для Anytype API"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.response_data = response_data
        super().__init__(self.message)
    
    def __str__(self):
        parts = []
        if self.status_code:
            parts.append(f"[{self.status_code}]")
        if self.error_code:
            parts.append(f"{self.error_code}:")
        parts.append(self.message)
        return " ".join(parts)

class UnauthorizedError(AnytypeAPIError):
    """Ошибка аутентификации (401)"""
    pass

class ForbiddenError(AnytypeAPIError):
    """Ошибка доступа (403)"""
    pass

class NotFoundError(AnytypeAPIError):
    """Ресурс не найден (404)"""
    pass

class ResourceGoneError(AnytypeAPIError):
    """Ресурс удален (410)"""
    pass

class ValidationError(AnytypeAPIError):
    """Ошибка валидации (400)"""
    pass

class RateLimitError(AnytypeAPIError):
    """Превышен лимит запросов (429)"""
    pass
