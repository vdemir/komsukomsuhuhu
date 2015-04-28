from __future__ import absolute_import
from celery import shared_task
from groups.models import Group

@shared_task
def create_temp_group(group_id):
    return group_id



@shared_task
def destroy_temp_group(group_id):
    temp_group = Group.objects.get(id=group_id)
    temp_group.isActive = False
    temp_group.save()
    return 'This group is expired'



