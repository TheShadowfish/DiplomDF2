import secrets
import string

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from config.settings import EMAIL_HOST_USER
from restaurant.models import Booking, ContentText, ContentParameters
# from mailapp.models import Mailing
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, UserToken




class GetFormKwargsGetUserMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class GetFormClassUserIsOwnerMixin:
    def get_form_class(self):
        user = self.request.user
        pk = self.kwargs.get("pk")

        print(f"{user.pk} =user.pk == self.kwargs.get('pk')= {object.pk}")

        if user.pk == self.kwargs.get("pk"):
            return UserProfileForm
        raise PermissionDenied


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    # success_url = reverse_lazy('users:confirm_email' args=[self.kwargs.get("email")])

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token

        user_token = UserToken.objects.create(token=token, user=user)
        user_token.save()

        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        # print(url)
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        redirect_url = reverse('users:confirm_email', args=[user.email])
        self.success_url = redirect_url

        # print(f'Отправлено {EMAIL_HOST_USER} to {user.email}')

        return super().form_valid(form)
    #
    # def get_success_url(self):
    #     return reverse("users:confirm_email", args=[self.kwargs.get("email")])

    # def set_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_email = self.kwargs.get("email")
    #     context['user_email'] = user_email
    #     print(f'user_email {user_email}')
    #     return context


def email_verification(request, token):
    # user = get_object_or_404(User)
    # message = Message.objects.get(pk=mailing_item.message_id)
    # mail_title = mailing_item.message.title
    # mail_body = mailing_item.message.body
    # mail_list = Client.objects.filter(mailing=mailing_item)

    this_user_token = get_object_or_404(UserToken, token=token)
    user = this_user_token.user

    try:
        confirm_timedelta = timezone.timedelta(minutes=ContentParameters.objects.get(title='confirm_timedelta'))
    except:
        confirm_timedelta = timezone.timedelta(minutes=45)
        print(f"confirm_timedelta - установлено по умолчаеию (45 минут)")

    if this_user_token.created_at < timezone.now() - confirm_timedelta:
        user.delete()
        this_user_token.delete()
        return render(request, 'users/token_expired.html')
    else:
        this_user_token.delete()
        user.is_active = True
        user.save()
        return render(request, 'users/email_confirmed.html')

    #
    # user = get_object_or_404(User, token=token)
    # user.is_active = True
    # user.save()
    # return redirect(reverse('users:login'))


def token_expired(request):
    return render(request, 'users/token_expired.html')


def email_confirmed(request):
    return render(request, 'users/email_confirmed.html')


def confirm_email(request, email):
    try:
        confirm_timedelta =ContentParameters.objects.get(title='confirm_timedelta')
    except:
        confirm_timedelta = 45
        print(f"confirm_timedelta - установлено по умолчаеию (45 минут)")

    context = {
        'email': email, 'confirm_timedelta': confirm_timedelta
    }

    return render(request, 'users/confirm_email.html', context)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = "users.view_user"



class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm




    success_url = reverse_lazy('users:profile')


    # def get_object(self, queryset=None):
    #     return self.request.user

    def get_success_url(self):
        return reverse('users:user_detail', args=[self.kwargs.get("pk")])


    # success_url = reverse_lazy('users:user_list')
    # success_url = reverse_lazy('users:user_detail', kwargs={'pk': get_object().pk})
    # success_url =  reverse_lazy('company', kwargs={'farm_id': farmid})
    # "{% url 'catalog:product_update' object.pk%}"
    # 'users/user_detail/(?P<pk>[0-9]+)/\\Z'


    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, GetFormClassUserIsOwnerMixin, DetailView):
    model = User
    # permission_required = ""
    # permission_required()
    #
    # permission_required = "users.view_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['mailing_list'] = Mailing.objects.all()

        context['booking_list'] = Booking.objects.filter(user=self.object)

        user = self.request.user
        pk = self.kwargs.get("pk")

        # print(f"{user.pk} =user.pk == self.kwargs.get('pk')= {pk}")
        if user.is_moderator or user.pk == pk:
            return context
        else:
            raise PermissionDenied





    # def get_form_class(self):
    #     user = self.request.user
    #     pk = self.kwargs.get("pk")
    #
    #     print(f"{user.pk} =user.pk == self.kwargs.get('pk')= {object.pk}")
    #
    #     if user.pk == self.kwargs.get("pk"):
    #         return UserProfileForm
    #     raise PermissionDenied




class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    # Суперпользователь сможет
    permission_required = "users.delete_user"
    success_url = reverse_lazy('users:user_list')


def password_recovery(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        print(f'Получен адрес {email}')

        user = get_object_or_404(User, email=email)

        print(f'Пользователь {user}')

        password = ''

        # Создание двенадцатисимвольного буквенно-цифрового пароля, содержащего как минимум один символ нижнего регистра,
        # как минимум один символ верхнего регистра и как минимум три цифры:
        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(12))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break

        print(f'Пароль {password}')

        message = f"Привет, держи новый сложный 12-ти символьный пароль, который ты тоже забудешь: {password}. \
                    Если вы не запрашивали восстановление пароля, просто игнорируйте это сообщение."

        print(f'Пароль {message}')

        send_mail(
            subject='Восстановление пароля',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email]
        )
        # пароль шифрует  - как его дальше в шифрованом виде в базу сохранять?
        # psw = make_password(password, salt=None, hasher='default')

        user.set_password(password)
        user.save()
        return redirect(reverse('users:login'))

    return render(request, 'users/password_recovery.html')


@login_required
@permission_required('users.can_set_user_inactive')
def toggle_activity_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
        user.is_banned = True
    else:
        user.is_active = True
        user.is_banned = False

    user.save()

    return redirect(reverse('users:user_list'))
