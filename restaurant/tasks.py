from datetime import datetime

from django.utils import timezone
from celery import shared_task
from restaurant.services import send_telegram_message

from restaurant.models import Booking
from restaurant.utils.utils import get_actual_bookings


# from habits.models import Habits


@shared_task
def send_information_about_bookings(message, tg_chat_id):
    """Отправляет сообщение пользователю о поставленном лайке"""
    send_telegram_message(message, tg_chat_id)


@shared_task
def find_active_bookings():
    habit_time = datetime.now().replace(second=0, microsecond=0)

    habit_weekday = timezone.now().today().weekday()

    bookings = get_actual_bookings()

    # bookings = Booking.objects.filter(owner__isnull=False, utc_time=habit_time)

    for b in bookings:
        tg_chat_id = b.user.tg_chat_id
        message = f"Бронирование активно [{b}]: Время: [{b.time_start}], дата: [{b.date_fied}]"

        send_information_about_bookings.delay(tg_chat_id, message)
