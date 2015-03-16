from django.contrib import admin
from profiles.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.


class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'customUser'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (CustomUserInline, )

#Registrations
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)