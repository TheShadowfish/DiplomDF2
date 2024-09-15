from datetime import datetime, timedelta, time

# from django.utils import timezone

from restaurant.models import ContentText, ContentImage, Contentlink, ContentParameters


# def when_not_found_content_text(title):
#     return f"Для изменения текста создайте запись '{title}' в таблице ContentText (необходимы полномочия администратора)"

# def when_not_found_content_image(title):
#     return ContentImage.objects.create(title='not_found', description=f"Для изменения изображения создайте запись '{title}' в таблице ContentImage и загрузите изображение (необходимы полномочия администратора)", image = None)

# def when_not_found_link(title):
#     return f"Для создания ссылки создайте запись '{title}' в таблице ContentLink (необходимы полномочия администратора)"

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

def time_segment(date: datetime.date, start: datetime.time, end: datetime.time) -> tuple[datetime, datetime]:
    # делает из даты, начального и конечного времени 2 значения datetime

    t_start = datetime(year=date.year, month=date.month, day=date.day, hour=start.hour, minute=start.minute)
    t_end = datetime(year=date.year, month=date.month, day=date.day, hour=end.hour, minute=end.minute)
    if end < start:
        t_end += timedelta(days=1)

    return t_start, t_end


def get_content_parameters(ignored_error):
    # выдернуть из базы данных параметры работы, бронирования и т.д.
    try:
        period_of_booking = int(ContentParameters.objects.get(title='period_of_booking').body)
        work_start = time.fromisoformat(ContentParameters.objects.get(title='work_start').body)
        work_end = time.fromisoformat(ContentParameters.objects.get(title='work_end').body)
        confirm_timedelta = int(str(ContentParameters.objects.get(title='confirm_timedelta')))
        # time_border = timezone.now() - confirm_timedelta




        return {'period_of_booking': period_of_booking, 'work_start': work_start, 'work_end': work_end,'confirm_timedelta': confirm_timedelta}
    except:
        # Exception as e:
        if ignored_error:
            work_start = time(8, 0, 0)
            work_end = time(23, 0, 0)
            period_of_booking = 14
            # confirm_timedelta = timezone.timedelta(minutes=45)
            # print(f"confirm_timedelta - установлено по умолчаеию (45 минут)")
            # time_border = timezone.now() - confirm_timedelta
            return {'period_of_booking': period_of_booking, 'work_start': work_start, 'work_end': work_end,
                        'confirm_timedelta': 45}
        # print(e)
        return False











# from datetime import datetime
#
# from django.core.mail import send_mail
# from django.utils import timezone
# from smtplib import SMTPException
# import pytz
#
# from config import settings
# from mailapp.models import Mailing, Client, Message, MailingLog, MailingSettings


# def get_info_and_send(mailing_item: Mailing):
#     """
#     Отправка письма
#     """
#     message = Message.objects.get(pk=mailing_item.message_id)
#     mail_title = mailing_item.message.title
#     mail_body = mailing_item.message.body
#     mail_list = Client.objects.filter(mailing=mailing_item)
#
#     print(f"message={message}...")
#     print(f"mail_from={settings.EMAIL_HOST_USER}...")
#     print(f"mail_title={mail_title}...")
#     print(f"mail_body={mail_body}...")
#     [print(f"mail_list={client.email}...") for client in mail_list]
#
#     for client in mail_list:
#         result = ''
#         if client.is_active:
#             try:
#                 result = send_mail(
#                     subject=mail_title,
#                     message=mail_body,
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[client.email],
#                     fail_silently=False,
#                 )
#
#                 log_text = f'Success!, time={timezone.now()}, mailing={mailing_item.title}, mail={client.email}'
#                 log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item, status=True, mail_answer=result)
#                 log.save()
#
#             except SMTPException as error:
#                 log_text = f"Can't send: {error}, time={timezone.now()}, mailing={mailing_item.title}, mail={client.email}"
#                 log = MailingLog.objects.create(log_text=log_text, mailing=mailing_item, status=False, mail_answer=result)
#                 log.save()
#         else:
#             print(f"Client {client} is excluded from mailing")


# def select_mailings():
#     zone = pytz.timezone(settings.TIME_ZONE)
#     current_datetime = datetime.now(zone)
#     # создание объекта с применением фильтра
#
#     # mailings = Mailing.objects.all()
#
#     setgs = MailingSettings.objects.filter(datetime_send__lte=current_datetime).filter(status=True).filter()
#
#     # mailings = Mailing.objects.filter(setgs in (setgs))
#
#     [print(f"settings={setting.__dict__}...") for setting in setgs]
#
#     # дополнение к логике: рассылки неактивных пользователей не запускаются
#     mailings2 = Mailing.objects.filter(settings__datetime_send__lte=current_datetime).filter(settings__status=True).filter(user__is_active=True)
#
#     [print(f"mailing={mailing_item.__dict__}...") for mailing_item in mailings2]
#
#     i = 1
#
#     for mailing_item in mailings2:
#         setting = MailingSettings.objects.get(pk=mailing_item.settings_id)
#         # logs = MailingLog.objects.filter(mailing=mailing_item).filter(status=True).filter(created_at > (current_datetime - timezone.timedelta(days=setting.periodicity)))
#
#         # days=, hours= - для тестирования
#         logs = MailingLog.objects.filter(mailing=mailing_item).filter(status=True).filter(
#             created_at__range=[current_datetime - timezone.timedelta(days=setting.periodicity), current_datetime])
#         [print(f"log={log.__dict__}...") for log in logs]
#
#         if logs.count() == 0:
#             print(f"{i}) mailing={mailing_item.__dict__} NO SENDED YET!")
#             i += 1
#             get_info_and_send(mailing_item)
#
#         """
#         settings: datetime_send, periodicity, status, active
#
#         class MailingLog: log_text, mailing, created_at, status, mail_answer, updated_at
#         """
