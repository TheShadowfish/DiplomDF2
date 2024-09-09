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
        # fields = (
        # "user",
        # "table",
        # "date_field",
        # "time_start",
        # "time_end",
        # "active",
        # "created_at"
        # ) казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар
        exclude = ('owner','created_at',)

    def clean(self):
        # blacklist = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        #
        # cleaned_data = self.cleaned_data['name'] + self.cleaned_data['description']

        # передалать на однократное получение в начале работы?
        # придется обновлеть при каждом изменении ContentText, подумать как

        work_start = datetime.time(8, 0, 0)
        work_end = datetime.time(23, 0, 0)
        period_of_booking = 14

        try:
            work_start = datetime.time(ContentText.objects.get(title='work_start'))
            work_end = datetime.time(ContentText.objects.get(title='work_end'))
            period_of_booking = int(ContentText.objects.get(title='period_of_booking'))
        except:

            raise forms.ValidationError(
                'В базу данных не внесено время работы ресторана: work_start=<время открытия>, work_end=<время закрытия>, period_of_booking=<период предварительного бронирования>')

        date = datetime.date.today()
        time = datetime.now().time()

        cleaned_data_date = self.cleaned_data['date_field']
        cleaned_data_time_start = self.cleaned_data['time_start']
        cleaned_data_time_end = self.cleaned_data['time_end']

        if date > cleaned_data_date:
            raise forms.ValidationError('Нельзя забронировать место на прошедшую дату')

        if cleaned_data_date > date + datetime.timedelta(days=period_of_booking):
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
