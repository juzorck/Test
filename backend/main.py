from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from html import escape

from models.model import Item, create_item, get_items, set_completed, pay, get_pay, get_cashback

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

items: dict[int, Item] = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = request.query_params.get("user", "you")
    items_list = get_items()
    
    tasks_html = "".join(f"<li>{escape(items_list[i].name)} - {escape(str(items_list[i].points))} баллов</li>" for i in items_list)
    pay_html = "".join(f"<li>{escape(get_pay(user)[i].name)} - {escape(str(get_pay(user)[i].points))} баллов</li>" for i in get_pay(user))
    options_html = "".join(f'<option value="{i}">{escape(items_list[i].name)}</option>' for i in items_list)
    
    return HTMLResponse(f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система баллов</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Система баллов</h1>
        <div class="user-toggle">
            <a href="?user=you" class="user-link{' active' if user == 'you' else ''}">Вы</a>
            <a href="?user=girlfriend" class="user-link{' active' if user == 'girlfriend' else ''}">Девушка</a>
        </div>
        <div class="user-info">
            <p>Текущий пользователь: <span class="highlight">{escape(user)}</span></p>
            <p>Баллы: <span class="highlight">{escape(str(get_cashback(user)))}</span></p>
        </div>
        <div class="action-menu">
            <button onclick="showTab('tasks')">Задачи</button>
            <button onclick="showTab('payments')">Оплата</button>
            <button onclick="showTab('cashback')">Кэшбэк</button>
        </div>
        <div id="tasks" class="tab-content">
            <h2>Задачи</h2>
            <form method="post" action="/tasks" class="task-form">
                <input type="text" name="task" placeholder="Название задачи" required>
                <input type="number" name="points" placeholder="Баллы" required>
                <button type="submit">Добавить задачу</button>
            </form>
            <div class="task-list">
                <h3>Все задачи:</h3>
                <ul>
                    {tasks_html}
                </ul>
            </div>
        </div>
        <div id="payments" class="tab-content" style="display: none;">
            <h2>Оплата</h2>
            <p>Выберите задачу и нажмите "Отметить выполненной", чтобы получить баллы</p>
            <form method="post" action="/pay">
                <select name="task_id">
                    {options_html}
                </select>
                <input type="hidden" name="user" value="{escape(user)}">
                <button type="submit">Отметить выполненной</button>
            </form>
            <h3>История выполненных задач:</h3>
            <ul>
                {pay_html}
            </ul>
        </div>
        <div id="cashback" class="tab-content" style="display: none;">
            <h2>Кэшбэк</h2>
            <p>Выберите награду и нажмите "Обменять", чтобы потратить баллы</p>
            <form method="post" action="/cashback">
                <select name="prize_id">
                    <option value="1">Побегать по магазинам (50 баллов)</option>
                    <option value="2">Сходить в кино (100 баллов)</option>
                    <option value="3">Сделать ужин (30 баллов)</option>
                </select>
                <input type="hidden" name="user" value="{escape(user)}">
                <button type="submit">Обменять</button>
            </form>
        </div>
    </div>
    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            document.getElementById(tabId).style.display = 'block';
        }}
        document.addEventListener('DOMContentLoaded', () => showTab('tasks'));
    </script>
</body>
</html>""")

@app.post("/tasks")
async def add_task(request: Request, task: str = Form(...), points: int = Form(...)):
    create_item(task, points)
    return RedirectResponse(url="/", status_code=303)

@app.post("/pay")
async def pay_task(request: Request, task_id: int = Form(...), user: str = Form(...)):
    set_completed(task_id, user)
    return RedirectResponse(url="/", status_code=303)

@app.post("/cashback")
async def cashback_prize(request: Request, prize_id: int = Form(...), user: str = Form(...)):
    pay(prize_id, user)
    return RedirectResponse(url="/", status_code=303)
