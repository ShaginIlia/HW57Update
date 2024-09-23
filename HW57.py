from fastapi import FastAPI, status, Body, HTTPException, Path, Request
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates2')

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
async def all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get("/user/{user_id}")
async def get_all_users(request: Request, user_id: int) -> HTMLResponse:
    user = next(user for user in users if user.id == user_id)
    return templates.TemplateResponse('users.html', {'request': request, 'user': user})


# Зарегистрировать нового пользователя
@app.post("/user/{username}/{age}")
async def registered_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> str:
    next_id = len(users) + 1 if users else 1
    new_user = User(id=next_id, username=username, age=age)
    users.append(new_user)
    return f'User {new_user} is registered'


def find_user(user_id):
    for user in users:
        if user.id == user_id:
            return user
    raise KeyError("User with ID {} not found".format(user_id))


# Обновить данные пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: str,
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> str:
    try:
        user = find_user(user_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    user.username = username
    user.age = age
    return f'The user {user} is updated'


# Удалить пользователя
@app.delete("/user/{user_id}")
async def delete_user(user_id: str) -> str:
    try:
        user = find_user(user_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    users.pop(user)
    return f'User with id {user_id} was deleted.'
