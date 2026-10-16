class Item:
    def __init__(self, name: str, points: int, completed: bool = False, paid: bool = False):
        self.name = name
        self.points = points
        self.completed = completed
        self.paid = paid

from typing import Dict, List
from models.model import Item

items: Dict[int, Item] = {}

def create_item(name: str, points: int) -> None:
    global items
    new_id = max(items.keys(), default=0) + 1
    items[new_id] = Item(name, points)

def get_items() -> Dict[int, Item]:
    return items

def set_completed(item_id: int, completed_by: str) -> None:
    if item_id in items and not items[item_id].completed:
        items[item_id].completed = True
        items[item_id].paid = True
        cashback[completed_by] = cashback.get(completed_by, 0) + items[item_id].points

def pay(prize_id: int, user: str) -> None:
    prizes = {1: 50, 2: 100, 3: 30}
    if prize_id in prizes and cashback.get(user, 0) >= prizes[prize_id]:
        cashback[user] -= prizes[prize_id]

cashback: Dict[str, int] = {}

def get_cashback(user: str) -> int:
    return cashback.get(user, 0)

def get_pay(user: str) -> List[Item]:
    return [item for item in items.values() if item.paid and item.completed]
