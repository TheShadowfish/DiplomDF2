# Generated by Django 5.1.1 on 2024-09-11 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="tg_chat_id",
            field=models.CharField(
                blank=True,
                help_text="Укажите телеграм chat-id",
                max_length=50,
                null=True,
                verbose_name="Телеграм chat-id",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="tg_nick",
            field=models.CharField(
                blank=True,
                help_text="Укажите telegram-ник",
                max_length=50,
                null=True,
                verbose_name="Tg name",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="time_offset",
            field=models.IntegerField(
                default=3,
                help_text="От -12 до +14, по умолчанию UTC+3 (Московское время)",
                verbose_name="Смещение часового пояса",
            ),
        ),
    ]
