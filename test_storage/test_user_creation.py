"""
Скрипт для засирания базы левыми юзерами, не прошедшими активацию.
smtp порт блочит отправку писем для активации, но пользователи в базе создаются.
"""
import time

import requests

# Define the URL of the endpoint
url = 'http://127.0.0.1:8000/api/v1/auth/users/'

# Define the data to be sent in the request body
for i in range(5):
    time.sleep(0.1)
    data = {
        "email": f"aaa531@mail{i}.ru",
        "password": f"Si6lipe8{i}",
        "re_password": f"Si6lipe8{i}"
    }

    # Send the POST request
    response = requests.post(url, data=data)

    # Check the response status code
    print(response.status_code)
    if response.status_code == 200:
        print("POST request successful!")
    else:
        print("POST request failed.")

