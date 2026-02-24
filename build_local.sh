#!/bin/bash

echo "🔨 Сборка Anytype SDK для локального использования..."

# Очистка старых сборок
echo "🧹 Очистка..."
rm -rf build/ dist/ *.egg-info/

# Сборка пакета
echo "📦 Сборка пакета..."
python -m build

# Создание директории для локального репозитория
mkdir -p local_pypi

# Копирование собранных пакетов
cp dist/* local_pypi/

# Создание простого индекса
echo "📝 Создание локального индекса..."
cat > local_pypi/index.html << 'INNEREOF'
<!DOCTYPE html>
<html>
<head><title>Local PyPI Index</title></head>
<body>
<h1>Local PyPI Index</h1>
<a href="anytype_sdk-0.1.0-py3-none-any.whl">anytype_sdk-0.1.0-py3-none-any.whl</a><br/>
<a href="anytype-sdk-0.1.0.tar.gz">anytype-sdk-0.1.0.tar.gz</a>
</body>
</html>
INNEREOF

echo ""
echo "✅ Готово!"
echo ""
echo "📦 Собранные пакеты в директории dist/:"
ls -la dist/
echo ""
echo "🚀 Способы установки:"
echo "  1. pip install dist/anytype_sdk-0.1.0-py3-none-any.whl"
echo "  2. pip install dist/anytype-sdk-0.1.0.tar.gz"
echo "  3. pip install -e ."
echo "  4. pip install --find-links=local_pypi anytype-sdk"
