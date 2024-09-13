import os
import secrets


from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from config.settings import EMAIL_HOST_USER
from restaurant.forms import BookingForm
from restaurant.models import Booking, Table, BookingToken

from dotenv import load_dotenv
load_dotenv()

class HomePageView(TemplateView):
    template_name = "restaurant/home.html"

    # def get_context_data(self, **kwargs):
    #     """
    #     - количество рассылок всего,
    #     - количество активных рассылок,
    #     - количество уникальных клиентов для рассылок,
    #     - три случайные статьи из блога.
    #
    #     :param kwargs:
    #     :return:
    #     """
    #     context = super().get_context_data(**kwargs)
    #     # количество рассылок всего
    #     context["mailings_count"] = len(Mailing.objects.all())
    #     # количество активных рассылок
    #     context["mailings_count_active"] = len(Mailing.objects.filter(settings__status=True))
    #
    #     # количество уникальных клиентов для рассылок
    #     emails_unique = Client.objects.values('email').annotate(total=Count('id'))
    #     context["emails_unique"] = emails_unique
    #     context["emails_unique_count"] = len(emails_unique)
    #     # три случайные статьи из блога
    #
    #     # наверняка это можно более оптимально получить, надо спросить как
    #     # чем весь список статей из базы тянуть
    #     article_list_len = len(Article.objects.all())
    #
    #     # article_list_len_2 = Article.objects.Count()
    #
    #     context["article_list_len"] = article_list_len
    #
    #     valid_profiles_id_list = Article.objects.values_list('id', flat=True)
    #     random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 3))
    #     # context["random_articles"] = Article.objects.filter(id__in=random_profiles_id_list)
    #     # = get_cached_article_list()
    #     context["random_articles"] = get_cached_article_list().filter(id__in=random_profiles_id_list)
    #
    #     # def sample(self, population, k, *, counts=None):
    #
    #     return context

class AboutUsPageView(TemplateView):
    template_name = "restaurant/about_us.html"

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    login_url = "users:login"

    # redirect_field_name = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['only_users'] = os.getenv("ONLY_USERS_PROPERTY")
        return context


class BookingCreateUpdateMixin:

    # def get_context_data(self, **kwargs):
    #     context['formset'] = mail_form_set()
    #     return context

    def form_valid(self, form):

        # Xозяином рассылки автоматически становится тот, кто её создал
        booking = form.save()
        user = self.request.user
        booking.user = user
        booking.active = False


        token = secrets.token_hex(16)
        email = user.email

        booking.save()

        booking_token = BookingToken.objects.create(token=token, booking=booking)
        booking_token.save()

        host = self.request.get_host()
        url = f'http://{host}/booking_verification/{token}/'
        # print(url)
        send_mail(
            subject='Подтверждение бронирования',
            message=f'Привет, перейди по ссылке для подтверждения бронирования: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[email]
        )

        # redirect_url = reverse('restaurant:booking_verification', args=[email])
        # self.success_url = redirect_url

        # print(f'Отправлено {EMAIL_HOST_USER} to {user.email}')

        return super().form_valid(form)
    def get_success_url(self):
        user = self.request.user
        email = user.email
        return reverse('restaurant:confirm_booking', args=[email])



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['mailing_list'] = Mailing.objects.all()
        # как пустые столики выкинуть?
        Tables = Table.objects.all()
        Bookings = Booking.objects.all()

        TBList = []

        for t in Tables:
            for b in Bookings:
                if b.table == t and t not in TBList:
                    TBList.append(t)

        context['tables_list'] = TBList
        # context['tables_list'] = Table.objects.all()
        context['booking_list'] = Booking.objects.all()
        return context



def confirm_booking(request, email):
    context = {
        'email': email,
    }
    return render(request, 'restaurant/confirm_booking.html', context)

def booking_verification(request, token):
    # user = get_object_or_404(User)
    # message = Message.objects.get(pk=mailing_item.message_id)
    # mail_title = mailing_item.message.title
    # mail_body = mailing_item.message.body
    # mail_list = Client.objects.filter(mailing=mailing_item)

    this_booking_token = get_object_or_404(BookingToken, token=token)
    booking = this_booking_token.booking

    if this_booking_token.created_at < timezone.now() - timezone.timedelta(minutes=45):
        booking.delete()
        this_booking_token.delete()
        return render(request, 'restaurant/token_expired.html')
    else:
        this_booking_token.delete()
        booking.active = True
        booking.save()
        return render(request, 'restaurant/booking_confirmed.html')

    #
    # user = get_object_or_404(User, token=token)
    # user.is_active = True
    # user.save()
    # return redirect(reverse('users:login'))


def token_expired(request):
    return render(request, 'restaurant/token_expired.html')


def email_confirmed(request):
    return render(request, 'restaurant/booking_confirmed.html')


class BookingCreateView(LoginRequiredMixin, BookingCreateUpdateMixin, CreateView):
    model = Booking
    form_class = BookingForm

    # success_url = reverse_lazy('restaurant:booking_list')  # object.pk

    # def get_success_url(self):
    #     user_pk = self.request.user.pk
    #     return reverse('users:user_detail', kwargs={'pk': user_pk})



class BookingUpdateView(LoginRequiredMixin, BookingCreateUpdateMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    # success_url = reverse_lazy('restaurant:booking_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return BookingForm
        raise PermissionDenied

    # def get_success_url(self):
    #     user_pk = self.request.user.pk
    #     return reverse('users:user_detail', kwargs={'pk': user_pk})


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    # success_url = reverse_lazy('restaurant:booking_list')
    def get_success_url(self):
        user_pk = self.request.user.pk
        return reverse('users:user_detail', kwargs={'pk': user_pk})


    def form_valid(self, form):
        user = self.request.user
        if user == self.object.user:
            return
        else:
            raise PermissionDenied


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['logs'] = MailingLog.objects.filter(mailing=self.object)
    #     context['clients'] = Client.objects.filter(mailing=self.object)
    #     context['message'] = Message.objects.get(id=self.object.message_id)
    #     context['settings'] = MailingSettings.objects.get(id=self.object.settings_id)
    #     return context

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.user or user.is_moderator:
            return
        else:
            raise PermissionDenied



# class MailingListView(LoginRequiredMixin, ListView):
#     model = Mailing
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['only_send'] = False
#         return context
#
# class MailingListViewSend(LoginRequiredMixin, ListView):
#     model = Mailing
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['only_send'] = True
#         return context

def toggle_activity_booking(request, pk):
    booking_item = get_object_or_404(Booking, pk=pk)
    if booking_item.active:
        booking_item.active = False
    else:
        booking_item.active = True

    booking_item.save()

    user_pk = booking_item.user.pk
    return redirect(reverse('users:user_detail', kwargs={'pk': user_pk}))