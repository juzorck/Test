#!/bin/bash
echo "=== Сборка .exe файла ==="
echo ""

echo "1. Installing dependencies..."
pip install fastapi uvicorn pyinstaller --break-system-packages --target .venv

echo ""
echo "2. Building executable..."
PYTHONPATH=.venv python .venv/pyinstaller --onefile --name household_points --icon=NUL backend/main.py

echo ""
echo "3. Cleaning up..."
if [ -f dist/household_points.exe ]; then
    echo ""
    echo "✅ Готово! Файл: dist/household_points.exe"
    echo ""
    echo "Для запуска:"
    echo "  ./household_points.exe"
    echo ""
    echo "Приложение будет доступно по адресу: http://localhost:8000"
else
    echo ""
    echo "❌ Ошибка сборки"
fi
