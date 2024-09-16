import datetime
import secrets

from django.test import TestCase

from restaurant.models import Questions, Table, Booking
from django.urls import reverse

from restaurant.templatetags.my_tags import generate_fake_mail
from users.models import User


class QuestionsListViewTest(TestCase):
    fixtures = ['test_data.json']

    # @classmethod
    # def setUpTestData(cls):
    #     #Create 13 authors for pagination tests
    #     number_of_questions = 13
    #     for question_num in range(number_of_questions):
    #         Questions.objects.create(question_text= secrets.token_hex(16), sign=generate_fake_mail(10), moderated=True, answer_text=secrets.token_hex(64))


    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/question_list/')
        self.assertEqual(resp.status_code, 200)

    # urlpatterns = [

    # #
    # path('booking_list/', BookingListView.as_view(), name='booking_list'),
    # # path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
    # path('booking_create/', BookingCreateView.as_view(), name='booking_create'),
    # path('booking_update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
    # path('booking_delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),
    # path('booking_detail/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    #
    # path('booking_activity/<int:pk>/', toggle_activity_booking, name='booking_activity'),
    #
    #
    # path("confirm_booking/<str:email>/", confirm_booking, name='confirm_booking'),
    # path("booking_verification/<str:token>/", booking_verification, name='booking_verification'),
    #
    # path("token_expired/", booking_verification, name='token_expired'),
    # path("booking_confirmed/", booking_verification, name='booking_confirmed'),
    # # question
    # path("question_create/", QuestionCreateView.as_view(), name='question_create'),
    # path("question_update/<int:pk>/", QuestionUpdateView.as_view(), name='question_update'),
    # path("question_delete/<int:pk>/", QuestionDeleteView.as_view(), name='question_delete'),
    # path("question_list/", QuestionListView.as_view(), name='question_list'),
    # path("question_success/<str:message>/", questions_success, name='questions_success'),


    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('restaurant:question_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('restaurant:question_list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'restaurant/questions_list.html')

    def test_lists_resp_context(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('restaurant:question_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('time_offset' in resp.context)
        self.assertTrue('questions_and_answers' in resp.context)
        self.assertTrue('time_offset' in resp.context)
        # self.assertTrue(resp.context['is_paginated'] == True)
        # self.assertTrue( len(resp.context['author_list']) == 3)



class HomeListViewTest(TestCase):
    fixtures = ['test_data.json']

    # @classmethod
    # def setUpTestData(cls):
    #     # #Create 13 authors for pagination tests
    #     # number_of_authors = 13
    #     # for author_num in range(number_of_authors):
    #     #     Author.objects.create(first_name='Christian %s' % author_num, last_name = 'Surname %s' % author_num,)

    def test_home_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_home_url_accessible_by_name(self):
        resp = self.client.get(reverse('restaurant:main'))
        self.assertEqual(resp.status_code, 200)

    def test_home_uses_correct_template(self):
        resp = self.client.get(reverse('restaurant:main'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'restaurant/home.html')

    def test_lists_resp_context(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('restaurant:main'))
        self.assertEqual(resp.status_code, 200)


        self.assertTrue('home_about_inside1' in resp.context)
        self.assertTrue('home_about_inside2' in resp.context)
        self.assertTrue(resp.context['home_about'])
        self.assertTrue('home_food1' in resp.context)
        self.assertTrue('home_food2' in resp.context)
        self.assertTrue('home_food3' in resp.context)
        self.assertTrue('home_offer' in resp.context)
        self.assertTrue('telegram' in resp.context)
        self.assertTrue('home_adress' in resp.context)
        self.assertTrue('whatsup' in resp.context)
        self.assertTrue('vkontakte' in resp.context)
        # print(f"resp.context {resp.context}")

        # self.assertTrue(resp.context['is_paginated'] == True)
        # self.assertTrue( len(resp.context['author_list']) == 3)


class AboutListViewTest(TestCase):

    #     # path('about_us/', AboutUsPageView.as_view(), name='about_us'),
    fixtures = ['test_data.json']

    # @classmethod
    # def setUpTestData(cls):
    #     # #Create 13 authors for pagination tests
    #     # number_of_authors = 13
    #     # for author_num in range(number_of_authors):
    #     #     Author.objects.create(first_name='Christian %s' % author_num, last_name = 'Surname %s' % author_num,)

    def test_home_url_exists_at_desired_location(self):
        resp = self.client.get('/about_us/')
        self.assertEqual(resp.status_code, 200)

    def test_home_url_accessible_by_name(self):
        resp = self.client.get(reverse('restaurant:about_us'))
        self.assertEqual(resp.status_code, 200)

    def test_home_uses_correct_template(self):
        resp = self.client.get(reverse('restaurant:about_us'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'restaurant/about_us.html')

    def test_lists_resp_context(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('restaurant:about_us'))
        self.assertEqual(resp.status_code, 200)


        self.assertTrue('about_us_mission_part' in resp.context)
        self.assertTrue('about_us_history_part1' in resp.context)
        self.assertTrue('about_us_history_part2' in resp.context)
        self.assertTrue('about_us_command_part1' in resp.context)
        self.assertTrue('about_us_command_part2' in resp.context)
        self.assertTrue('about_us_inside3' in resp.context)
        self.assertTrue('about_us_inside4' in resp.context)
        self.assertTrue('about_us_team1' in resp.context)
        self.assertTrue('about_us_team2' in resp.context)
        self.assertTrue('about_us_team3' in resp.context)

# class TestRedirect(TestCase):
#     fixtures = ['test_data.json']
#     def test_booking_create_reverse(self):
#         resp = self.client.get(reverse('restaurant:booking_create'))
#         self.assertEqual(resp.status_code, 302)
#         self.assertRedirects(resp, '/users/login/?login=/booking_create/')
#         # AssertionError: '/users/login/?login=%2Fbooking_create%2F' != '/users/login/?next=%2Frestaurant%2Fbooking_create%2F'
#
#         # self.assertEqual(resp.location, 'users:login')
#
#         # self.assertTemplateUsed(resp, 'restaurant/booking_create.html')
#
#         # resp
#
#     def test_booking_list_reverse(self):
#         resp = self.client.get(reverse('restaurant:booking_list'))
#         self.assertEqual(resp.status_code, 302)
#
#         self.assertRedirects(resp, '/users/login/?login=/booking_list/')



class BookingListViewTest(TestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        # Создание ользователя
        test_user1 = User.objects.create_user(email='test_user1@test.ru', name='user1', password='test')
        test_user1.save()

        #берем первый попавшийся столик из фикстуры
        table = Table.objects.first()


        # Создание 10 объектов Booking
        number_of_booking_copies = 10

        for i, booking in enumerate(range(number_of_booking_copies), start=1):

            date_next = datetime.date.today() + datetime.timedelta(days=1)
            time_next_1h = datetime.time((8+i), 0, 0)
            time_next_2h = datetime.time((9+i), 0, 0)

            booking = Booking.objects.create(user=test_user1, table=table, places=4, description='test_booking',
                                                    notification=0,
                                                    date_field=date_next, time_start=time_next_1h,
                                                    time_end=time_next_2h, active=True)
            booking.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('restaurant:booking_list'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/users/login/?login=/booking_list/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email='test_user1@test.ru', password='test')
        resp = self.client.get(reverse('restaurant:booking_list'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']),  'user1 (test_user1@test.ru)')
        #return f"{self.name} ({self.email})
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'restaurant/booking_list.html')

    def test_only_user_bookings_in_list(self):
        login = self.client.login(email='test_user1@test.ru', password='test')
        resp = self.client.get(reverse('restaurant:booking_list'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'user1 (test_user1@test.ru)')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Проверка, что все бронирования пользователя показаны
        self.assertTrue('booking_list' in resp.context)
        self.assertEqual(len(resp.context['booking_list']), 10)

        # Подтверждение, что все бронирования принадлежат testuser1
        for booking_item in resp.context['booking_list']:
            self.assertEqual(resp.context['user'], booking_item.user)

        # проверка, что список отсортирован
        date_last = 0
        time_last = 0

        for copy in resp.context['booking_list']:
            if date_last == 0:
                date_last = copy.date_field
                time_last = copy.time_start
            else:
                self.assertTrue(copy.date_field >= date_last)
                self.assertTrue(copy.time_start >= time_last)

class BookingCreateViewTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        # Создание пользователя
        test_user2 = User.objects.create_user(email='test_user2@test.ru', name='user2', password='test')
        test_user2.save()

        test_user1 = User.objects.create_user(email='test_user1@test.ru', name='user1', password='test')
        test_user1.save()

        # берем первый попавшийся столик из фикстуры
        table_1 = Table.objects.first()

        # берем первый попавшийся столик из фикстуры
        table_2 = Table.objects.last()

        # Создание 10 объектов Booking
        number_of_booking_copies = 10

        for i, booking in enumerate(range(number_of_booking_copies), start=1):
            date_next = datetime.date.today() + datetime.timedelta(days=1)
            time_next_1h = datetime.time((8 + i), 0, 0)
            time_next_2h = datetime.time((9 + i), 0, 0)

            booking = Booking.objects.create(user=test_user2, table=table_2, places=4, description='test_booking',
                                            notification=0,
                                            date_field=date_next, time_start=time_next_1h,
                                            time_end=time_next_2h, active=True)
            booking = Booking.objects.create(user=test_user1, table=table_1, places=4, description='test_booking',
                                             notification=0,
                                             date_field=date_next, time_start=time_next_1h,
                                             time_end=time_next_2h, active=True)

            booking.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('restaurant:booking_create'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/users/login/?login=/booking_create/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email='test_user2@test.ru', password='test')
        resp = self.client.get(reverse('restaurant:booking_create'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'user2 (test_user2@test.ru)')
        # return f"{self.name} ({self.email})
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'restaurant/booking_form.html')

    def test_seeing_active_bookings_when_create(self):
        login = self.client.login(email='test_user2@test.ru', password='test')
        resp = self.client.get(reverse('restaurant:booking_create'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'user2 (test_user2@test.ru)')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Проверка, что все бронирования пользователя показаны
        self.assertTrue('booking_list' in resp.context)
        self.assertEqual(len(resp.context['booking_list']), 20)

        # Подтверждение, что бронирования принадлежат разным пользователям
        different_users=False
        for booking_item in resp.context['booking_list']:
            if booking_item.user != resp.context['user']:
                different_users = True
                break
        self.assertTrue(different_users)

        # проверка что список отсортирован
        date_last = 0
        time_last = 0

        for copy in resp.context['booking_list']:
            if date_last == 0:
                date_last = copy.date_field
                time_last = copy.time_start
            else:
                self.assertTrue(copy.date_field >= date_last)
                self.assertTrue(copy.time_start >= time_last)