import secrets

from django.test import TestCase

from restaurant.models import Questions
from django.urls import reverse

from restaurant.templatetags.my_tags import generate_fake_mail


# class QuestionsListViewTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         #Create 13 authors for pagination tests
#         number_of_questions = 13
#         for question_num in range(number_of_questions):
#             Questions.objects.create(question_text= secrets.token_hex(16), sign=generate_fake_mail(10), moderated=True, answer_text=secrets.token_hex(64))
#
#
#     def test_view_url_exists_at_desired_location(self):
#         resp = self.client.get('/question_list/')
#         self.assertEqual(resp.status_code, 200)
#
#     # urlpatterns = [

#     # #
#     # path('booking_list/', BookingListView.as_view(), name='booking_list'),
#     # # path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
#     # path('booking_create/', BookingCreateView.as_view(), name='booking_create'),
#     # path('booking_update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
#     # path('booking_delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),
#     # path('booking_detail/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
#     #
#     # path('booking_activity/<int:pk>/', toggle_activity_booking, name='booking_activity'),
#     #
#     #
#     # path("confirm_booking/<str:email>/", confirm_booking, name='confirm_booking'),
#     # path("booking_verification/<str:token>/", booking_verification, name='booking_verification'),
#     #
#     # path("token_expired/", booking_verification, name='token_expired'),
#     # path("booking_confirmed/", booking_verification, name='booking_confirmed'),
#     # # question
#     # path("question_create/", QuestionCreateView.as_view(), name='question_create'),
#     # path("question_update/<int:pk>/", QuestionUpdateView.as_view(), name='question_update'),
#     # path("question_delete/<int:pk>/", QuestionDeleteView.as_view(), name='question_delete'),
#     #
#     # path("question_success/<str:message>/", questions_success, name='questions_success'),
#
#
#     def test_view_url_accessible_by_name(self):
#         resp = self.client.get(reverse('question_list'))
#         self.assertEqual(resp.status_code, 200)
#
#     def test_view_uses_correct_template(self):
#         resp = self.client.get(reverse('question_list'))
#         self.assertEqual(resp.status_code, 200)
#
#         self.assertTemplateUsed(resp, '/restaurant/question_list.html')
#
#     # def test_pagination_is_ten(self):
#     #     resp = self.client.get(reverse('authors'))
#     #     self.assertEqual(resp.status_code, 200)
#     #     self.assertTrue('is_paginated' in resp.context)
#     #     self.assertTrue(resp.context['is_paginated'] == True)
#     #     self.assertTrue( len(resp.context['author_list']) == 10)
#
#     # def test_lists_all_authors(self):
#     #     #Get second page and confirm it has (exactly) remaining 3 items
#     #     resp = self.client.get(reverse('authors')+'?page=2')
#     #     self.assertEqual(resp.status_code, 200)
#     #     self.assertTrue('is_paginated' in resp.context)
#     #     self.assertTrue(resp.context['is_paginated'] == True)
#     #     self.assertTrue( len(resp.context['author_list']) == 3)


class HomeAboutListViewTest(TestCase):
    #     # path('', HomePageView.as_view(), name='main'),
    #     # path('about_us/', AboutUsPageView.as_view(), name='about_us'),
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

