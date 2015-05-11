from django.contrib import admin

# Register your models here.
from models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'type', 'state', 'isActive']


admin.site.register(Group, GroupAdmin)