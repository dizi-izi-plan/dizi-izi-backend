from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

admin.site.unregister(CustomUser)


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'is_admin', 'city',]


@admin.register(CustomUser)
class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    list_display = ['email', 'is_admin', 'city']
    ordering = ['email', ]
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'first_name', 'city', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    def save_model(self, request, obj, form, change):
        obj = CustomUser.objects.create_user(
            email=form.cleaned_data['email'],
        )
        obj.set_password(form.cleaned_data['password'])
        obj.save()
        return super().save_model(request, obj, form, change)
