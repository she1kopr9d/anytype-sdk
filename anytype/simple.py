from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Generator
from .client import AnytypeClient

class AnytypeDB:
    """Простой интерфейс как у базы данных"""
    
    def __init__(self, api_key: str, base_url: str = "http://127.0.0.1:31009"):
        self.api_key = api_key
        self.base_url = base_url
    
    @contextmanager
    def connect(self, space_id: str) -> Generator['Connection', None, None]:
        """Подключиться к пространству"""
        client = AnytypeClient(api_key=self.api_key, base_url=self.base_url)
        conn = Connection(client, space_id)
        try:
            yield conn
        finally:
            conn.close()

class Connection:
    """Подключение к пространству"""
    
    def __init__(self, client: AnytypeClient, space_id: str):
        self.client = client
        self.space_id = space_id
    
    def execute(self, query: str, **params) -> Any:
        """Выполнить 'SQL' запрос"""
        # Простой парсинг запросов
        query = query.strip().lower()
        
        if query.startswith('select'):
            return self._select(params)
        elif query.startswith('insert'):
            return self._insert(params)
        elif query.startswith('update'):
            return self._update(params)
        elif query.startswith('delete'):
            return self._delete(params)
        else:
            raise ValueError(f"Unsupported query: {query}")
    
    def _select(self, params):
        type_key = params.get('type')
        filters = params.get('where', {})
        
        result = self.client.objects.list(
            space_id=self.space_id,
            filters=filters
        )
        return result.data
    
    def _insert(self, params):
        return self.client.objects.create(
            space_id=self.space_id,
            **params
        )
    
    def _update(self, params):
        return self.client.objects.update(
            space_id=self.space_id,
            object_id=params['id'],
            **params
        )
    
    def _delete(self, params):
        return self.client.objects.delete(
            space_id=self.space_id,
            object_id=params['id']
        )
    
    def table(self, name: str) -> 'Table':
        """Получить таблицу по имени типа"""
        return Table(self, name)
    
    def close(self):
        self.client.close()

class Table:
    """Таблица (тип объектов)"""
    
    def __init__(self, conn: Connection, type_key: str):
        self.conn = conn
        self.type_key = type_key
    
    def insert(self, **data) -> Any:
        """Вставить запись"""
        return self.conn.client.objects.create(
            space_id=self.conn.space_id,
            type_key=self.type_key,
            **data
        )
    
    def get(self, id: str) -> Any:
        """Получить запись по ID"""
        return self.conn.client.objects.get(
            space_id=self.conn.space_id,
            object_id=id
        )
    
    def find(self, **filters) -> List[Any]:
        """Найти записи"""
        result = self.conn.client.objects.list(
            space_id=self.conn.space_id,
            filters=filters
        )
        return result.data
    
    def update(self, id: str, **data) -> Any:
        """Обновить запись"""
        return self.conn.client.objects.update(
            space_id=self.conn.space_id,
            object_id=id,
            **data
        )
    
    def delete(self, id: str) -> Any:
        """Удалить запись"""
        return self.conn.client.objects.delete(
            space_id=self.conn.space_id,
            object_id=id
        )
