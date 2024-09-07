from django.shortcuts import render
from django.views.generic import TemplateView


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
