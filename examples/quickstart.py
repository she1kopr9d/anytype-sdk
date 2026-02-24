#!/usr/bin/env python3
"""
Быстрый старт с Anytype SDK
"""

from anytype import Anytype
from anytype.models import EmojiIcon

def main():
    # Инициализация
    at = Anytype(api_key="your-api-key")
    
    # Подключение к пространству
    with at.connect("your-space-id") as conn:
        # Создание страницы
        page = conn.objects.insert(
            type_key="page",
            name="Привет, мир!",
            body="# Заголовок\n\nЭто моя первая страница из SDK",
            icon=EmojiIcon(emoji="📄")
        )
        print(f"✅ Создана страница: {page.name} (ID: {page.id})")
        
        # Поиск страниц
        pages = conn.objects.find(name__contains="мир")
        print(f"📄 Найдено страниц: {len(pages)}")
        
        # Обновление
        if pages:
            updated = conn.objects.update(
                pages[0].id,
                name="Обновленное название"
            )
            print(f"🔄 Обновлено: {updated.name}")

if __name__ == "__main__":
    main()
