from django.test import TestCase
from users.models import User, UserToken


# email = models.EmailField(max_length=150, verbose_name='почта', unique=True, help_text='Введите вашу почту')
#     name = models.CharField(max_length=150, verbose_name='имя пользователя', help_text='Введите ваше имя', **NULLABLE)
#     description = models.TextField(verbose_name='описание', help_text='Введите дополнительную информацию', **NULLABLE)
#     phone_number = PhoneNumberField(**NULLABLE, verbose_name='телефон', help_text='Введите ваш номер телефона')
#     phone_number = PhoneNumberField(**NULLABLE, verbose_name='телефон', help_text='Введите ваш номер телефона')
#     avatar = models.ImageField(upload_to='users/avatars', verbose_name='аватар', help_text='Выберите аватар',
#                                **NULLABLE)
#
#     tg_nick = models.CharField(max_length=50, **NULLABLE, verbose_name="Tg name", help_text="Укажите telegram-ник",)
#
#     tg_chat_id = models.CharField(max_length=50, verbose_name="Телеграм chat-id", help_text="Укажите телеграм chat-id",  **NULLABLE,)
#     time_offset = models.IntegerField(default=3, verbose_name="Смещение часового пояса", help_text="От -12 до +14, по умолчанию UTC+3 (Московское время)")
class UserTest(TestCase):
    # fixtures = ['test_data.json']

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(email='test_user@test.ru', name='user', password='test')
        test_user.save()

    def test_user_labels(self):
        test_user = User.objects.get(email='test_user@test.ru')

        email_label = test_user._meta.get_field('email').verbose_name
        name_label = test_user._meta.get_field('name').verbose_name
        description_label = test_user._meta.get_field('description').verbose_name
        phone_number_label = test_user._meta.get_field('phone_number').verbose_name
        avatar_label = test_user._meta.get_field('avatar').verbose_name
        tg_nick_label = test_user._meta.get_field('tg_nick').verbose_name
        tg_chat_id_label = test_user._meta.get_field('tg_chat_id').verbose_name
        time_offset_label = test_user._meta.get_field('time_offset').verbose_name

        self.assertEquals(email_label, 'почта')
        self.assertEquals(name_label, 'имя пользователя')
        self.assertEquals(description_label, 'описание')
        self.assertEquals(phone_number_label, 'телефон')
        self.assertEquals(avatar_label, 'аватар')
        self.assertEquals(tg_nick_label, 'Tg name')
        self.assertEquals(tg_chat_id_label, 'Телеграм chat-id')
        self.assertEquals(time_offset_label, 'Смещение часового пояса')

    def test_review_sign_max_length(self):
        test_user = User.objects.get(email='test_user@test.ru')

        email_length = test_user._meta.get_field('email').max_length
        name_length = test_user._meta.get_field('name').max_length
        tg_nick_length = test_user._meta.get_field('tg_nick').max_length
        tg_chat_id_length = test_user._meta.get_field('tg_chat_id').max_length

        self.assertEquals(email_length, 150)
        self.assertEquals(name_length, 150)
        self.assertEquals(tg_nick_length, 50)
        self.assertEquals(tg_chat_id_length, 50)

    def test_review_str(self):
        user = User.objects.get(email='test_user@test.ru')
        expected_object_name = f"{user.name} ({user.email})"
        self.assertEquals(expected_object_name, str(user))


class UserTokenTest(TestCase):
    # fixtures = ['test_data.json']

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(email='test_user@test.ru', name='user', password='test')
        test_user.save()

        token=UserToken.objects.create(user=test_user, token='test_token')
        token.save()

    def test_user_token_label(self):
        test_user = User.objects.get(email='test_user@test.ru')
        token = UserToken.objects.get(user=test_user)

        user_label = token._meta.get_field('user').verbose_name
        self.assertEquals(user_label, 'пользователь к которому относится токен')

        token_label = token._meta.get_field('token').verbose_name
        self.assertEquals(token_label, 'Token')

        created_at_label = token._meta.get_field('created_at').verbose_name
        self.assertEquals(created_at_label, 'дата создания')


    def test_user_token_max_length(self):
        test_user = User.objects.get(email='test_user@test.ru')
        token = UserToken.objects.get(user=test_user)

        token_length = token._meta.get_field('token').max_length
        self.assertEquals(token_length, 100)