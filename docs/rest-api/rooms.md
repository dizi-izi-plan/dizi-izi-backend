## Resource: Rooms

Base URI: `/api/v1/rooms/`

#### Common **Headers**
-  **Authorization** - `Token .....`

#### Endpoints:

- **GET** `/api/v1/rooms/`

    Description: Получение списка комнат принадлежащих пользователю

    Responses:

    Status Code `200 OK`
  ```json
  {
    "data": [
      {
        "id": 0,
        "name": "string",
        "type_id": 0
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
    "detail": "Учетные данные не были предоставлены." 
  }
  ```
  
- **POST** `/api/v1/rooms/`

    Description: Получение списка комнат принадлежащих пользователю

    Parameters: 

    Request Body:
  ```json
  {
    
  }
  ```
    Status Code `201 Created`
  ```json
  {
    
  }
  ```
  

- **GET** `/api/v1/rooms/{id}/`
- **PATCH** `/api/v1/rooms/{id}/`
- **DELETE** `/api/v1/rooms/{id}/`
- **GET** `/api/v1/rooms/types/`
- **GET** `/api/v1/rooms/{id}/types/`
- **POST** `/api/v1/rooms/{id}/share/emails/`
  
  
