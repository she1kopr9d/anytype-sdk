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
        title_field: str = "name"  # Какое поле использовать как заголовок
    
    @classmethod
    def get_type_key(cls) -> str:
        return getattr(cls.Meta, 'type_key', cls.__name__.lower())
    
    @classmethod
    def get_title_field(cls) -> str:
        """Возвращает название поля для заголовка объекта"""
        return getattr(cls.Meta, 'title_field', 'name')
    
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
                elif hasattr(prop, 'select') and prop.select is not None:
                    data[prop.key] = prop.select
                elif hasattr(prop, 'multi_select') and prop.multi_select is not None:
                    data[prop.key] = prop.multi_select
                elif hasattr(prop, 'url') and prop.url is not None:
                    data[prop.key] = prop.url
                elif hasattr(prop, 'email') and prop.email is not None:
                    data[prop.key] = prop.email
                elif hasattr(prop, 'phone') and prop.phone is not None:
                    data[prop.key] = prop.phone
                elif hasattr(prop, 'files') and prop.files is not None:
                    data[prop.key] = prop.files
                elif hasattr(prop, 'objects') and prop.objects is not None:
                    data[prop.key] = prop.objects
        
        # Название объекта может быть в разных полях
        if hasattr(obj, 'name') and obj.name:
            data['name'] = obj.name
        elif hasattr(obj, 'title') and obj.title:
            data['title'] = obj.title
        elif hasattr(obj, 'display_name') and obj.display_name:
            data['display_name'] = obj.display_name
        
        return cls(**data)
    
    def to_properties(self) -> List[models.PropertyLink]:
        """Преобразовать модель в список свойств для Anytype"""
        properties = []
        
        for key, value in self.model_dump(exclude={'id', 'space_id'}).items():
            if value is not None and key != self.get_title_field():
                if isinstance(value, str):
                    properties.append(models.TextPropertyLink(key=key, text=value))
                elif isinstance(value, (int, float)):
                    properties.append(models.NumberPropertyLink(key=key, number=value))
                elif isinstance(value, bool):
                    properties.append(models.CheckboxPropertyLink(key=key, checkbox=value))
                elif isinstance(value, datetime):
                    properties.append(models.DatePropertyLink(key=key, date=value.isoformat()))
                elif isinstance(value, list):
                    # Предполагаем, что это multi_select
                    properties.append(models.MultiSelectPropertyLink(key=key, multi_select=value))
        
        return properties
    
    def to_create_payload(self) -> Dict[str, Any]:
        """Создает payload для создания объекта в API"""
        payload = {
            "type_key": self.get_type_key()
        }
        
        # Добавляем заголовок (может быть name, title и т.д.)
        title_field = self.get_title_field()
        title_value = getattr(self, title_field, None)
        if title_value:
            payload[title_field] = title_value
        
        # Добавляем свойства
        properties = self.to_properties()
        if properties:
            # Преобразуем список свойств в нужный формат
            payload["properties"] = [
                {"key": p.key, "value": p.text if hasattr(p, 'text') else 
                                  p.number if hasattr(p, 'number') else
                                  p.checkbox if hasattr(p, 'checkbox') else
                                  p.date if hasattr(p, 'date') else
                                  p.multi_select if hasattr(p, 'multi_select') else
                                  p.select if hasattr(p, 'select') else
                                  p.url if hasattr(p, 'url') else
                                  p.email if hasattr(p, 'email') else
                                  p.phone if hasattr(p, 'phone') else
                                  p.files if hasattr(p, 'files') else
                                  p.objects if hasattr(p, 'objects') else None}
                for p in properties
            ]
        
        return payload

class Page(Model):
    """Модель для страницы"""
    
    name: Optional[str] = None
    title: Optional[str] = None  # Добавляем альтернативное поле
    content: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    
    class Meta:
        type_key = "page"
        title_field = "name"  # Пробуем name сначала

class Task(Model):
    """Модель для задачи"""
    
    name: Optional[str] = None
    title: Optional[str] = None  # Добавляем альтернативное поле
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False
    
    class Meta:
        type_key = "task"
        title_field = "name"  # Пробуем name сначала

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
            # Используем прямой API клиент для создания
            # с правильным форматом данных
            try:
                # Пробуем создать через objects.insert
                result = self.conn.objects.insert(
                    type_key=model.get_type_key(),
                    **{model.get_title_field(): getattr(model, model.get_title_field(), None)}
                )
                
                # Если объект создан, обновляем его ID
                if hasattr(result, 'id'):
                    model.id = result.id
                    
            except Exception as e:
                # Если не получилось, пробуем через прямой API
                import httpx
                headers = {"Authorization": f"Bearer {self.conn.client.api_key}"}
                
                payload = model.to_create_payload()
                
                with httpx.Client(base_url=self.conn.client.base_url, headers=headers) as client:
                    response = client.post(f"/v1/spaces/{self.conn.space_id}/objects", json=payload)
                    if response.status_code in [200, 201]:
                        data = response.json()
                        if 'object' in data and 'id' in data['object']:
                            model.id = data['object']['id']
                    else:
                        raise Exception(f"Failed to create object: {response.text}")
        
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
    
    @property
    def client(self):
        """Доступ к внутреннему клиенту для прямых запросов"""
        return self._db.client