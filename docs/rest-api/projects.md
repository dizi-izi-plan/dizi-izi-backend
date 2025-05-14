## Resource: projects

Base URI: `/api/v1/projects/`

#### Common **Headers**
-  **Authorization** - `Token .....`

#### Endpoints:

- **GET** `/api/v1/projects/`

  Description: Получение списка проектов принадлежащих пользователю

  Responses:

  Status Code `200 OK`
  ```json
  {
    "data": [
      {
        "id": 0,
        "name": "string",
        "created_at": "2025-05-14T12:00:00"
      }
    ]
  } 
  ```
  Status Code `401 Unauthorized`
  ```json
  {
    "detail": "Учетные данные не были предоставлены."
  }
  ```
  Status Code `403 Forbidden`
  ```json
  {
    "detail": "У вас недостаточно прав для выполнения данного действия." 
  }
  ```

- **POST** `/api/v1/projects/`
    
    Description: Создание проекта
    
    Body:
    ```json
    {
      "name": "string"  
    }
  ```
    Responses:
    
    Status Code `201 Created`
  ```json
  {
    "id": 0,
    "name": "string",
    "created_at": "2025-05-14T12:00:00" 
  }
  ```
  Status Code `400 Bad Request`
  ```json
  {
    "detail": "....."
  }
  ```
  Status Code `401 Unauthorized`
  ```json
  {
    "detail": "Учетные данные не были предоставлены."
  }
  ```
  Status Code `403 Forbidden`
  ```json
  {
    "detail": "Превышен лимит проектов для данного тарифа." 
  }
  ```
  
- **PATCH** `/api/v1/projects/{id}/`

  Description: Редактирование проекта 

  Body:
    ```json
    {
      "name": "string"  
    }
  ```
  Responses:

  Status Code `200 OK`
  ```json
  {
    "id": 0,
    "name": "string",
    "created_at": "2025-05-14T12:00:00" 
  }
  ```
  Status Code `400 Bad Request`
  ```json
  {
    "detail": "....."
  }
  ```
  Status Code `401 Unauthorized`
  ```json
  {
    "detail": "Учетные данные не были предоставлены."
  }
  ```
  Status Code `403 Forbidden`
  ```json
  {
    "detail": "У вас недостаточно прав для выполнения данного действия." 
  }
  ```
  
- **DELETE** `/api/v1/projects/{id}/`

    Description: Удаление проекта 

    Responses:

    Status Code `204 No Content`
    ```
  Без тела ответа
  ```
    Status Code `401 Unauthorized`
  ```json
  {
    "detail": "Учетные данные не были предоставлены."
  }
  ```
  Status Code `403 Forbidden`
  ```json
  {
    "detail": "У вас недостаточно прав для выполнения данного действия." 
  }
  ```
  
- **POST** `/api/v1/projects/{id}/dub`
    
    Description: Дублирование проекта в месте со связанными комнатами
    
    Status Code `201 Created`
  ```json
  {
    "id": 0,
    "name": "string",
    "created_at": "2025-05-14T12:00:00" 
  }
  ```
    Status Code `401 Unauthorized`
  ```json
  {
    "detail": "Учетные данные не были предоставлены."
  }
  ```
  Status Code `403 Forbidden`
  ```json
  {
    "detail": "У вас недостаточно прав для выполнения данного действия." 
  }
  ```
  ИЛИ 
  ```json
  {
    "detail": "Превышен лимит проектов для данного тарифа." 
  }
  ```
    
  