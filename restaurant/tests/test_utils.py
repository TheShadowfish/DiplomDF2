from datetime import datetime, time, date
from unittest import TestCase

from restaurant.models import ContentParameters, ContentText, ContentImage, Contentlink
from restaurant.utils.utils import time_segment, get_content_parameters, get_content_text_from_postgre, \
    get_content_image_from_postgre, get_content_link_from_postgre


class UtilsTest(TestCase):

    def test_time_segment(self):
        time_lt = time(8, 0, 0)
        time_qt = time(23, 0, 0)

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

        ContentParameters.objects.create(title="period_of_booking", body=10)
        ContentParameters.objects.create(title="work_start", body="12:00")
        ContentParameters.objects.create(title="work_end", body="16:00")
        ContentParameters.objects.create(title="confirm_timedelta", body=50)

        dict_1_eq = {"period_of_booking": 14, "work_start": time(8, 0, 0),
                     "work_end": time(23, 0, 0), "confirm_timedelta": 45}
        dict_3_eg = {"period_of_booking": 10, "work_start": time(12, 0, 0),
                     "work_end": time(16, 0, 0), "confirm_timedelta": 50}

        dictionary_3 = get_content_parameters(ignored_error=False)

        self.assertEquals(dictionary_1, dict_1_eq)
        self.assertEquals(dictionary_2, False)
        self.assertEquals(dictionary_3, dict_3_eg)

    def test_get_content_text_from_postgre(self):
        text_error = get_content_text_from_postgre("test")
        text_e = ("Для изменения текста создайте запись 'test' в таблице ContentText (необходимы полномочия "
                  "администратора)")

        ContentText.objects.create(title="test", body="test")
        text_success = get_content_text_from_postgre("test")
        self.assertEquals(text_error, text_e)
        self.assertEquals(text_success, "test")

    def test_get_content_image_from_postgre(self):
        text_error = get_content_image_from_postgre("test")
        text_e = ("Для изменения изображения создайте запись 'test' в таблице ContentImage и загрузите изображение ("
                  "необходимы полномочия администратора)")

        test_image = ContentImage.objects.create(title="test", description="test", image=None)
        text_success = get_content_image_from_postgre("test")

        self.assertEquals(text_error.description, text_e)
        self.assertEquals(text_success.title, test_image.title)

    def test_get_content_link_from_postgre(self):
        text_error = get_content_link_from_postgre("test")
        text_e = "Для создания ссылки создайте запись 'test' в таблице ContentLink (необходимы полномочия администратора)"

        test_link = Contentlink.objects.create(title="test", text="test", link="#", description="test")
        text_success = get_content_link_from_postgre("test")

        self.assertEquals(text_error.description, text_e)
        self.assertEquals(text_success.text, test_link.text)
