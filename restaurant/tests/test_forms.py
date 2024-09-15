# from django.test import TestCase
#
# # Создайте ваши тесты здесь
#
import datetime

from unittest import TestCase

from django.core.exceptions import ValidationError

from restaurant.forms import BookingForm, QuestionsForm, LimitedQuestionsForm


class TestQuestionsForm(TestCase):

    def test_question_form_text_labels(self):
        form = QuestionsForm()
        self.assertTrue(form.fields['question_text'].label == 'Текст вопроса')
        self.assertTrue(form.fields['sign'].label == 'Подпись')
        self.assertTrue(form.fields['moderated'].label == 'Проверен')
        self.assertTrue(form.fields['answer_text'].label == 'Ответ на вопрос')

        with self.assertRaises(Exception) as e:
            self.assertEqual(form.fields['created_at'].label, 'введите дату создания')

    def test_question_form_help_texts(self):
        form = QuestionsForm()
        self.assertEqual(form.fields['question_text'].help_text,'Введите текст вопроса')
        self.assertEqual(form.fields['sign'].help_text, 'Введите подпись под вопросом')
        self.assertEqual(form.fields['moderated'].help_text, 'Введите признак проверки')
        self.assertEqual(form.fields['answer_text'].help_text, 'Введите ответ на вопрос')

        with self.assertRaises(Exception) as e:
            self.assertEqual(form.fields['created_at'].help_text, 'введите дату создания')

class TestLimitedQuestionsForm(TestCase):

    def test_limited_question_form_text_labels(self):
        form = LimitedQuestionsForm()
        self.assertTrue(form.fields['question_text'].label == 'Текст вопроса')
        self.assertTrue(form.fields['sign'].label == 'Подпись')

        with self.assertRaises(Exception) as e:
            self.assertFalse(form.fields['moderated'].label == 'Проверен')
        with self.assertRaises(Exception) as e:
            self.assertFalse(form.fields['answer_text'].label == 'Ответ на вопрос')
        with self.assertRaises(Exception) as e:
            self.assertFalse(form.fields['created_at'].label == 'дата создания')


    def test_limited_question_form_help_texts(self):
        form = LimitedQuestionsForm()
        self.assertEqual(form.fields['question_text'].help_text,'Введите текст вопроса')
        self.assertEqual(form.fields['sign'].help_text, 'Введите подпись под вопросом')


