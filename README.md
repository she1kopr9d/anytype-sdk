# Anytype Python SDK

<div align="center">

Python библиотека для работы с Anytype API с интерфейсом, похожим на работу с базой данных.

</div>

## ✨ Возможности

- 🔑 **Полная аутентификация** - создание API ключей через десктоп приложение
- 📦 **Управление пространствами** - создание, получение, обновление
- 📄 **Работа с объектами** - CRUD операции, поиск, фильтрация
- 🏷️ **Типы и свойства** - создание кастомных типов и свойств
- 🔍 **Поиск** - глобальный и в пределах пространства
- 👥 **Участники** - управление доступом к пространствам
- 🎨 **Иконки** - поддержка эмодзи, файлов и именованных иконок
- 📦 **Несколько интерфейсов** - от простого до ORM

## 🚀 Установка

```bash
# Локальная установка из директории
pip install -e .

# Или через pip из GitHub
pip install git+https://github.com/she1kopr9d/anytype-sdk.git
```

## 📖 Быстрый старт

### 1️⃣ Аутентификация

```python
from anytype import AnytypeClient

client = AnytypeClient()

# Создать challenge
challenge = client.auth.create_challenge(app_name="my_app")
print(f"Challenge ID: {challenge.challenge_id}")
print("Введите 4-значный код из десктоп приложения")

# Получить API ключ
code = input("Код: ")
api_key = client.auth.create_api_key(challenge.challenge_id, code)
print(f"API ключ: {api_key}")

client.set_api_key(api_key)
```

### 2️⃣ Интерфейс как у базы данных

```python
from anytype import Anytype

at = Anytype(api_key="your-api-key")

with at.connect("space-id") as conn:
    # Вставка
    page = conn.objects.insert(
        type_key="page",
        name="Моя страница",
        body="# Привет мир!"
    )
    print(f"Создана страница: {page.name}")
    
    # Поиск
    pages = conn.objects.find(name__contains="тест")
    print(f"Найдено страниц: {len(pages)}")
```

### 3️⃣ ORM стиль

```python
from anytype import Anytype, Task

at = Anytype(api_key="your-api-key")

with at.connect("space-id") as session:
    # Создание задачи
    task = Task(
        name="Написать код",
        description="Реализовать библиотеку",
        status="in_progress",
        priority="high"
    )
    session.add(task)
    session.commit()
    
    # Поиск задач
    tasks = session.query(Task).filter(status="done").all()
```

## 📚 Документация

Полная документация доступна в [Wiki](https://github.com/yourusername/anytype-sdk/wiki).

## 🧪 Разработка

```bash
# Установка в режиме разработки
pip install -e .

# Запуск тестов
pytest tests/

# Форматирование кода
black anytype/ tests/
isort anytype/ tests/
```

## 📄 Лицензия

MIT License
