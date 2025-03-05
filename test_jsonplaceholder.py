import requests
from pydantic import BaseModel, ValidationError
import pytest

# Модель Pydantic для пользователя
class User(BaseModel):
    id: int
    name: str
    username: str
    email: str

# Функция для получения списка пользователей с JSONPlaceholder
def get_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    # Проверка успешного ответа
    response.raise_for_status()
    return response.json()

# Тест для проверки данных пользователей
def test_users():
    users_data = get_users()  # Получаем данные о пользователях

    # Проверяем, что каждый пользователь валиден согласно модели Pydantic
    seen_ids = set()  # Множество для проверки уникальности ID

    for user_data in users_data:
        try:
            user = User(**user_data)  # Валидация с использованием Pydantic
        except ValidationError as e:
            pytest.fail(f"Validation error for user {user_data['id']}: {e}")
        
        # Проверки
        assert user.id > 0  # ID должен быть положительным числом
        assert len(user.name) > 0  # Имя не должно быть пустым
        assert len(user.username) > 0  # Username не должен быть пустым
        assert '@' in user.email  # Email должен содержать '@'

        # Проверка уникальности ID
        assert user.id not in seen_ids, f"Duplicate ID found: {user.id}"
        seen_ids.add(user.id)

# Для запуска теста через pytest можно использовать команду:
# pytest test_users.py --maxfail=1 --disable-warnings -v
