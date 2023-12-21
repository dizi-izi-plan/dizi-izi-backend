from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser

admin.site.unregister(CustomUser)
User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'is_admin', 'city', ]

    def clean_password2(self):
        # Проверка на совпадения паролей
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Сохранение пароля в хеш формате
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


@admin.register(CustomUser)
class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    list_display = ['email', 'is_admin', 'city', 'i_am_designer']
    ordering = ['email', ]
    add_fieldsets = (
        (None, {
            'fields': (
                'email',
                'first_name',
                'city',
                'birthday',
                'password1',
                'password2'
            ),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal Info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    def save_model(self, request, obj, form, change):
        email = form.cleaned_data['email']
        if not change:
            obj = CustomUser.objects.create_user(
                email=email,
            )
            obj.set_password(form.cleaned_data['password1'])
            obj.save()

        return super().save_model(request, obj, form, change)
