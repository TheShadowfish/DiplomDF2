import datetime

from django import forms
from django.db.models import Q
from django.forms import BooleanField, TimeField, DateField, NumberInput, Textarea, TextInput, CharField
from django.utils import timezone


from restaurant.models import Table, Booking, ContentText, ContentImage, ContentParameters, BookingToken, Questions
from restaurant.utils.utils import time_segment, get_content_parameters


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


class BookingStyleFormMixin:
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

            if isinstance(field, CharField):
                field.widget = Textarea(attrs={'rows': 5})


            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'



class BookingForm(BookingStyleFormMixin, forms.ModelForm):

    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ('user','active','created_at')

    def clean(self):

        # все параметры надо запихнуть в одну функцию и тащить их оттуда

        # try:
        #     period_of_booking = int(ContentParameters.objects.get(title='period_of_booking').body)
        #     work_start = datetime.time.fromisoformat(ContentParameters.objects.get(title='work_start').body)
        #     work_end = datetime.time.fromisoformat(ContentParameters.objects.get(title='work_end').body)
        # except:
        #     print(
        #         f"{ContentParameters.objects.get(title='work_start')} || {ContentParameters.objects.get(title='work_end')} || {ContentParameters.objects.get(title='period_of_booking')}")
        #     raise forms.ValidationError(
        #         f'В базу данных не внесено время работы ресторана: work_start=<время открытия>, work_end=<время закрытия>, period_of_booking=<период предварительного бронирования>')
        #         # work_start = datetime.time(8, 0, 0)
        #         # work_end = datetime.time(23, 0, 0)
        #         # period_of_booking = 14
        # # получение времени подтверждения бронирования, получение времени, которое определяет границу регистрации
        # try:
        #     confirm_timedelta = timezone.timedelta(
        #         minutes=ContentParameters.objects.get(title='confirm_timedelta'))
        # except:
        #     confirm_timedelta = timezone.timedelta(minutes=45)
        #     # print(f"confirm_timedelta - установлено по умолчаеию (45 минут)")
        # time_border = timezone.now() - confirm_timedelta


        parameters_dict = get_content_parameters(False)

        if parameters_dict:
            period_of_booking = parameters_dict.get('period_of_booking')
            work_start = parameters_dict.get('work_start')
            work_end = parameters_dict.get('work_end')
            confirm_timedelta = parameters_dict.get('confirm_timedelta')

            time_border = timezone.now() - timezone.timedelta(minutes=confirm_timedelta)


            # time_border = parameters_dict.get('time_border')
        else:
            message = """Не удалось извлечь корректные значения работы ресторана из база данных:
                        таблица ContentParameters, данные 
                        work_start=<%HH:%MM> - время открытия ресторана, 
                        work_end=<%HH:%MM> - время закрытия>, 
                        period_of_booking=<int> - период предварительного бронирования,
                        confirm_timedelta=<int> - время на подтверждение бронирования (в минутах)"""
            raise forms.ValidationError(message)


        cleaned_data_date_field = self.cleaned_data['date_field']
        cleaned_data_time_start = self.cleaned_data['time_start']
        cleaned_data_time_end = self.cleaned_data['time_end']
        cleaned_data_places = self.cleaned_data['places']

        t_now = datetime.datetime.now()

        t_start, t_end = time_segment(cleaned_data_date_field, cleaned_data_time_start, cleaned_data_time_end)
        t_work_start, t_work_end = time_segment(cleaned_data_date_field, work_start, work_end)


        # попытаюсь запихнуть в валидатор
        if t_now > t_start:
            raise forms.ValidationError('Нельзя забронировать место на прошедшее время')
        if t_end <= t_start:
            raise forms.ValidationError(f'Время начала периода бронирования должно быть раньше чем время конца периода')

        if t_start > t_now + datetime.timedelta(days=period_of_booking):
            raise forms.ValidationError(f'Бронировать места можно не ранее чем за {period_of_booking} дней')

        if t_start < t_work_start:
            raise forms.ValidationError(f'В это время ({cleaned_data_time_start}) ресторан ещё не открылся')
        if t_end > t_work_end:
            raise forms.ValidationError(f'В это время ({cleaned_data_time_end}) ресторан уже закрыт')




        # а можно это сделать методом модели?

        table = self.cleaned_data['table']


        # список pk бронирований, которые могут быть подтверждены
        booking_tokens = [token.booking.pk for token in  BookingToken.objects.filter(created_at__gt=time_border)]

        # получение списка актуальных бронирований
        # bookings = Booking.objects.filter(table=table).filter(Q(active=True) | Q(pk__in=booking_tokens)).order_by("date_field", "time_start")
        # получение уменьшенного списка бронирований
        # date_now = datetime.now()
        bookings = (Booking.objects.filter(table=table).filter(Q(active=True) | Q(pk__in=booking_tokens)).
               filter(date_field__year__gte=t_now.year, date_field__month__gte=t_now.month,
                      date_field__day__gte=(t_now - datetime.timedelta(days=1)).day).order_by("date_field", "time_start"))

        # а можно это сделать методом модели?




        # можно ли это запихнуть в валидатор?
        if cleaned_data_places > table.places:
            raise forms.ValidationError(f'За данным столиком всего {table.places} мест. Выберете столик с большим количеством мест или позже забронируйте соседний столик')
        elif cleaned_data_places < 1:
            raise forms.ValidationError(
                f'Должно быть занято хотя бы одно место за столиком')



        for b in bookings:
            b_start, b_end = time_segment(b.date_field, b.time_start, b.time_end)

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



