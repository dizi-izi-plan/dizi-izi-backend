
#эндпоинты регистрации через соц.сети
http://localhost:8000/api/v1/social_auth/login/yandex-oauth2/ - регистрация через яндекс

http://localhost:8000/api/v1/social_auth/login/vk-oauth2/ - регистрация через вк

#Настройка редиректа, на проде нужно поменять 127.0.0.1:8000 на домен

http://127.0.0.1:8000/api/v1/social_auth/complete/yandex-oauth2/ 

http://127.0.0.1:8000/api/v1/social_auth/complete/vk-oauth2/ - настраивается в vk.com/dev
