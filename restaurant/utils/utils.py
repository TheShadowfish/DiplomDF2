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
