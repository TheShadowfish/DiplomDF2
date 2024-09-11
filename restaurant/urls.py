from django.urls import path
from django.views.decorators.cache import cache_page

from .views import HomePageView, AboutUsPageView, BookingListView, BookingCreateView, BookingUpdateView, \
    BookingDeleteView, BookingDetailView

# MessageCreateView,

from restaurant.apps import RestaurantConfig

app_name = RestaurantConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='main'),
    path('about_us/', AboutUsPageView.as_view(), name='about_us'),
    #
    path('booking_list/', BookingListView.as_view(), name='booking_list'),
    # path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
    path('booking_create/', BookingCreateView.as_view(), name='booking_create'),
    path('booking_update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking_delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),
    path('booking_detail/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    #
    # path('mailing_activity/<int:pk>/', toggle_activity_mailing, name='mailing_activity'),

]
# path('message_create/', MessageCreateView.as_view(), name='message_create'),
