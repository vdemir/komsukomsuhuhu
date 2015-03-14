from django.contrib import admin
#from profiles.models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.

"""
class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False
    verbose_name_plural = 'userdetails'


class UserAdmin(UserAdmin):
    inlines = (MyUserInline, )




admin.site.unregister(User)
admin.site.register(User, UserAdmin)
"""
#admin.site.unregister(Group)