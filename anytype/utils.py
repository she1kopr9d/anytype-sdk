from typing import Optional, Dict, Any, List, Generator
from datetime import datetime
import re

class FilterBuilder:
    """Утилита для построения сложных фильтров"""
    
    @staticmethod
    def text_equals(key: str, value: str) -> Dict:
        return {"property_key": key, "condition": "eq", "text": value}
    
    @staticmethod
    def text_contains(key: str, value: str) -> Dict:
        return {"property_key": key, "condition": "contains", "text": value}
    
    @staticmethod
    def number_gt(key: str, value: float) -> Dict:
        return {"property_key": key, "condition": "gt", "number": value}
    
    @staticmethod
    def number_lt(key: str, value: float) -> Dict:
        return {"property_key": key, "condition": "lt", "number": value}
    
    @staticmethod
    def date_after(key: str, date: datetime) -> Dict:
        return {
            "property_key": key,
            "condition": "gt",
            "date": date.isoformat()
        }
    
    @staticmethod
    def date_before(key: str, date: datetime) -> Dict:
        return {
            "property_key": key,
            "condition": "lt",
            "date": date.isoformat()
        }
    
    @staticmethod
    def checkbox_is(key: str, value: bool) -> Dict:
        return {"property_key": key, "condition": "eq", "checkbox": value}
    
    @staticmethod
    def select_in(key: str, values: list) -> Dict:
        return {"property_key": key, "condition": "in", "select": values}
    
    @staticmethod
    def multi_select_contains(key: str, values: list) -> Dict:
        return {
            "property_key": key,
            "condition": "contains",
            "multi_select": values
        }
    
    @staticmethod
    def is_empty(key: str) -> Dict:
        return {"property_key": key, "condition": "empty"}
    
    @staticmethod
    def not_empty(key: str) -> Dict:
        return {"property_key": key, "condition": "nempty"}

class PaginationHelper:
    """Утилита для работы с пагинацией"""
    
    def __init__(self, client, method, *args, **kwargs):
        self.client = client
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.page_size = kwargs.get('limit', 100)
        self.offset = 0
        self.total = None
        self.items = []
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.total is not None and self.offset >= self.total:
            raise StopIteration
        
        self.kwargs['offset'] = self.offset
        self.kwargs['limit'] = self.page_size
        
        response = self.method(*self.args, **self.kwargs)
        
        if self.total is None:
            self.total = response.pagination.total
        
        self.items = response.data
        self.offset += len(self.items)
        
        return self.items
    
    def all(self):
        """Получить все элементы сразу"""
        results = []
        for page in self:
            results.extend(page)
        return results

def paginate(method, *args, **kwargs):
    """Хелпер для пагинации"""
    return PaginationHelper(None, method, *args, **kwargs)

def to_snake_case(name: str) -> str:
    """Преобразовать строку в snake_case"""
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    name = re.sub(r'[-\s]+', '_', name)
    return name

def create_emoji_icon(emoji: str) -> Dict:
    """Создать иконку-эмодзи"""
    return {"format": "emoji", "emoji": emoji}

def create_file_icon(file_id: str) -> Dict:
    """Создать иконку из файла"""
    return {"format": "file", "file": file_id}

def create_named_icon(name: str, color: Optional[str] = None) -> Dict:
    """Создать именованную иконку"""
    icon = {"format": "icon", "name": name}
    if color:
        icon["color"] = color
    return icon
