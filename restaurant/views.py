import os
import secrets
from datetime import datetime, timedelta

# from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from config.settings import EMAIL_HOST_USER
from restaurant.forms import BookingForm
from restaurant.models import Booking, Table, BookingToken, ContentText, ContentParameters

from dotenv import load_dotenv

from restaurant.templates.restaurant.utils import when_not_found_content_text, get_content_text_from_postgre

load_dotenv()

class HomePageView(TemplateView):
    template_name = "restaurant/home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # количество рассылок всего
        CONST1 = "home-about"
        CONST2 = "home-offer"
        CONST3 = "home-adress"

        context[CONST1.replace('-','_')] = get_content_text_from_postgre(CONST1)
        context[CONST2.replace('-', '_')] = get_content_text_from_postgre(CONST2)
        context[CONST3.replace('-', '_')] = get_content_text_from_postgre(CONST3)


        # try:
        #     context[CONST1.replace('-','_')] = ContentText.objects.get(title=CONST1).body
        # except:
        #     context[CONST1.replace('-','_')] = when_not_found_content_text(CONST1)
        # try:
        #     context[CONST2.replace('-','_')] = ContentText.objects.get(title=CONST2).body
        # except:
        #     context[CONST2.replace('-','_')] = when_not_found_content_text(CONST2)
        # try:
        #     context[CONST3.replace('-','_')] = ContentText.objects.get(title=CONST3).body
        # except:
        #     context[CONST3.replace('-','_')] = when_not_found_content_text(CONST3)
        # context["home-offer"] = ContentText.objects.get(title="home-offer")
        # context["home-adress"] = ContentText.objects.get(title="home-adress")
        #
        # # количество активных рассылок
        # context["mailings_count_active"] = len(Mailing.objects.filter(settings__status=True))
        #
        # # количество уникальных клиентов для рассылок
        # emails_unique = Client.objects.values('email').annotate(total=Count('id'))
        # context["emails_unique"] = emails_unique
        # context["emails_unique_count"] = len(emails_unique)
        # # три случайные статьи из блога
        #
        # # наверняка это можно более оптимально получить, надо спросить как
        # # чем весь список статей из базы тянуть
        # article_list_len = len(Article.objects.all())
        #
        # # article_list_len_2 = Article.objects.Count()
        #
        # context["article_list_len"] = article_list_len
        #
        # valid_profiles_id_list = Article.objects.values_list('id', flat=True)
        # random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 3))
        # # context["random_articles"] = Article.objects.filter(id__in=random_profiles_id_list)
        # # = get_cached_article_list()
        # context["random_articles"] = get_cached_article_list().filter(id__in=random_profiles_id_list)
        #
        # # def sample(self, population, k, *, counts=None):

        return context

