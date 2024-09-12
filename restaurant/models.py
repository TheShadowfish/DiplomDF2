from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Table(models.Model):
    number = models.SmallIntegerField(verbose_name='Номер столика', help_text="Введите номер столика", unique=True)
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
        return f"cтолик {self.number}"


class Booking(models.Model):
    NOTIFICATION_HOURS = (
        (0, "Не оповещать"),
        (1, "За час"),
        (2, "За два часа"),
        (3, "За три часа"),
    )



    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', help_text='пользователь', related_name='user', **NULLABLE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='столик', help_text='столик', related_name = 'table')
    places = models.SmallIntegerField(verbose_name='Число бронируемых мест',
                                      help_text="Введите число бронируемых мест", default=2)

    notification = models.SmallIntegerField(
        default=0, verbose_name="Оповещение", choices=NOTIFICATION_HOURS
    )

    date_field = models.DateField(verbose_name='дата бронирования', help_text='введите дата бронирования')
    time_start = models.TimeField(verbose_name='начало бронирования', help_text='введите начало бронирования')
    time_end = models.TimeField(verbose_name='конец бронирования', help_text='введите конец бронирования')

    active = models.BooleanField(verbose_name='активно ли бронирование', default=True, help_text='введите активно ли бронирование')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания', help_text = 'введите дату создания бронирования')

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'бронирования'
    def __str__(self):
        return f"{self.pk}, {self.user} - {self.table}"


class ContentText(models.Model):
    title = models.CharField(max_length=150, verbose_name='контент-название', help_text="введите название текстового блока", unique=True)
    body = models.TextField(verbose_name='тело текстового блока', help_text='введите тело текстового блока')

    class Meta:
        verbose_name = 'контент'
        verbose_name_plural = 'контент'


    def __str__(self):
        return f"{self.title}: {self.body}"

class ContentImage(models.Model):
    title = models.CharField(max_length=150, verbose_name='картинка-название',
                                 help_text="введите название картинки", unique=True)

    description = models.TextField(
        verbose_name = "Описание картинки",
        help_text = "Введите описание картинки",
        ** NULLABLE,
        )
    image = models.ImageField(
        upload_to = "content/photo",
        verbose_name = "Изображение",
        help_text = "Загрузите изображение",
        ** NULLABLE,
        )

    class Meta:
        verbose_name = 'картинка'
        verbose_name_plural = 'картинки'

    def __str__(self):
        return f"{self.title}: {self.description}"

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
