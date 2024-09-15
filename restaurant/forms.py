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

    def validate_date_time(self, parametr_dict):
        # проверка допустимости бронирования с учетом времени работы и срока предварительного бронирования
        cleaned_data_date_time = self.cleaned_data

        data = cleaned_data_date_time['date_field']
        time_start = cleaned_data_date_time['time_start']
        time_end = cleaned_data_date_time['time_end']

        period_of_booking = parametr_dict['period_of_booking']

        # period_of_booking
        # 10
        # work_start
        # 12: 00:00
        # work_end
        # 16: 00:00
        # confirm_timedelta
        # 50

        t_now = datetime.datetime.now()
        t_start, t_end = time_segment(data, time_start, time_end)
        t_work_start, t_work_end = time_segment(data, parametr_dict['work_start'], parametr_dict['work_end'])

        if t_now > t_start:
            raise forms.ValidationError('Нельзя забронировать место на прошедшее время')

        # # честно, такого быть не может, функция time_segment не позволит
        # if t_end <= t_start:
        #     raise forms.ValidationError(f'Время начала периода бронирования должно быть раньше чем время конца периода')

        if t_start > t_now + datetime.timedelta(days=period_of_booking):
            raise forms.ValidationError(f'Бронировать места можно не ранее чем за {period_of_booking} дней')


        if t_start < t_work_start:
            raise forms.ValidationError(f'В это время ({t_start.hour}:{t_start.minute}) ресторан ещё не открылся')
        if t_end > t_work_end:
            raise forms.ValidationError(f'В это время ({t_end.hour}:{t_end.minute}) ресторан уже закрыт')

        return cleaned_data_date_time

    def clean_place(self):
        # проверка допустимого количества мест за бронируемым столиком
        data = self.cleaned_data
        # print(f"clean_place {data}")

        place = self.cleaned_data['places']
        table = self.cleaned_data['table']
        if place > table.places:
            raise forms.ValidationError(
                f'За данным столиком всего {table.places} мест. Выберете столик с большим количеством мест или позже забронируйте соседний столик')
        elif place < 1:
            raise forms.ValidationError(
                f'Должно быть занято хотя бы одно место за столиком')
        return data

    def clean_my_table(self, time_border):
        # проверка того, что столик свободен
        data = self.cleaned_data
        # print(f"clean_table {data}")

        t_start, t_end = time_segment(data['date_field'], data['time_start'], data['time_end'])

        table = data['table']
        t_now = datetime.datetime.now()

        # список pk бронирований, которые могут быть подтверждены
        booking_tokens = [token.booking.pk for token in BookingToken.objects.filter(created_at__gt=time_border)]

        # получение списка актуальных бронирований
        # bookings = Booking.objects.filter(table=table).filter(Q(active=True) | Q(pk__in=booking_tokens)).order_by("date_field", "time_start")
        # получение уменьшенного списка бронирований
        bookings = (Booking.objects.filter(table=table).filter(Q(active=True) | Q(pk__in=booking_tokens)).
                    filter(date_field__year__gte=t_now.year, date_field__month__gte=t_now.month,
                           date_field__day__gte=(t_now - datetime.timedelta(days=1)).day).order_by("date_field",
                                                                                                   "time_start"))

        # проверка перекрытия времени бронирований
        for b in bookings:
            b_start, b_end = time_segment(b.date_field, b.time_start, b.time_end)

            # если это обновление, то будет оюновляемый объект, иначе None
            booking_id = self.instance

            if b_start <= t_start < b_end and booking_id.pk != b.pk:
                raise forms.ValidationError(
                    f'В указанное время выбранный столик занят')
            if b_start < t_end <= b_end and booking_id.pk != b.pk:
                raise forms.ValidationError(f'В указанное время выбранный столик еще не освободился')

            if t_start <= b_start < t_end and booking_id.pk != b.pk:
                raise forms.ValidationError(f'В указанный период времени столик забронирован')


        return data




    def clean(self):

        parameters_dict = get_content_parameters(False)
        # print(parameters_dict)

        if parameters_dict:
            # period_of_booking
            # 10
            # work_start
            # 12: 00:00
            # work_end
            # 16: 00:00
            # confirm_timedelta
            # 50

            confirm_timedelta = parameters_dict.get('confirm_timedelta')
            time_border = timezone.now() - timezone.timedelta(minutes=confirm_timedelta)

            # print(f"self.cleaned_data 1 {self.cleaned_data}")

            # проверка допустимости бронирования с учетом времени работы и срока предварительного бронирования
            self.validate_date_time(parameters_dict)

            # проверка допустимости бронирования по количеству мест
            self.clean_place()

            # проверка перекрытия времени бронирования
            self.clean_my_table(time_border)

            # print(f"self.cleaned_data 2 {self.cleaned_data}")



        else:
            message = """Не удалось извлечь корректные значения работы ресторана из база данных:
                        таблица ContentParameters, данные 
                        work_start=<%HH:%MM> - время открытия ресторана, 
                        work_end=<%HH:%MM> - время закрытия>, 
                        period_of_booking=<int> - период предварительного бронирования,
                        confirm_timedelta=<int> - время на подтверждение бронирования (в минутах)"""
            raise forms.ValidationError(message)

        return self.cleaned_data


class QuestionsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Questions
        fields = "__all__"
        exclude = (
            "created_at",
        )

class LimitedQuestionsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Questions
        fields = ('question_text','sign')



