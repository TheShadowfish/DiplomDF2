import datetime

from django import forms
from django.db.models import TextField, Q
from django.forms import BooleanField, TimeField, TimeInput, SelectDateWidget, DateField, NumberInput
from django.utils import timezone

from restaurant.models import Table, Booking, ContentText, ContentImage, ContentParameters, BookingToken, Questions


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        time_append = 0

        for field_name, field in self.fields.items():

            # time = datetime.datetime.now().time()

            if isinstance(field, DateField):
                field.widget=NumberInput(attrs={'type': 'date'})
                field.initial = datetime.date.today

            if isinstance(field, TimeField):
                field.widget=NumberInput(attrs={'type': 'time'})
                field.initial = datetime.time(18 + time_append, 0)
                time_append += 2

            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'



class BookingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ('user','active','created_at')



    def clean(self):
        # а может в Validators затолкаем?
        # TimeValidations(cleaned_data)
        # TableValidations(cleaned_data)

        work_start = datetime.time(8, 0, 0)
        work_end = datetime.time(23, 0, 0)
        period_of_booking = 14

        try:
            period_of_booking = int(ContentParameters.objects.get(title='period_of_booking').body)
            work_start = datetime.time.fromisoformat(ContentParameters.objects.get(title='work_start').body)
            work_end = datetime.time.fromisoformat(ContentParameters.objects.get(title='work_end').body)

        except:
            print(
                f"{ContentParameters.objects.get(title='work_start')} || {ContentParameters.objects.get(title='work_end')} || {ContentParameters.objects.get(title='period_of_booking')}")
            raise forms.ValidationError(
                f'В базу данных не внесено время работы ресторана: work_start=<время открытия>, work_end=<время закрытия>, period_of_booking=<период предварительного бронирования>')
                # work_start = datetime.time(8, 0, 0)
                # work_end = datetime.time(23, 0, 0)
                # period_of_booking = 14

        date = datetime.date.today()
        # time = datetime.datetime.now().time()
        # print(f"{self.cleaned_data}")

        cleaned_data_date_field = self.cleaned_data['date_field']
        cleaned_data_time_start = self.cleaned_data['time_start']
        cleaned_data_time_end = self.cleaned_data['time_end']
        cleaned_data_places = self.cleaned_data['places']

        t_start = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=cleaned_data_time_start.hour,
                                          minute=cleaned_data_time_start.minute)
        t_end = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=cleaned_data_time_end.hour,
                                          minute=cleaned_data_time_end.minute)

        t_work_start = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=work_start.hour,
                                          minute=work_start.minute)
        # datetime.time.fromisoformat(ContentParameters.objects.get(title='work_start').body)
        t_work_end = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=work_end.hour,
                                          minute=work_end.minute)

        t_now = datetime.datetime.now()
        # datetime.time.fromisoformat(ContentParameters.objects.get(title='work_end').body)

        if cleaned_data_time_end < cleaned_data_time_start:
            t_end += datetime.timedelta(days=1)
            # print("cleaned_data_time_end < cleaned_data_time_start")
        if work_end < work_start:
            t_work_end += datetime.timedelta(days=1)
            # print("work_end < work_start")

        if date > cleaned_data_date_field:
            raise forms.ValidationError('Нельзя забронировать место на прошедшую дату')
        if cleaned_data_date_field > date + datetime.timedelta(days=period_of_booking):
            raise forms.ValidationError(f'Бронировать места можно не ранее чем за {period_of_booking} дней')

        if t_start < t_work_start:
            raise forms.ValidationError(f'В это время ({cleaned_data_time_start}) ресторан ещё не открылся')
        if t_end > t_work_end:
            raise forms.ValidationError(f'В это время ({cleaned_data_time_end}) ресторан уже закрыт')
        if t_end <= t_start:
            raise forms.ValidationError(f'Время начала периода бронирования должно быть раньше чем время конца периода')
        if t_start < t_now:
            raise forms.ValidationError(f'Сегодня это время уже прошло {cleaned_data_time_start}')

        table = self.cleaned_data['table']

        # получение времени подтверждения бронирования, получение времени, которое определяет границу регистрации
        try:
            confirm_timedelta = timezone.timedelta(
                minutes=ContentParameters.objects.get(title='confirm_timedelta'))
        except:
            confirm_timedelta = timezone.timedelta(minutes=45)
            # print(f"confirm_timedelta - установлено по умолчаеию (45 минут)")
        time_border = timezone.now() - confirm_timedelta

        # список pk бронирований, которые могут быть подтверждены
        booking_tokens = [token.booking.pk for token in  BookingToken.objects.filter(created_at__gt=time_border)]

        # получение списка актуальных бронирований
        # bookings = Booking.objects.filter(table=table).filter(Q(active=True) | Q(pk__in=booking_tokens)).order_by("date_field", "time_start")
        # получение уменьшенного списка бронирований
        date_now = datetime.now()
        bookings = (Booking.objects.filter(table=table).filter(Q(active=True) | Q(pk__in=booking_tokens)).
               filter(date_field__year__gte=date_now.year, date_field__month__gte=date_now.month,
                      date_field__day__gte=(date_now - datetime.timedelta(days=1)).day).order_by("date_field", "time_start"))


        if cleaned_data_places > table.places:
            raise forms.ValidationError(f'За данным столиком всего {table.places} мест. Выберете столик с большим количеством мест или позже забронируйте соседний столик')
        elif cleaned_data_places < 1:
            raise forms.ValidationError(
                f'Должно быть занято хотя бы одно место за столиком')



        for b in bookings:
            b_start = datetime.datetime(year=b.date_field.year, month=b.date_field.month,
                                        day=b.date_field.day, hour=b.time_start.hour,
                                        minute=b.time_start.minute)
            b_end = datetime.datetime(year=b.date_field.year, month=b.date_field.month,
                                      day=b.date_field.day, hour=b.time_end.hour,
                                      minute=b.time_end.minute)
            if b.time_start > b.time_end:
                b_end += datetime.timedelta(days=1)

            # если это обновление то будет объект, иначе None
            booking_id = self.instance

            if b_start <= t_start < b_end and booking_id.pk != b.pk:
                raise forms.ValidationError(f'В указанное время выбранный столик занят {b_start} <= {t_start} < {b_end} ')
            if b_start < t_end <= b_end and booking_id.pk != b.pk:
                raise forms.ValidationError(f'В указанное время выбранный столик еще не освободился')

            if t_start <= b_start < t_end and booking_id.pk != b.pk:
                raise forms.ValidationError(f'В указанный период времени столик забронирован')


        return self.cleaned_data


class QuestionsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Questions
        fields = "__all__"
        exclude = (
            "created_at",
        )

        # question_text = models.TextField(verbose_name='Текст вопроса', help_text='Введите текст вопроса')
        # sign = models.CharField(max_length=50, verbose_name='Подпись', help_text='Введите подпись под вопросом')
        # moderated = models.BooleanField(default=False, verbose_name='Проверен',
        #                                 help_text='Введите признак проверки')
        # answer_text = models.TextField(verbose_name='Ответ на вопрос', help_text='Введите ответ на вопрос',
        #                                **NULLABLE)
        # created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
class LimitedQuestionsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Questions
        fields = ('question_text','sign')



