# BLOG API

## Описание

BLOG API — это API для управления публикациями блога. Этот API позволяет пользователям создавать, получать, и удалять публикации, а также искать публикации по тегам. API построен с использованием FastAPI, поддерживает асинхронные операции с aiosqlite и использует Pydantic для валидации данных.

## Установка

### Необходимые зависимости

- Python 3.10 или выше
- FastAPI
- Uvicorn
- Pydantic
- Aiosqlite

### Шаги по установке

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Kene33/blog-api.git
   cd blog-api
   ```

2. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Запустите приложение:**

   ```bash
   python main.py
   ```

## Эндпоинты API

### **1. Получение всех постов**

- **GET** `/api/posts`

  Возвращает список всех постов.

### **2. Получение публикаций пользователя**

- **GET** `/api/posts/user/{user_id}`

  Возвращает все посты пользователя.

### **3. Создание публикации**

- **POST** `/api/posts`

  Тело запроса:

  ```json
  {
      "user_id": 2311,
      "username": "kenee33",
      "title": "Название",
      "content": "Содержимое",
      "category": "Категория",
      "tags": ["tag1", "tag2"]
  }
  ```

### **4. Удаление поста**

- **DELETE** `/api/posts`

  Удаляет публикацию по ID.

## TODO
- Добавить JWT-аутентификацию. [DONE]
- Создать небольшой сайт с использованием этого API. [IN PROGRESS]
