from django.test import TestCase

# Создайте ваши тесты здесь

import datetime
from django.utils import timezone
from restaurant.forms import QuestionsForm, LimitedQuestionsForm, BookingForm

"""
class Questions(models.Model):
    question_text =  models.TextField(verbose_name='Текст вопроса', help_text='Введите текст вопроса')
    sign = models.CharField(max_length=50, verbose_name='Подпись', help_text='Введите подпись под вопросом')
    moderated = models.BooleanField(default=False, verbose_name='Проверен', help_text='Введите признак проверки')
    answer_text = models.TextField(verbose_name='Ответ на вопрос', help_text='Введите ответ на вопрос', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания',
                                      help_text='введите дату создания')
    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return f"{self.question_text}"
        
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
"""
#
# class QuestionsForm(TestCase):
#
#
#     def test_question_form_question_text_label(self):
#         form = QuestionsForm()
#         # print(form.fields)
#         self.assertTrue(form.fields['question_text'].label == None or form.fields['question_text'].label == 'question_text')
#
#     def test_question_form_question_text_help_text(self):
#         form = QuestionsForm()
#         self.assertEqual(form.fields['question_text'].help_text,'Введите текст вопроса')
#
# class LimitedQuestionsForm(TestCase):
#
#
#     def test_limited_question_form_question_text_label(self):
#         form = LimitedQuestionsForm()
#         self.assertTrue(form.fields['question_text'].label == None or form.fields['question_text'].label == 'question_text')
#
#     def test_limited_question_form_question_text_help_text(self):
#         form = LimitedQuestionsForm()
#         self.assertEqual(form.fields['question_text'].help_text,'Введите текст вопроса')

    # def test_question_form_created_at(self):
    #     date = datetime.date.today() - datetime.timedelta(days=1)
    #     form_data = {'created_at': date}
    #     form = QuestionsForm(data=form_data)
    #     self.assertFalse(form.is_valid())

    # def test_renew_form_date_too_far_in_future(self):
    #     date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertFalse(form.is_valid())

    # def test_renew_form_date_today(self):
    #     date = datetime.date.today()
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertTrue(form.is_valid())

    # def test_renew_form_date_max(self):
    #     date = timezone.now() + datetime.timedelta(weeks=4)
    #     form_data = {'renewal_date': date}
    #     form = RenewBookForm(data=form_data)
    #     self.assertTrue(form.is_valid())