from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Type, TypeVar, Generic, Generator
from datetime import datetime
from pydantic import BaseModel
from . import models
from .db import AnytypeDatabase, AnytypeConnection

T = TypeVar('T', bound='Model')

class Model(BaseModel):
    """Базовый класс для всех моделей ORM"""
    
    id: Optional[str] = None
    space_id: Optional[str] = None
    
    class Meta:
        type_key: str = ""
    
    @classmethod
    def get_type_key(cls) -> str:
        return getattr(cls.Meta, 'type_key', cls.__name__.lower())
    
    @classmethod
    def from_anytype_object(cls, obj: models.Object) -> 'Model':
        """Создать модель из Anytype объекта"""
        data = {"id": obj.id, "space_id": obj.space_id}
        
        # Маппинг свойств Anytype на атрибуты модели
        if obj.properties:
            for prop in obj.properties:
                if hasattr(prop, 'text') and prop.text is not None:
                    data[prop.key] = prop.text
                elif hasattr(prop, 'number') and prop.number is not None:
                    data[prop.key] = prop.number
                elif hasattr(prop, 'checkbox') and prop.checkbox is not None:
                    data[prop.key] = prop.checkbox
                elif hasattr(prop, 'date') and prop.date is not None:
                    data[prop.key] = prop.date
                # ... другие типы
        
        if obj.name:
            data['name'] = obj.name
        
        return cls(**data)
    
    def to_properties(self) -> List[models.PropertyLink]:
        """Преобразовать модель в список свойств для Anytype"""
        properties = []
        
        for key, value in self.model_dump(exclude={'id', 'space_id'}).items():
            if value is not None:
                if isinstance(value, str):
                    properties.append(models.TextPropertyLink(key=key, text=value))
                elif isinstance(value, (int, float)):
                    properties.append(models.NumberPropertyLink(key=key, number=value))
                elif isinstance(value, bool):
                    properties.append(models.CheckboxPropertyLink(key=key, checkbox=value))
                elif isinstance(value, datetime):
                    properties.append(models.DatePropertyLink(key=key, date=value.isoformat()))
                # ... другие типы
        
        return properties

class Page(Model):
    """Модель для страницы"""
    
    name: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    
    class Meta:
        type_key = "page"

class Task(Model):
    """Модель для задачи"""
    
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False
    
    class Meta:
        type_key = "task"

class Session:
    """Сессия для работы с Anytype как с ORM"""
    
    def __init__(self, conn: AnytypeConnection):
        self.conn = conn
        self._new_objects = []
        self._dirty_objects = []
    
    def add(self, model: Model):
        """Добавить объект для создания"""
        self._new_objects.append(model)
    
    def get(self, model_class: Type[T], id: str) -> Optional[T]:
        """Получить объект по ID"""
        obj = self.conn.objects.get(id)
        if obj and obj.type and obj.type.key == model_class.get_type_key():
            return model_class.from_anytype_object(obj)
        return None
    
    def query(self, model_class: Type[T]) -> 'Query[T]':
        """Создать запрос для модели"""
        return Query(self.conn, model_class)
    
    def commit(self):
        """Сохранить все изменения"""
        for model in self._new_objects:
            self.conn.objects.insert(
                type_key=model.get_type_key(),
                name=getattr(model, 'name', None),
                properties=model.to_properties()
            )
        self._new_objects.clear()
        self._dirty_objects.clear()
    
    def close(self):
        """Закрыть сессию"""
        self.conn.close()

class Query(Generic[T]):
    """Построитель запросов для ORM"""
    
    def __init__(self, conn: AnytypeConnection, model_class: Type[T]):
        self.conn = conn
        self.model_class = model_class
        self._builder = conn.query(model_class.get_type_key())
    
    def filter(self, **kwargs) -> 'Query[T]':
        self._builder.filter(**kwargs)
        return self
    
    def all(self) -> List[T]:
        objects = self._builder.all()
        return [self.model_class.from_anytype_object(obj) for obj in objects]
    
    def first(self) -> Optional[T]:
        obj = self._builder.first()
        return self.model_class.from_anytype_object(obj) if obj else None
    
    def count(self) -> int:
        return self._builder.count()
    
    def limit(self, limit: int) -> 'Query[T]':
        self._builder.limit(limit)
        return self
    
    def offset(self, offset: int) -> 'Query[T]':
        self._builder.offset(offset)
        return self

# Фабрика для создания подключений
class Anytype:
    def __init__(self, api_key: str, base_url: str = "http://127.0.0.1:31009"):
        self.api_key = api_key
        self.base_url = base_url
        self._db = AnytypeDatabase(api_key, base_url)
    
    @contextmanager
    def connect(self, space_id: str) -> Generator[Session, None, None]:
        """Подключиться к пространству"""
        with self._db.connect(space_id) as conn:
            yield Session(conn)
    
    def session(self, space_id: str) -> Session:
        """Создать сессию для пространства"""
        return Session(self._db.get_space(space_id))
