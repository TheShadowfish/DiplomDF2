"""

from datetime import datetime, timedelta

from django.utils import timezone

from restaurant.models import ContentText, ContentImage, Contentlink, ContentParameters

def get_content_text_from_postgre(title):
    try:
        return ContentText.objects.get(title=title).body
    except:
        return f"Для изменения текста создайте запись '{title}' в таблице ContentText (необходимы полномочия администратора)"

def get_content_image_from_postgre(title):
    try:
        return ContentImage.objects.get(title=title)
    except:
        description = f"Для изменения изображения создайте запись '{title}' в таблице ContentImage и загрузите изображение (необходимы полномочия администратора)"
        return ContentImage.objects.create(title='not_found', description=description, image = None)

def get_content_link_from_postgre(title):
    try:
        return Contentlink.objects.get(title=title)
    except:
        return f"Для создания ссылки создайте запись '{title}' в таблице ContentLink (необходимы полномочия администратора)"

"""
from datetime import datetime, time, date
from unittest import TestCase

from restaurant.models import ContentParameters
from restaurant.utils.utils import time_segment, get_content_parameters, get_content_text_from_postgre


class UtilsTest(TestCase):
    # fixtures = ['test_data.json']

    # @classmethod
    # def setUpTestData(cls):
    #     user = User.objects.first()
    #     #Set up non-modified objects used by all test methods
    #     Review.objects.create(review_text='test', author=user,  sign=user.email, grade=5, moderated=True, answer_text='test')

    def test_time_segment(self):
        time_lt = time(8, 0, 0)
        time_qt = time(23, 0, 0)
        # work_start = datetime.time(8, 0, 0)
        # work_end = datetime.time(23, 0, 0)


        data = date(2024, 4, 1)

        t_start, t_end = time_segment(data, time_lt, time_qt)
        t_start_2, t_end_2 = time_segment(data, time_qt, time_lt)


        self.assertEquals(t_start, datetime(2024, 4, 1, 8, 0, 0))
        self.assertEquals(t_end, datetime(2024, 4, 1, 23, 0, 0))
        self.assertEquals(t_start_2, datetime(2024, 4, 1, 23, 0, 0))
        self.assertEquals(t_end_2, datetime(2024, 4, 2, 8, 0, 0))


    def test_get_content_parameters(self):

        dictionary_1 = get_content_parameters(ignored_error=True)
        dictionary_2 = get_content_parameters(ignored_error=False)

        ContentParameters.objects.create(title='period_of_booking', body=10)
        ContentParameters.objects.create(title='work_start', body='12:00')
        ContentParameters.objects.create(title='work_end', body='16:00')
        ContentParameters.objects.create(title='confirm_timedelta', body=50)

        dict_1_eq = {'period_of_booking': 14, 'work_start': time(8, 0, 0), 'work_end': time(23, 0, 0),
                        'confirm_timedelta': 45}
        dict_3_eg = {'period_of_booking': 10, 'work_start': time(12, 0, 0), 'work_end': time(16, 0, 0),
                        'confirm_timedelta': 50}

        dictionary_3 = get_content_parameters(ignored_error=False)
        print(dictionary_3)


        self.assertEquals(dictionary_1, dict_1_eq)
        self.assertEquals(dictionary_2, False)
        self.assertEquals(dictionary_3, dict_3_eg)




    def test_get_content_text_from_postgre(self):
        text_error = get_content_text_from_postgre('test')
        text_e = f"Для изменения текста создайте запись 'test' в таблице ContentText (необходимы полномочия администратора)"

        ContentParameters.objects.create(title='test', body='test')
        text_success=get_content_text_from_postgre('test')


        self.assertEquals(text_error, text_e)
        self.assertEquals(text_success, 'test')

"""
def get_content_text_from_postgre(title):
    try:
        return ContentText.objects.get(title=title).body
    except:
        return f"Для изменения текста создайте запись '{title}' в таблице ContentText (необходимы полномочия администратора)"

def get_content_image_from_postgre(title):
    try:
        return ContentImage.objects.get(title=title)
    except:
        description = f"Для изменения изображения создайте запись '{title}' в таблице ContentImage и загрузите изображение (необходимы полномочия администратора)"
        return ContentImage.objects.create(title='not_found', description=description, image = None)

def get_content_link_from_postgre(title):
    try:
        return Contentlink.objects.get(title=title)
    except:
        return f"Для создания ссылки создайте запись '{title}' в таблице ContentLink (необходимы полномочия администратора)"
"""

