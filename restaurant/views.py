import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from restaurant.forms import BookingForm
from restaurant.models import Booking

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
        # Что же я его owner не назвал сразу... теперь поздняк метаться.
        booking.user = user
        booking.save()



        # redirect_url = reverse('mailapp:message_settings_update', args=[message.id])

        self.success_url = reverse_lazy('restaurant:booking_list')

        return super().form_valid(form)


class BookingCreateView(LoginRequiredMixin, BookingCreateUpdateMixin, CreateView):
    model = Booking
    form_class = BookingForm

    success_url = reverse_lazy('restaurant:booking_list')  # object.pk



class BookingUpdateView(LoginRequiredMixin, BookingCreateUpdateMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('restaurant:booking_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return BookingForm
        raise PermissionDenied


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('restaurant:booking_list')

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