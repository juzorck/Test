#!/usr/bin/env python3
"""Запуск FastAPI приложения с инициализацией базы данных."""

import sys
import os

# Добавляем путь к .venv в sys.path
venv_path = os.path.join(os.path.dirname(__file__), '.venv')
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

from uvicorn import run
from backend.main import app

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8000, log_level='info')
