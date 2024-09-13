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


class BookingToken(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name='токен для подтверждения бронирования',
                             help_text='токен для восстановления пароля', related_name='user_token')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
                                      help_text='введите дату создания токена')
    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)
