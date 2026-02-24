"""
Anytype Python SDK
~~~~~~~~~~~~~~~~~~

Python библиотека для работы с Anytype API с интерфейсом, похожим на работу с базой данных.

Основное использование:
    >>> from anytype import Anytype
    >>> at = Anytype(api_key="your-api-key")
    >>> with at.connect("space-id") as conn:
    ...     page = conn.objects.insert(type_key="page", name="Моя страница")
    ...     pages = conn.objects.find(name__contains="тест")

Доступные модули:
    - AnytypeClient - прямой клиент API
    - AnytypeDatabase - интерфейс как у БД
    - Anytype - ORM стиль с моделями
    - AnytypeDB - максимально простой интерфейс
"""

__version__ = "0.1.0"

from .client import AnytypeClient
from . import models
from . import exceptions
from . import utils
from .db import AnytypeDatabase, AnytypeConnection
from .orm import Anytype, Model, Session, Page, Task
from .simple import AnytypeDB

__all__ = [
    "AnytypeClient",
    "AnytypeDatabase",
    "AnytypeConnection",
    "Anytype",
    "Model",
    "Session",
    "Page",
    "Task",
    "AnytypeDB",
    "models",
    "exceptions",
    "utils",
]
