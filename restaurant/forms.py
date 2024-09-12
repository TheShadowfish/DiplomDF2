import datetime

from django import forms
from django.forms import BooleanField, TimeField, TimeInput, SelectDateWidget, DateField, NumberInput

from restaurant.models import Table, Booking, ContentText, ContentImage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            # if isinstance(field, DateField):
            #     field.widget=SelectDateWidget()
            time = datetime.datetime.now().time()

            if isinstance(field, DateField):
                field.widget=NumberInput(attrs={'type': 'date'})
                field.initial = datetime.date.today

            if isinstance(field, TimeField):
                field.widget=NumberInput(attrs={'type': 'time'})
                field.initial = datetime.time(18, 0)


            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


            # else:
            #     field.widget.attrs['class'] = 'form-control'


class BookingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ('user','active','created_at')



    def clean(self):
        work_start = datetime.time(8, 0, 0)
        work_end = datetime.time(23, 0, 0)
        period_of_booking = 14

        try:
            # время работы хранится в базе данных, период бронирования там же
            period_of_booking = int(ContentText.objects.get(title='period_of_booking').body)
            work_start = datetime.time.fromisoformat(ContentText.objects.get(title='work_start').body)
            work_end = datetime.time.fromisoformat(ContentText.objects.get(title='work_end').body)
        except:
            print(
                f"{ContentText.objects.get(title='work_start')} || {ContentText.objects.get(title='work_end')} || {ContentText.objects.get(title='period_of_booking')}")
            raise forms.ValidationError(
                f'В базу данных не внесено время работы ресторана: work_start=<время открытия>, work_end=<время закрытия>, period_of_booking=<период предварительного бронирования>')

        date = datetime.date.today()
        time = datetime.datetime.now().time()

        # print(f"{self.cleaned_data}")

        cleaned_data_date_field = self.cleaned_data['date_field']
        cleaned_data_time_start = self.cleaned_data['time_start']
        cleaned_data_time_end = self.cleaned_data['time_end']

        # time1 = datetime.strptime("10:30", "%H:%M")
        # time2 = datetime.strptime("01:45", "%H:%M")
        # sum_time = time1 + timedelta(hours=time2.hour, minutes=time2.minute)

        # true_datetime = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
        #                                   day=cleaned_data_date_field.day, hour=cleaned_data_time_start.hour,
        #                                   minute=cleaned_data_time_start.minute)



        t_start = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=cleaned_data_time_start.hour,
                                          minute=cleaned_data_time_start.minute)
        t_end = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=cleaned_data_time_end.hour,
                                          minute=cleaned_data_time_end.minute)

        t_work_start = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=work_start.hour,
                                          minute=work_start.minute)
        # datetime.time.fromisoformat(ContentText.objects.get(title='work_start').body)
        t_work_end = datetime.datetime(year=cleaned_data_date_field.year, month=cleaned_data_date_field.month,
                                          day=cleaned_data_date_field.day, hour=work_end.hour,
                                          minute=work_end.minute)

        t_now = datetime.datetime.now()
        # datetime.time.fromisoformat(ContentText.objects.get(title='work_end').body)

        if cleaned_data_time_end < cleaned_data_time_start:
            t_end += datetime.timedelta(days=1)
        if work_end < work_start:
            t_work_end += datetime.timedelta(days=1)

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
        bookings = Booking.objects.filter(table=table)


        for b in bookings:
            b_start = datetime.datetime(year=b.date_field.year, month=b.date_field.month,
                                        day=b.date_field.day, hour=b.time_start.hour,
                                        minute=b.time_start.minute)
            b_end = datetime.datetime(year=b.date_field.year, month=b.date_field.month,
                                      day=b.date_field.day, hour=b.time_start.hour,
                                      minute=b.time_start.minute)
            if b.time_start < b.time_end:
                b_end += datetime.timedelta(days=1)

            if b_start <= t_start < b_end:
                raise forms.ValidationError(f'В указанное время выбранный столик занят')
            if b_start < t_end <= b_end:
                raise forms.ValidationError(f'В указанное время выбранный столик еще не освободился')

            if t_start <= b_start < t_end:
                raise forms.ValidationError(f'В указанный период времени столик забронирован')




        # zero_time = datetime.time(0,0)
        #
        # if work_end > work_start:
        #     print('рабочее время в пределах одних суток (до 00:00)')
        #
        #
        #
        #     # если рабочее время в пределах одних суток (до 00:00)
        #     # и работа не круглосуточна
        #     if cleaned_data_time_start < work_start:
        #         raise forms.ValidationError(f'В это время ({cleaned_data_time_start}) ресторан ещё не открылся')
        #     if cleaned_data_time_end > work_end:
        #         raise forms.ValidationError(f'В это время ({cleaned_data_time_end}) ресторан уже закрыт')
        #     if cleaned_data_time_end <= cleaned_data_time_start:
        #         raise forms.ValidationError(f'Время начала периода бронирования должно быть раньше чем время конца периода')
        #     if cleaned_data_time_start < time and date == cleaned_data_date_field:
        #         raise forms.ValidationError(f'Сегодня это время уже прошло {cleaned_data_time_start}')
        #
        #     # Здесь проверка столика свободен ли он.
        #     table = self.cleaned_data['table']
        #     bookings = Booking.objects.filter(table=table)
        #
        #
        #     # habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time)
        #     # tables = Table.objects.filter(table=table)
        #
        #     for b in bookings:
        #         if b.date_field == cleaned_data_date_field:
        #             if b.time_start  <= cleaned_data_time_start < b.time_end:
        #                 raise forms.ValidationError(f'В указанное время выбранный столик занят')
        #             if b.time_start < cleaned_data_time_end <= b.time_end:
        #                 raise forms.ValidationError(f'В указанное время выбранный столик еще не освободился')
        #
        #             if cleaned_data_time_start <=  b.time_start < cleaned_data_time_end:
        #                 raise forms.ValidationError(f'В указанный период времени столик забронирован')
        #
        #
        # # рабочий день падает на несколько суток
        # elif work_end == zero_time:
        #     print('рабочий день кончается в 00:00')
        #
        #     if cleaned_data_time_start < work_start:
        #         raise forms.ValidationError(f'В это время ({cleaned_data_time_start}) ресторан ещё не открылся')
        #     if cleaned_data_time_end <= cleaned_data_time_start and cleaned_data_time_end != zero_time:
        #         raise forms.ValidationError(
        #             f'Время начала периода бронирования должно быть раньше чем время конца периода')
        #     if cleaned_data_time_start < time and date == cleaned_data_date_field:
        #         raise forms.ValidationError(f'Сегодня это время уже прошло {cleaned_data_time_start}')
        #
        #     # Здесь проверка столика свободен ли он.
        #     table = self.cleaned_data['table']
        #     bookings = Booking.objects.filter(table=table)
        #
        #     for b in bookings:
        #         if b.date_field == cleaned_data_date_field:
        #             if b.time_start <= cleaned_data_time_start and (cleaned_data_time_start <= b.time_end or b.time_end == zero_time):
        #                 raise forms.ValidationError(f'В указанное время выбранный столик занят')
        #             if b.time_start <= cleaned_data_time_end and (cleaned_data_time_end <= b.time_end or b.time_end == zero_time):
        #                 raise forms.ValidationError(f'В указанное время выбранный столик еще не освободился')
        #
        #             if cleaned_data_time_start <= b.time_start and (b.time_start <= cleaned_data_time_end or cleaned_data_time_end==zero_time):
        #                 raise forms.ValidationError(f'В указанный период времени столик забронирован')
        #
        #
        # # если рабочий день падает на несколько суток то надо менять модель: Time на DateTime
        # # иначе это вывих мозга - или делать из всех Time Datetime ориентируясь на дату бронирования

        return self.cleaned_data

#
# class ContactForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Contact
#         fields = (
#             "name",
#             "phone",
#             "message",
#         )
#
#
# class VersionForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Version
#         fields = "__all__"
#
#         """    product, number, name, sign """
#
#         """# Дополнительное задание
# В один момент может быть только одна активная версия продукта, поэтому при изменении версий необходимо проверять,
# что пользователь в качестве активной версии указал только одну.
# В случае возникновения ошибки вернуть сообщение пользователю и попросить выбрать только одну активную версию.
#
# Дополнительное задание, помеченное звездочкой, желательно, но не обязательно выполнять."""
#     def clean(self):
#
#
#         cleaned_data = self.cleaned_data
#         version_list = Version.objects.all()
#
#         one_is_yet = False
#         for version in version_list:
#
#             if version.product == cleaned_data['product'] and version.sign and cleaned_data['sign']:
#                 if one_is_yet:
#                     raise forms.ValidationError(
#                     f'Нельзя иметь две активных версии продукта одновременно. Измените версию {version}')
#                 else:
#                     one_is_yet = True
#
#         else:
#             return self.cleaned_data
