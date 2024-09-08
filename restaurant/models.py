from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Table(models.Model):
    number = models.SmallIntegerField(verbose_name='Номер столика', help_text="Введите номер столика")
    places = models.SmallIntegerField(verbose_name='Число сидячих мест у столика',
                                      help_text="Введите число сидячих мест у столика", default=4)
    flour = models.SmallIntegerField(verbose_name='Этаж нахождения столика',
                                     help_text="Введите этаж нахождения столика", default=1)
    description = models.TextField(verbose_name='Описание столика', help_text='Введите описание столика',
                                   default='обычный столик')

    class Meta:
        verbose_name = 'столик'
        verbose_name_plural = 'столики'
        # permissions = [
        #     ("can_turn_off_mailing", "Can turn off mailing (mailing.settings.status = False"),
        # ]
    def __str__(self):
        return f"id = {self.pk}, numbe r= {self.number}"


class Booking(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='рассылка',
    help_text = 'введите название рассылки')
    message_in = models.TextField(verbose_name='описание', help_text='введите описание рассылки', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
    help_text = 'введите дату создания рассылки')
    # status = models.BooleanField(default=False, verbose_name='статус', help_text='введите статус рассылки')
    # datetime_send = models.DateTimeField(auto_now_add=False, verbose_name='дата срабатывания',
    #                                      help_text='введите дату срабатывания')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', help_text = 'пользователь', related_name = 'user', ** NULLABLE)

    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE, related_name = 'message')

    settings = models.OneToOneField(MailingSettings, on_delete=models.CASCADE, verbose_name='настройки', **NULLABLE, related_name = 'settings')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ("can_turn_off_mailing", "Can turn off mailing (mailing.settings.status = False"),
        ]
    def __str__(self):
        return f" {self.title}"

"""
# Функционал менеджера
- Может просматривать любые рассылки.  PermissionRequiredMixin permission_required = "article.view_article
- Может просматривать список пользователей сервиса.  PermissionRequiredMixin permission_required = "article.view_article
- Может блокировать пользователей сервиса. "can_set_user_inactive", "Can blocked user (bool is_active (is_blocked ?) = False)"
- Может отключать рассылки. "can_turn_off_mailing", "Can turn off mailing (mailing.settings.status = False"

- Не может редактировать рассылки.
- Не может управлять списком рассылок.
- Не может изменять рассылки и сообщения.
 """




#
# class Message(models.Model):
#     title = models.CharField(max_length=150, verbose_name='тема сообщения', help_text="Введите тему сообщения",
#                              default='рассылка')
#     body = models.TextField(verbose_name='тело сообщения', help_text='Введите тело сообщения', default='текст рассылки')
#
#
# """
# **_Рассылка (настройки):_**
# - дата и время первой отправки рассылки;
# - периодичность: раз в день, раз в неделю, раз в месяц;
# - статус рассылки (например, завершена, создана, запущена).
# """
#
#
# class MailingSettings(models.Model):
#     datetime_send = models.DateTimeField(auto_now_add=True, verbose_name='дата и время первой отправки рассылки',
#                                          help_text='введите дату и время первой отправки рассылки')
#
#     # раз в день, раз в неделю, раз в месяц
#
#     periodicity = models.PositiveSmallIntegerField(verbose_name='периодичность (через сколько дней)',
#                                                    help_text='введите периодичность', default='1')
#     # завершена, запущена
#     status = models.BooleanField(default=True, verbose_name='статус', help_text='введите статус рассылки (ожидается ('
#                                                                                 'запущена) или завершена)')
#     active = models.BooleanField(default=True, verbose_name='активность', help_text='запущена ли рассылка сейчас')
#
#
# class Mailing(models.Model):
#     title = models.CharField(max_length=150, unique=True, verbose_name='рассылка',
#                              help_text='введите название рассылки')
#     message_in = models.TextField(verbose_name='описание', help_text='введите описание рассылки', **NULLABLE)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
#                                       help_text='введите дату создания рассылки')
#     # status = models.BooleanField(default=False, verbose_name='статус', help_text='введите статус рассылки')
#     # datetime_send = models.DateTimeField(auto_now_add=False, verbose_name='дата срабатывания',
#     #                                      help_text='введите дату срабатывания')
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь',
#                              help_text='пользователь', related_name='user', **NULLABLE)
#
#     message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE,
#                                    related_name='message')
#
#     settings = models.OneToOneField(MailingSettings, on_delete=models.CASCADE, verbose_name='настройки', **NULLABLE,
#                                     related_name='settings')
#
#     class Meta:
#         verbose_name = 'рассылка'
#         verbose_name_plural = 'рассылки'
#         permissions = [
#             ("can_turn_off_mailing", "Can turn off mailing (mailing.settings.status = False"),
#         ]
#
#
#     """
#     # Функционал менеджера
#     - Может просматривать любые рассылки.  PermissionRequiredMixin permission_required = "article.view_article
#     - Может просматривать список пользователей сервиса.  PermissionRequiredMixin permission_required = "article.view_article
#     - Может блокировать пользователей сервиса. "can_set_user_inactive", "Can blocked user (bool is_active (is_blocked ?) = False)"
#     - Может отключать рассылки. "can_turn_off_mailing", "Can turn off mailing (mailing.settings.status = False"
#
#     - Не может редактировать рассылки.
#     - Не может управлять списком рассылок.
#     - Не может изменять рассылки и сообщения.
#      """
#
#     def __str__(self):
#         return f" {self.title}"
#
#
# class MailingLog(models.Model):
#     log_text = models.TextField(verbose_name='текст лога', help_text='введите текст лога', default=timezone.now())
#
#     mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='логгируемая рассылка',
#                                 help_text='логгируемая рассылка', related_name='mailing_logged')
#
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
#                                       help_text='введите дату создания лога')
#     status = models.BooleanField(default=True, verbose_name='статус попытки', help_text='введите статус попытки')
#     mail_answer = models.TextField(verbose_name='ответ почтового сервера', help_text='введите ответ почтового сервера',
#                                    default='No sending, create or change')
#
#     # updated_at = models.DateTimeField(auto_now=True, verbose_name='дата')
#
#     """
#     - дата и время последней попытки; (+)
#     - статус попытки (успешно / не успешно);
#     - ответ почтового сервера, если он был.
#     """
#
#     class Meta:
#         verbose_name = 'лог рассылки'
#         verbose_name_plural = 'логи рассылок'
#
#     def __str__(self):
#         return f" {self.log_text}"
#
#
# class Client(models.Model):
#     """Модель клиента"""
#     name = models.CharField(max_length=150, verbose_name='имя получателя', default='Уважаемый клиент!')
#     email = models.EmailField(max_length=150, verbose_name='почта')
#     comment = models.TextField(verbose_name='комментарий', help_text='Введите комментарий', default='')
#     is_active = models.BooleanField(default=True, verbose_name='активен', )
#
#     mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка',
#                                 help_text='рассылка', related_name='mailing')
#
#     def __str__(self):
#         return f" {self.email}"
#
#     class Meta:
#         verbose_name = 'клиент'
#         verbose_name_plural = 'клиенты'
