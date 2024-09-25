# from django.contrib.sites import requests
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from config import settings
import requests

from django.core.cache import cache
from restaurant.models import Booking, Questions


def send_telegram_message(chat_id, message):
    """Функция отправки сообщения в телеграм"""

    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params)


def send_email_message(subject, message, recipient_list):
    print(f"subject = {subject}, message = {message}, from_email (EMAIL_HOST_USER) = {EMAIL_HOST_USER}, "
          f"recipient_list = {recipient_list}")

    send_mail(
        subject=subject,
        message=str(message),
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list
    )



def get_cached_booking_list(recached: bool = False):
    if settings.CACHE_ENABLED:
        key = "booking_list"
        if recached:
            booking_list = Booking.objects.all()
            cache.set(key, booking_list)
        else:
            booking_list = cache.get(key)
            if booking_list is None:
                booking_list = Booking.objects.all()
                cache.set(key, booking_list)
    else:
        booking_list = Booking.objects.all()
    return booking_list


def get_cached_questions_list(recached: bool = False):
    if settings.CACHE_ENABLED:

        key = "questions_list"
        if recached:
            questions_list = Questions.objects.all()
            cache.set(key, questions_list)

        else:
            questions_list = cache.get(key)
            if questions_list is None:
                questions_list = Questions.objects.all()
                cache.set(key, questions_list)
    else:
        questions_list = Questions.objects.all()
    return questions_list


def cache_delete_booking_list():
    key = "booking_list"
    cache.delete(key)


def cache_delete_question_list():
    key = "questions_list"
    cache.delete(key)


def cache_clear():
    cache.clear()
