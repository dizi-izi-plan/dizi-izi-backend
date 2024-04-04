from drf_spectacular.utils import extend_schema

from users.schema.base_extension import BaseExtension
from djoser.views import UserViewSet


class GenerateSwaggerDocForDjoser(BaseExtension):
    """Этот класс предназначен для генерации документации Swagger для эндпоинтов Djoser."""
    target_class = UserViewSet

    # Ключи словаря соответствуют названиям методов в UserViewSet.
    endpoints_doc = {
        "me": [
            # GET /users/me/
            extend_schema(
                methods=["get"],
                summary="Получение информации о текущем пользователе",
                description="Возвращает информацию о текущем пользователе.",
            ),
            # PUT /users/me/
            extend_schema(
                methods=["put"],
                summary="Обновление информации текущего пользователя",
                description="Позволяет полностью обновить информацию о текущем пользователе.",
            ),
            # PATCH /users/me/
            extend_schema(
                methods=["patch"],
                summary="Частичное обновление информации текущего пользователя",
                description="Позволяет частично обновить информацию о текущем пользователе.",
            ),
            # DELETE /users/me/
            extend_schema(
                methods=["delete"],
                summary="Удаление текущего пользователя",
                description="Удаляет текущего пользователя. Требуется права администратора.",
            ),
        ],
        # POST /users/activation/
        "activation": extend_schema(
            methods=["post"],
            summary="Активация пользователя",
            description="Активирует пользователя после регистрации. "
                        "Требуется отправка кода активации, полученного пользователем.",
        ),
        # POST /users/resend_activation/
        "resend_activation": extend_schema(
            methods=["post"],
            summary="Повторная отправка письма активации",
            description="Повторно отправляет письмо активации пользователю, который не активировал свой аккаунт.",
        ),
        # POST /users/set_password/
        "set_password": extend_schema(
            methods=["post"],
            summary="Установка нового пароля",
            description="Позволяет пользователю установить новый пароль.",
        ),
        # POST /users/reset_password/
        "reset_password": extend_schema(
            methods=["post"],
            summary="Сброс пароля",
            description="Инициирует процесс сброса пароля, "
                        "отправляя письмо для сброса на электронную почту пользователя.",
        ),
        # POST /users/reset_password_confirm/
        "reset_password_confirm": extend_schema(
            methods=["post"],
            summary="Подтверждение сброса пароля",
            description="Завершает процесс сброса пароля, устанавливая новый пароль для пользователя.",
        ),
        # POST /users/set_email/
        "set_username": extend_schema(
            methods=["post"],
            summary="Установка нового адреса почты пользователя",
            description="Позволяет текущему пользователю изменить свой адрес почты на новый.",
        ),
        # POST /users/reset_email/
        "reset_username": extend_schema(
            methods=["post"],
            summary="Сброс адреса почты пользователя",
            description="Инициирует процесс сброса адреса почты пользователя, "
                        "отправляя инструкции на электронную почту пользователя. "
                        "Требуется предоставление электронной почты, ассоциированной с аккаунтом.",
        ),
        # POST /users/reset_email_confirm/
        "reset_username_confirm": extend_schema(
            methods=["post"],
            summary="Подтверждение сброса адреса почты пользователя",
            description="Позволяет пользователю подтвердить сброс и установить новый адрес почты "
                        "пользователя, используя код подтверждения, отправленный на его электронную почту. "
                        "Этот процесс завершает смену адреса почты пользователя.",
        ),
        # GET /users/
        "list": extend_schema(
            summary="Получение данных пользователя",
            description="Возвращает данные пользователя. Для админа возвращает список всех пользователей",
        ),
        # POST /users/
        "create": extend_schema(
            summary="Создание нового пользователя",
            description="Создает нового пользователя с предоставленными данными.",
        ),
        # GET /users/{id}/
        "retrieve": extend_schema(
            summary="Получение информации о пользователе",
            description="Возвращает информацию о пользователе по его уникальному идентификатору. "
                        "Требуются права администратора или собственные данные пользователя.",
        ),
        # PUT /users/{id}/
        "update": extend_schema(
            summary="Обновление информации пользователя",
            description="Обновляет информацию о пользователе с использованием полного набора данных. "
                        "Требуются права администратора или собственные данные пользователя.",
        ),
        # PATCH /users/{id}/
        "partial_update": extend_schema(
            summary="Частичное обновление информации пользователя",
            description="Обновляет информацию о пользователе, используя только предоставленные поля. "
                        "Требуются права администратора или собственные данные пользователя.",
        ),
        # DELETE /users/{id}/
        "destroy": extend_schema(
            summary="Удаление пользователя",
            description="Удаляет пользователя. Требуется права администратора."
        ),
    }
