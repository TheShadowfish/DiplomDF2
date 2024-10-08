# Generated by Django 5.1.1 on 2024-09-17 14:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_tg_chat_id_user_tg_nick_user_time_offset"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
            },
        ),
        migrations.AlterField(
            model_name="usertoken",
            name="user",
            field=models.ForeignKey(
                help_text="токен для восстановления пароля",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_token",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь к которому относится токен",
            ),
        ),
    ]
