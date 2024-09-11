import datetime

from django import forms
from django.forms import BooleanField

from restaurant.models import Table, Booking, ContentText, ContentImage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
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
        # def clean(self):
        #     cleaned_data = self.cleaned_data['year_born']
        #     year_born = int(self.cleaned_data['year_born'])
        #     current_year = timezone.now().year
        #     timedelta = current_year - year_born
        #     if timedelta >= 100:
        #         raise forms.ValidationError("Собаки столько не живут. проверьте год рождения.")
        #
        #     return self.cleaned_data


        # blacklist = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        #
        # cleaned_data = self.cleaned_data['name'] + self.cleaned_data['description']

        # передалать на однократное получение в начале работы?
        # придется обновлеть при каждом изменении ContentText, подумать как

        work_start = datetime.time(8, 0, 0)
        work_end = datetime.time(23, 0, 0)
        period_of_booking = 14

        # print(f"{ContentText.objects.get(title='work_start')} || {ContentText.objects.get(title='work_end')} || {ContentText.objects.get(title='period_of_booking')}")

        try:
            #
            # print("07/01/2015-14:31:58.520")
            period_of_booking = int(ContentText.objects.get(title='period_of_booking').body)
            # print(f"period_of_booking {str(period_of_booking)}")

            # print(f"work_start {ContentText.objects.get(title='work_start').body}")

            work_start = datetime.time.fromisoformat(ContentText.objects.get(title='work_start').body)
            # work_start = datetime.time.strftime('10:00', '%H:%M')
            # work_start = datetime.time.fromisoformat('10:00')


            # work_start = datetime.time(ContentText.objects.get(title='work_start'))
            # print(f"work_start {str(work_start)}")
            work_end = datetime.time.fromisoformat(ContentText.objects.get(title='work_end').body)
            # work_end = datetime.time(ContentText.objects.get(title='work_end'))


            # print(f"work_end {str(work_end)}")

        except:
            print(
                f"{ContentText.objects.get(title='work_start')} || {ContentText.objects.get(title='work_end')} || {ContentText.objects.get(title='period_of_booking')}")

            raise forms.ValidationError(
                f'В базу данных не внесено время работы ресторана: work_start=<время открытия>, work_end=<время закрытия>, period_of_booking=<период предварительного бронирования>')

        date = datetime.date.today()
        time = datetime.datetime.now().time()

        print(f"{self.cleaned_data}")

        # cleaned_data = self.cleaned_data['year_born']


        cleaned_data_date_field = self.cleaned_data['date_field']
        cleaned_data_time_start = self.cleaned_data['time_start']
        cleaned_data_time_end = self.cleaned_data['time_end']

        # cleaned_data_date = time.strptime(self.cleaned_data['date_field'], '%d-%m-%y')
        # cleaned_data_time_start = time.strptime(self.cleaned_data['time_start'], '%H:%M')
        # cleaned_data_time_end = time.strptime(self.cleaned_data['time_end'], '%H:%M')

        # time.strptime(ContentText.objects.get(title='work_start'), '%H:%M')

        if date > cleaned_data_date_field:
            raise forms.ValidationError('Нельзя забронировать место на прошедшую дату')

        if cleaned_data_date_field > date + datetime.timedelta(days=period_of_booking):
            raise forms.ValidationError(f'Бронировать места можно не ранее чем за {period_of_booking} дней')


        if cleaned_data_time_start < work_start:
            raise forms.ValidationError(f'В это время ({cleaned_data_time_start}) ресторан ещё не открылся')
        if cleaned_data_time_end > work_end:
            raise forms.ValidationError(f'В это время ({cleaned_data_time_end}) ресторан уже закрыт')
        if cleaned_data_time_end <= cleaned_data_time_start:
            raise forms.ValidationError(f'Время начала периода бронирования должно быть раньше чем время конца периода')
        if cleaned_data_time_start < time and date == cleaned_data_date:
            raise forms.ValidationError(f'Сегодня это время уже прошло {cleaned_data_time_start}')

        # Здесь проверка столика свободен ли он.
        # cleaned_data = self.cleaned_data
        # version_list = Version.objects.all()
        #
        # one_is_yet = False
        # for version in version_list:
        #
        #     if version.product == cleaned_data['product'] and version.sign and cleaned_data['sign']:
        #         if one_is_yet:
        #             raise forms.ValidationError(
        #                 f'Нельзя иметь две активных версии продукта одновременно. Измените версию {version}')
        #         else:
        #             one_is_yet = True


        # Здесь проверка имеется ли за ним нужное количество мест.
        # cleaned_data = self.cleaned_data
        # version_list = Version.objects.all()
        #
        # one_is_yet = False
        # for version in version_list:
        #
        #     if version.product == cleaned_data['product'] and version.sign and cleaned_data['sign']:
        #         if one_is_yet:
        #             raise forms.ValidationError(
        #                 f'Нельзя иметь две активных версии продукта одновременно. Измените версию {version}')
        #         else:
        #             one_is_yet = True


        else:
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
