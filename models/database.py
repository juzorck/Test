import sqlite3
from typing import Dict, List, Optional
from models.model import Item

DB_PATH = "household_points.db"

def get_db() -> sqlite3.Connection:
    """Получить подключение к базе данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Инициализировать базу данных."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            points INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            paid INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cashback (
            user TEXT PRIMARY KEY,
            points INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def create_item(name: str, points: int) -> None:
    """Создать новую задачу."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, points) VALUES (?, ?)", (name, points))
    conn.commit()
    conn.close()

def get_items() -> Dict[int, Item]:
    """Получить все задачи."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()
    return {row['id']: Item(row['name'], row['points'], bool(row['completed']), bool(row['paid'])) for row in rows}

def set_completed(item_id: int, completed_by: str) -> None:
    """Отметить задачу выполненной и начислить баллы."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем задачу
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    
    if item and not item['completed']:
        # Обновляем задачу
        cursor.execute("UPDATE items SET completed = 1, paid = 1 WHERE id = ?", (item_id,))
        
        # Начисляем баллы
        cursor.execute("INSERT INTO cashback (user, points) VALUES (?, ?) ON CONFLICT(user) DO UPDATE SET points = points + ?",
                       (completed_by, item['points'], item['points']))
        
        conn.commit()
    
    conn.close()

def pay(prize_id: int, user: str) -> bool:
    """Обменять баллы на награду. Возвращает True если успешно."""
    prizes = {1: 50, 2: 100, 3: 30}
    
    if prize_id not in prizes:
        return False
    
    cost = prizes[prize_id]
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем текущий баланс
    cursor.execute("SELECT points FROM cashback WHERE user = ?", (user,))
    row = cursor.fetchone()
    current_points = row['points'] if row else 0
    
    if current_points >= cost:
        cursor.execute("UPDATE cashback SET points = points - ? WHERE user = ?", (cost, user))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

def get_cashback(user: str) -> int:
    """Получить баланс пользователя."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM cashback WHERE user = ?", (user,))
    row = cursor.fetchone()
    conn.close()
    return row['points'] if row else 0

def get_pay(user: str) -> List[Item]:
    """Получить историю выполненных задач."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE paid = 1 AND completed = 1")
    rows = cursor.fetchall()
    conn.close()
    return [Item(row['name'], row['points'], bool(row['completed']), bool(row['paid'])) for row in rows]
