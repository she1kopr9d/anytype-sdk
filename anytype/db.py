from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Generator
from .client import AnytypeClient
from . import models

class AnytypeConnection:
    """Класс, имитирующий подключение к базе данных"""
    
    def __init__(self, client: AnytypeClient, space_id: str):
        self.client = client
        self.space_id = space_id
        self._objects = ObjectsTable(self)
        self._types = TypesTable(self)
        self._properties = PropertiesTable(self)
        self._tags = TagsTable(self)
    
    @property
    def objects(self):
        """Таблица объектов"""
        return self._objects
    
    @property
    def types(self):
        """Таблица типов"""
        return self._types
    
    @property
    def properties(self):
        """Таблица свойств"""
        return self._properties
    
    @property
    def tags(self):
        """Таблица тегов"""
        return self._tags
    
    def query(self, type_key: str) -> 'QueryBuilder':
        """Начать построение запроса к объектам определенного типа"""
        return QueryBuilder(self, type_key)
    
    def close(self):
        """Закрыть соединение"""
        self.client.close()

class ObjectsTable:
    """Таблица объектов - как таблица в БД"""
    
    def __init__(self, conn: AnytypeConnection):
        self.conn = conn
    
    def insert(self, **kwargs) -> models.ObjectWithBody:
        """Вставить новый объект (CREATE)"""
        return self.conn.client.objects.create(
            space_id=self.conn.space_id,
            **kwargs
        )
    
    def get(self, object_id: str) -> models.ObjectWithBody:
        """Получить объект по ID (READ)"""
        return self.conn.client.objects.get(
            space_id=self.conn.space_id,
            object_id=object_id
        )
    
    def update(self, object_id: str, **kwargs) -> models.ObjectWithBody:
        """Обновить объект (UPDATE)"""
        return self.conn.client.objects.update(
            space_id=self.conn.space_id,
            object_id=object_id,
            **kwargs
        )
    
    def delete(self, object_id: str) -> models.ObjectWithBody:
        """Удалить объект (DELETE)"""
        return self.conn.client.objects.delete(
            space_id=self.conn.space_id,
            object_id=object_id
        )
    
    def find(self, **filters) -> List[models.Object]:
        """Найти объекты по фильтрам (SELECT)"""
        result = self.conn.client.objects.list(
            space_id=self.conn.space_id,
            filters=filters
        )
        return result.data

class QueryBuilder:
    """Построитель запросов - как SQLAlchemy или Django ORM"""
    
    def __init__(self, conn: AnytypeConnection, type_key: str):
        self.conn = conn
        self.type_key = type_key
        self._filters = []
        self._limit = 100
        self._offset = 0
        self._order_by = None
        self._order_dir = "asc"
    
    def filter(self, **conditions):
        """Добавить условия фильтрации"""
        for key, value in conditions.items():
            if "__" in key:
                field, op = key.split("__")
            else:
                field, op = key, "eq"
            
            self._filters.append({
                "property_key": field,
                "condition": self._map_operator(op),
                "value": value
            })
        return self
    
    def _map_operator(self, op: str) -> str:
        """Маппинг операторов Django-like на операторы Anytype"""
        mapping = {
            "eq": "eq",
            "exact": "eq",
            "ne": "ne",
            "gt": "gt",
            "gte": "gte",
            "lt": "lt",
            "lte": "lte",
            "contains": "contains",
            "icontains": "contains",
            "in": "in",
            "isnull": "empty",
            "notnull": "nempty"
        }
        return mapping.get(op, "eq")
    
    def limit(self, limit: int):
        self._limit = min(limit, 1000)
        return self
    
    def offset(self, offset: int):
        self._offset = offset
        return self
    
    def order_by(self, field: str, direction: str = "asc"):
        self._order_by = field
        self._order_dir = direction
        return self
    
    def all(self) -> List[models.Object]:
        """Выполнить запрос и вернуть все результаты"""
        # Здесь нужно построить FilterExpression из _filters
        result = self.conn.client.search.search_in_space(
            space_id=self.conn.space_id,
            types=[self.type_key],
            offset=self._offset,
            limit=self._limit
        )
        return result.data
    
    def first(self) -> Optional[models.Object]:
        """Вернуть первый результат"""
        self._limit = 1
        results = self.all()
        return results[0] if results else None
    
    def count(self) -> int:
        """Вернуть количество результатов"""
        result = self.conn.client.search.search_in_space(
            space_id=self.conn.space_id,
            types=[self.type_key],
            offset=0,
            limit=1
        )
        return result.pagination.total

class TypesTable:
    def __init__(self, conn: AnytypeConnection):
        self.conn = conn
    
    def list(self) -> List[models.Type]:
        result = self.conn.client.types.list(space_id=self.conn.space_id)
        return result.data
    
    def get(self, type_id: str) -> models.Type:
        return self.conn.client.types.get(
            space_id=self.conn.space_id,
            type_id=type_id
        )
    
    def create(self, **kwargs) -> models.Type:
        return self.conn.client.types.create(
            space_id=self.conn.space_id,
            **kwargs
        )

class PropertiesTable:
    def __init__(self, conn: AnytypeConnection):
        self.conn = conn
    
    def list(self) -> List[models.Property]:
        result = self.conn.client.properties.list(space_id=self.conn.space_id)
        return result.data
    
    def get(self, property_id: str) -> models.Property:
        return self.conn.client.properties.get(
            space_id=self.conn.space_id,
            property_id=property_id
        )
    
    def create(self, **kwargs) -> models.Property:
        return self.conn.client.properties.create(
            space_id=self.conn.space_id,
            **kwargs
        )

class TagsTable:
    def __init__(self, conn: AnytypeConnection):
        self.conn = conn
    
    def list(self, property_id: str) -> List[models.Tag]:
        result = self.conn.client.tags.list(
            space_id=self.conn.space_id,
            property_id=property_id
        )
        return result.data
    
    def get(self, property_id: str, tag_id: str) -> models.Tag:
        return self.conn.client.tags.get(
            space_id=self.conn.space_id,
            property_id=property_id,
            tag_id=tag_id
        )
    
    def create(self, property_id: str, **kwargs) -> models.Tag:
        return self.conn.client.tags.create(
            space_id=self.conn.space_id,
            property_id=property_id,
            **kwargs
        )

# Фабрика подключений
class AnytypeDatabase:
    def __init__(self, api_key: str, base_url: str = "http://127.0.0.1:31009"):
        self.api_key = api_key
        self.base_url = base_url
    
    @contextmanager
    def connect(self, space_id: str) -> Generator[AnytypeConnection, None, None]:
        """Контекстный менеджер для подключения к пространству"""
        client = AnytypeClient(api_key=self.api_key, base_url=self.base_url)
        conn = AnytypeConnection(client, space_id)
        try:
            yield conn
        finally:
            conn.close()
    
    def get_space(self, space_id: str) -> AnytypeConnection:
        """Получить подключение к пространству (без контекстного менеджера)"""
        client = AnytypeClient(api_key=self.api_key, base_url=self.base_url)
        return AnytypeConnection(client, space_id)