class AboutUsPageView(TemplateView):
    template_name = "restaurant/about_us.html"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # количество рассылок всего
        CONST1 = "about_us-mission-part"
        CONST2 = "about_us-history-part1"
        CONST3 = "about_us-history-part2"
        CONST4 = "about_us-command-part1"
        CONST5 = "about_us-command-part2"

        context[CONST1.replace('-','_')] = get_content_text_from_postgre(CONST1)
        context[CONST2.replace('-', '_')] = get_content_text_from_postgre(CONST2)
        context[CONST3.replace('-', '_')] = get_content_text_from_postgre(CONST3)
        context[CONST4.replace('-', '_')] = get_content_text_from_postgre(CONST4)
        context[CONST5.replace('-', '_')] = get_content_text_from_postgre(CONST5)

        #
        #
        # try:
        #     context[CONST1.replace('-','_')] = ContentText.objects.get(title=CONST1).body
        # except:
        #     context[CONST1.replace('-','_')] = when_not_found_content_text(CONST1)
        # try:
        #     context[CONST2.replace('-','_')] = ContentText.objects.get(title=CONST2).body
        # except:
        #     context[CONST2.replace('-','_')] = when_not_found_content_text(CONST2)
        # try:
        #     context[CONST3.replace('-','_')] = ContentText.objects.get(title=CONST3).body
        # except:
        #     context[CONST3.replace('-','_')] = when_not_found_content_text(CONST3)
        #
        # try:
        #     context[CONST4.replace('-','_')] = ContentText.objects.get(title=CONST4).body
        # except:
        #     context[CONST4.replace('-','_')] = when_not_found_content_text(CONST4)
        # try:
        #     context[CONST5.replace('-','_')] = ContentText.objects.get(title=CONST5).body
        # except:
        #     context[CONST5.replace('-','_')] = when_not_found_content_text(CONST5)

        # context["home-offer"] = ContentText.objects.get(title="home-offer")
        # context["home-adress"] = ContentText.objects.get(title="home-adress")
        #
        # # количество активных рассылок
        # context["mailings_count_active"] = len(Mailing.objects.filter(settings__status=True))
        #
        # # количество уникальных клиентов для рассылок
        # emails_unique = Client.objects.values('email').annotate(total=Count('id'))
        # context["emails_unique"] = emails_unique
        # context["emails_unique_count"] = len(emails_unique)
        # # три случайные статьи из блога
        #
        # # наверняка это можно более оптимально получить, надо спросить как
        # # чем весь список статей из базы тянуть
        # article_list_len = len(Article.objects.all())
        #
        # # article_list_len_2 = Article.objects.Count()
        #
        # context["article_list_len"] = article_list_len
        #
        # valid_profiles_id_list = Article.objects.values_list('id', flat=True)
        # random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 3))
        # # context["random_articles"] = Article.objects.filter(id__in=random_profiles_id_list)
        # # = get_cached_article_list()
        # context["random_articles"] = get_cached_article_list().filter(id__in=random_profiles_id_list)
        #
        # # def sample(self, population, k, *, counts=None):

        return context

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

        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        email = user.email
        return reverse('restaurant:confirm_booking', args=[email])



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # получение времени подтверждения бронирования, получение времени, которое определяет границу регистрации
        try:
            confirm_timedelta = timezone.timedelta(
                minutes=ContentParameters.objects.get(title='confirm_timedelta'))
        except:
            confirm_timedelta = timezone.timedelta(minutes=45)
            # print(f"confirm_timedelta - установлено по умолчаеию (45 минут)")
        time_border = timezone.now() - confirm_timedelta

        # список pk бронирований, которые могут быть подтверждены
        booking_tokens = [token.booking.pk for token in  BookingToken.objects.filter(created_at__gt=time_border)]

        not_has_been_tokens = [token.booking.pk for token in BookingToken.objects.filter(created_at__gt=time_border)]

        # qte

        # now = Booking.objects.filter(date_field__year__gte=date_now.year, date_field__month__gte=date_now.month, date_field__day__gte=date_now.day,
        #                             time_end__time__hour__gte=date_now.hour, time_end__time__minute__gte=date_now.minute)

        # ну 3.14159здец конечно...
        date_now = datetime.now()
        # для начала
        now = Booking.objects.filter(date_field__year__gte=date_now.year, date_field__month__gte=date_now.month, date_field__day__gte=(date_now - timedelta(days=1)).day)

        # теперь проще найти бронирования, которые еще дляться
        still_is = []
        for n in now:
            n_end = datetime(year=n.date_field.year, month=n.date_field.month,
                                      day=n.date_field.day, hour=n.time_end.hour,
                                      minute=n.time_end.minute)
            if n.time_start > n.time_end:
                n_end += timedelta(days=1)

            if n_end > date_now:
                still_is.append(n.pk)


        # for n in Booking.objects.filter(pk__in=still_is).order_by("date_field", "time_start"):
        #     print(f"now: {n} {n.date_field} {n.time_end}")

        # получение списка актуальных бронирований
        # unfiltered_booking = Booking.objects.filter(Q(active=True) | Q(pk__in=booking_tokens))
        bookings = Booking.objects.filter(pk__in=still_is).filter(Q(active=True) | Q(pk__in=booking_tokens)).order_by("date_field", "time_start")

        # получение списка задействованных столиков
        table_pk = [b.table.pk for b in bookings]
        tables = Table.objects.filter(pk__in=table_pk).order_by("number")
        # TBList = []
        #
        # for t in Table.objects.order_by("number"):
        #     for b in bookings:
        #         if b.table == t and t not in TBList:
        #             TBList.append(t)

        context['tables_list'] = tables

        context['booking_list'] = bookings

        context['period_of_booking'] = ContentParameters.objects.get(title='period_of_booking').body
        context['work_start'] = ContentParameters.objects.get(title='work_start').body
        context['work_end'] = ContentParameters.objects.get(title='work_end').body

        CONST1 = "booking_create"
        context[CONST1.replace('-','_')] = get_content_text_from_postgre(CONST1)
        # context['booking_list'] = Booking.objects.all()
        return context




def confirm_booking(request, email):

    try:
        confirm_timedelta = ContentParameters.objects.get(title='confirm_timedelta')
    except Exception as e:
        confirm_timedelta = 45
        print(f"confirm_timedelta - установлено по умолчаеию (45 минут) {e}")

    context = {
        'email': email, 'confirm_timedelta': confirm_timedelta
    }
    return render(request, 'restaurant/confirm_booking.html', context)

def booking_verification(request, token):


    this_booking_token = get_object_or_404(BookingToken, token=token)
    booking = this_booking_token.booking

    try:
        confirm_timedelta = timezone.timedelta(minutes=ContentParameters.objects.get(title='confirm_timedelta'))
    except:
        confirm_timedelta = timezone.timedelta(minutes=45)
        print(f"confirm_timedelta - установлено по умолчаеию (45 минут)")


    if this_booking_token.created_at < timezone.now() - confirm_timedelta:
        booking.delete()
        this_booking_token.delete()
        return render(request, 'restaurant/token_expired.html')
    else:
        this_booking_token.delete()
        booking.active = True
        booking.save()
        return render(request, 'restaurant/booking_confirmed.html')


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


    def form_valid(self, form):
        user = self.request.user
        if user == self.object.user or user.is_moderator:
            return
        else:
            raise PermissionDenied


def toggle_activity_booking(request, pk):
    booking_item = get_object_or_404(Booking, pk=pk)
    if booking_item.active:
        booking_item.active = False
    else:
        booking_item.active = True

    booking_item.save()

    user_pk = booking_item.user.pk
    return redirect(reverse('users:user_detail', kwargs={'pk': user_pk}))