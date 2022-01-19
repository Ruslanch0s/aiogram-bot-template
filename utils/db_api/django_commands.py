from asgiref.sync import sync_to_async

from django_root.users_manage.models import User
import logging


@sync_to_async
def select_user(user_id: int):
    user = User.objects.get(user_id=user_id)
    return user


@sync_to_async
def add_user(user_id, full_name, username):
    User(user_id=int(user_id), name=full_name, username=username).save()
