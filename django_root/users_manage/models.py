from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, verbose_name="ID Пользователя")
    name = models.CharField(max_length=100, verbose_name="Имя Пользователя")
    username = models.CharField(max_length=100, verbose_name="Username Telegram", null=True)
    email = models.EmailField(max_length=100, verbose_name="Email", null=True)

    def __str__(self):
        return f"№{self.id} ({self.user_id} - {self.username})"

