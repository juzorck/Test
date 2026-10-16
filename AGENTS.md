# AGENTS.md

## Household tasks application

### Application structure
- Backend: `backend/main.py` (FastAPI), models: `models/model.py`
- Static files: `static/style.css`
- Config: `pyproject.toml`

### User interaction
- Two users: "you" and "girlfriend"
- Tasks have name, points
- Cashback is earned by completing tasks
- Prizes can be exchanged for points

### Commands
- Run with `pip install -e . && run` or `uvicorn backend.main:app --reload`
