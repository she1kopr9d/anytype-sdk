"""Тесты для Anytype SDK"""

import pytest
from anytype import AnytypeClient
from anytype.models import EmojiIcon

def test_client_initialization():
    """Тест инициализации клиента"""
    client = AnytypeClient(api_key="test-key")
    assert client.api_key == "test-key"
    assert client.base_url == "http://127.0.0.1:31009"
    client.close()

def test_emoji_icon():
    """Тест создания эмодзи-иконки"""
    icon = EmojiIcon(emoji="📄")
    assert icon.format == "emoji"
    assert icon.emoji == "📄"
    assert icon.model_dump() == {"format": "emoji", "emoji": "📄"}
