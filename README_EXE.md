# Сборка .exe файла

## Требования
- Python 3.10+
- pip

## Установка зависимостей

```bash
pip install fastapi uvicorn pyinstaller --break-system-packages --target .venv
```

## Сборка exe файла

### Windows
```bash
compile_exe.bat
```

### Linux/Mac
```bash
chmod +x compile_exe.sh
./compile_exe.sh
```

## Запуск

После сборки exe файл появится в папке `dist/`:
- **Windows:** `dist/household_points.exe`
- **Linux/Mac:** `dist/household_points`

Запуск:
```bash
household_points.exe
```

Приложение будет доступно по адресу: **http://localhost:8000**

## Структура проекта
- `backend/main.py` - основной код приложения
- `models/model.py` - модели данных
- `static/style.css` - стили
- `pyproject.toml` - конфигурация зависимостей

## Примечание
Приложение использует локальную память для хранения данных. При перезапуске все данные сбрасываются.
Для постоянного хранения необходимо подключить базу данных (SQLite, PostgreSQL и т.д.).