class TestBookingForm(TestCase):

    def test_booking_form_labels(self):
        form = BookingForm()
        # print(form.fields)
        # self.assertTrue(form.fields['table'].label == None or form.fields['table'].label == 'столик')


        self.assertTrue(form.fields['table'].label == 'Столик')
        self.assertTrue(form.fields['places'].label == 'Число бронируемых мест')
        self.assertTrue(form.fields['description'].label == 'Примечания')
        self.assertTrue(form.fields['places'].label == 'Число бронируемых мест')
        self.assertTrue(form.fields['notification'].label == 'Оповещение')
        self.assertTrue(form.fields['date_field'].label == 'Дата бронирования')
        self.assertTrue(form.fields['time_start'].label == 'Начало бронирования')
        self.assertTrue(form.fields['time_end'].label == 'Конец бронирования')
        self.assertTrue(form.fields['notification'].label == 'Оповещение')


        with self.assertRaises(Exception):
            self.assertTrue(form.fields['user'].label == 'пользователь')
        with self.assertRaises(Exception):
            self.assertTrue(form.fields['active'])
        with self.assertRaises(Exception):
            self.assertTrue(form.fields['created_at'])

    def test_validate_date_time(self):

        parameters = {'period_of_booking': 14, 'work_start': datetime.time(8, 0, 0),
                      'work_end': datetime.time(23, 0, 0), 'confirm_timedelta': 45}

        date_out_period = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)


        date_past = datetime.date.today() - datetime.timedelta(days=2)

        date_now = datetime.date.today()
        date_next = datetime.date.today() + datetime.timedelta(days=1)

        # # ЭТО БУДЕТ ГЛЮЧИТЬ ПРИ ВРЕМЕНИ БЛИЗКОМ К ЗАКРЫТИЮ
        # time_now = (datetime.datetime.now() - datetime.timedelta(hours=2)).time()

        time_next_1h = datetime.time(9, 0, 0)
        time_next_2h = datetime.time(12, 0, 0)

        # form_data = {'renewal_date': date}




        correct_data = {'date_field': date_next, 'time_start': time_next_1h, 'time_end': time_next_2h}
        past_data = {'date_field': date_past, 'time_start': time_next_1h, 'time_end': time_next_2h}
        # past_time = {'date_field': date_now, 'time_start': time_past, 'time_end': time_next_2h}
        out_period = {'date_field': date_out_period, 'time_start': time_next_1h, 'time_end': time_next_2h}

        form_correct = BookingForm()
        form_correct.cleaned_data = correct_data

        form_past_d = BookingForm()
        form_past_d.cleaned_data = past_data

        # form_past_t = BookingForm()
        # form_past_t.cleaned_data=past_time

        form_out = BookingForm()
        form_out.cleaned_data=out_period

        # work_start': datetime.time(8, 0, 0),
        # work_end': datetime.time(23, 0, 0)
        #
        before_open  = {'date_field': date_next, 'time_start': datetime.time(7, 0, 0), 'time_end': time_next_2h}
        after_close = {'date_field': date_next, 'time_start': time_next_1h, 'time_end': datetime.time(23, 50, 0)}
        above_closing = {'date_field': date_next, 'time_start': datetime.time(7, 0, 0),
                              'time_end': datetime.time(23, 50, 0)}

        form_after_close = BookingForm()
        form_after_close.cleaned_data = after_close

        form_before_open = BookingForm()
        form_before_open.cleaned_data=before_open

        form_above_closing = BookingForm()
        form_above_closing.cleaned_data=above_closing

        self.assertTrue(form_correct.validate_date_time(parameters))

        with self.assertRaises(Exception):
            form_past_d.validate_date_time(parameters)

        with self.assertRaises(ValidationError) as e:
            form_past_d.validate_date_time(parameters)
        self.assertEqual(e.exception.message, 'Нельзя забронировать место на прошедшее время')

        # with self.assertRaises(ValidationError) as e_2:
        #     form_past_t.validate_date_time(parameters)
        # self.assertEqual(e_2.exception.message, 'Нельзя забронировать место на прошедшее время')

        with self.assertRaises(ValidationError) as e_3:
            form_out.validate_date_time(parameters)
        self.assertEqual(e_3.exception.message, f'Бронировать места можно не ранее чем за {parameters.get("period_of_booking")} дней')


        # work_start': datetime.time(8, 0, 0),
        # work_end': datetime.time(23, 0, 0)
        # before_open = {'date_field': date_now, 'time_start': datetime.time(7, 0, 0), 'time_end': time_next_2h}
        # after_close = {'date_field': date_now, 'time_start': time_next_1h, 'time_end': datetime.time(23, 50, 0)}


        with self.assertRaises(ValidationError) as e_4:
            form_after_close.validate_date_time(parameters)
        self.assertEqual(e_4.exception.message, (f'В это время (23:50) ресторан уже закрыт'))

        with self.assertRaises(ValidationError) as e_5:
            form_before_open.validate_date_time(parameters)
        self.assertEqual(e_5.exception.message, f'В это время (7:0) ресторан ещё не открылся')

        with self.assertRaises(ValidationError) as e_6:
            form_above_closing.validate_date_time(parameters)
        self.assertEqual(e_6.exception.message, 'В это время (7:0) ресторан ещё не открылся')



        # self.assertFalse(form.is_valid())

"""
        def validate_date_time(self, parametr_dict):
            # отдеьная проверка допустимости параметров времени бронирования

            data = self.cleaned_data['date_field']
            time_start = self.cleaned_data['time_start']
            time_end = self.cleaned_data['time_end']

            booking_period = parametr_dict['booking_period']
            
            t_now = datetime.datetime.now()
        t_start, t_end = time_segment(data, time_start, time_end)
        t_work_start, t_work_end = time_segment(data, parametr_dict['work_start'], parametr_dict['work_end'])

        if t_now > t_start:
            raise forms.ValidationError('Нельзя забронировать место на прошедшее время')

        if t_start > t_now + datetime.timedelta(days=booking_period):
            raise forms.ValidationError(f'Бронировать места можно не ранее чем за {booking_period} дней')

        if t_start < t_work_start:
            raise forms.ValidationError(f'В это время ({t_start.hour}:{t_start.minute}) ресторан ещё не открылся')
        if t_end > t_work_end:
            raise forms.ValidationError(f'В это время ({t_end.hour}:{t_end.minute}) ресторан уже закрыт')

        # # Всегда надо возвращать очищенные данные.
        # return data
            # если ошибки не случилось
        return self.cleaned_data
            """



