from django.urls import path
from django.views.decorators.cache import cache_page

from .views import HomePageView

# MessageCreateView,

from restaurant.apps import RestaurantConfig

app_name = RestaurantConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='main'),
    #
    # path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    # path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
    # path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    # path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    # path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    # path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    #
    # path('mail_list/', ClientListView.as_view(), name='mail_list'),
    # path('mail_create/', ClientCreateView.as_view(), name='mail_create'),
    # path('mail_update/<int:pk>/', ClientUpdateView.as_view(), name='mail_update'),
    # path('mail_delete/<int:pk>/', ClientDeleteView.as_view(), name='mail_delete'),
    # path('mail_detail/<int:pk>/', ClientDetailView.as_view(), name='mail_detail'),
    #
    # path('mailing_send/<int:pk>/', mailing_send, name='mailing_send'),
    #
    # path('message_list/', MessageListView.as_view(), name='message_list'),
    #
    # path('message_settings_update/<int:pk>/', MessageSettingsUpdateView.as_view(), name='message_settings_update'),
    # path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    #
    # path('settings_list/', MailingSettingsListView.as_view(), name='settings_list'),
    # path('settings_update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='settings_update'),
    #
    # path('mailing_activity/<int:pk>/', toggle_activity_mailing, name='mailing_activity'),

]
# path('message_create/', MessageCreateView.as_view(), name='message_create'),
