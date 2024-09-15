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
        # отдеьная проверка допустимости параметров времени бронирования

        data = self.cleaned_data['date_field']
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']

        period_of_booking = parametr_dict['period_of_booking']

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

        # не позволить перекрывать перерыв - сделать

        if t_start < t_work_start:
            raise forms.ValidationError(f'В это время ({t_start.hour}:{t_start.minute}) ресторан ещё не открылся')
        if t_end > t_work_end:
            raise forms.ValidationError(f'В это время ({t_end.hour}:{t_end.minute}) ресторан уже закрыт')

        # # Всегда надо возвращать очищенные данные.
        # return data
            # если ошибки не случилось
        return self.cleaned_data


    def clean(self):

        parameters_dict = get_content_parameters(False)



        if parameters_dict:
            period_of_booking = parameters_dict.get('period_of_booking')
            work_start = parameters_dict.get('work_start')
            work_end = parameters_dict.get('work_end')
            confirm_timedelta = parameters_dict.get('confirm_timedelta')

            time_border = timezone.now() - timezone.timedelta(minutes=confirm_timedelta)

        else:
            message = """Не удалось извлечь корректные значения работы ресторана из база данных:
                        таблица ContentParameters, данные 
                        work_start=<%HH:%MM> - время открытия ресторана, 
                        work_end=<%HH:%MM> - время закрытия>, 
                        period_of_booking=<int> - период предварительного бронирования,
                        confirm_timedelta=<int> - время на подтверждение бронирования (в минутах)"""
            raise forms.ValidationError(message)


        self.validate_date_time(parameters_dict)

        # cleaned_data_date_field = self.cleaned_data['date_field']
        # cleaned_data_time_start = self.cleaned_data['time_start']
        # cleaned_data_time_end = self.cleaned_data['time_end']
        # cleaned_data_places = self.cleaned_data['places']

        # t_now = datetime.datetime.now()
        #
        # t_start, t_end = time_segment(cleaned_data_date_field, cleaned_data_time_start, cleaned_data_time_end)
        # t_work_start, t_work_end = time_segment(cleaned_data_date_field, work_start, work_end)


        # попытаюсь запихнуть в валидатор
        # if t_now > t_start:
        #     raise forms.ValidationError('Нельзя забронировать место на прошедшее время')
        #     # return False
        # if t_end <= t_start:
        #     raise forms.ValidationError(f'Время начала периода бронирования должно быть раньше чем время конца периода')
        #
        # if t_start > t_now + datetime.timedelta(days=period_of_booking):
        #     raise forms.ValidationError(f'Бронировать места можно не ранее чем за {period_of_booking} дней')
        #
        # if t_start <= t_work_start < t_end:
        #     raise forms.ValidationError(f'В указанный период времени ресторан закрывается на перерыв')
        #
        # if t_start < t_work_start:
        #     raise forms.ValidationError(f'В это время ({cleaned_data_time_start}) ресторан ещё не открылся')
        # if t_end > t_work_end:
        #     raise forms.ValidationError(f'В это время ({cleaned_data_time_end}) ресторан уже закрыт')






        # а можно это сделать методом модели?

        table = self.cleaned_data['table']


        t_now = datetime.datetime.now()


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

        cleaned_data_places = self.cleaned_data['places']

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

class LimitedQuestionsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Questions
        fields = ('question_text','sign')



