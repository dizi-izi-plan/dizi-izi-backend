from django.contrib import admin
from django.urls import include, path
from user_app import views


urlpatterns = [
    path('api/v1/furniture/', views.FurnitureViewSet.as_view()),
    path('admin/', admin.site.urls)
]
