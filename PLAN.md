Готов подробный план работы над проектом.

1 неделя. Репозиторий с основными файлами (джанго), 
реализовано создание пользователей, регистрация, подтверждение регистрации.

**Создание приложения по типу MVP** (Minimum Viable Product, минимально жизнеспособный продукт.
Решение об этом в связи с ОЧЕНЬ большим количеством возможных функций касательно бронирования мест в ресторане)
К примеру: 
# [здесь находится бэклог]
- выбор мест на схеме зала, 
- подписка на ожидание освобождения мест,
- возможность долгосрочного бронирования с настройками на сколько дней вперед оно открывается
- временные интервалы включающие не только часы, но и минуты
- заказ блюд заранее + вывод меню на данный день, 
- 3D схема зала, 
- рассылки постоянным клиентам, 
- настройка напоминаний в WhatsApp и Telegram,
- размещение статей на сайте ресторана (для привлечения клиентов)
- Настройка работы с разными часовыми поясами при выводе информации и рассылках (в данный момент работа только с пользователями в зоне UTC+3)
- бронирование по предоплате, а то забронируют и не приходят >:D

И ЭТО ЕЩЕ МАЛАЯ ЧАСТЬ.


# [спринт №1]
Данная версия позволяет 
- бронировать столик на 1 или 2 часа в течение данных суток или следующих
в период, соответствующий графику работы ресторана (настраивается), 
- учитывает, забронирован ли данный столик, на сайте есть показ информации об этом,
- позволяет бронировать только свободные столики.
- бронирование только на авторизованного пользователя
- пользователь может просматривать историю бронирования
- (если разрешит руководитель - напоминание о забронированом столике отсылает за 2 часа на телеграм пользователю через celery)
Условие по умолчанию: все столики поддерживают от 1 до 4 мест, 
бронируются на одного пользователя, 
если надо больше то бронируется второй столик в то же время


2 неделя. Реализован и протестирован функционал, написаны тесты, оформлен черновик презентации.
Сдан проект на проверку

# [13.09 - 14:51, оставшиеся работы]
~~сортировка списка бронирований~~
~~изменение поведения кнопки активировать~~ - вообще не нужна такая кнопка, с ней логика ломается 
~~отключение редактирования прошедших бронирований~~ ну вообще-то запрета нет, просто не реализованы ссылки на это
~~стиль страницы сделать так же как главная~~
~~чистка списка от неактивных бронирований или проверка на возможность подтверждения~~
~~не показывать прошедшие бронирования~~ часть даже из проверки исключил, такая себе оптимизация конечно, но лучше чем ничего
~~контент и картинки прикрутить из базы~~
ОТМЕНА ПО ВРЕМЕНИ прикрутить отзывы
~~прикрутить вопросы (ответ может давать админ и контент-менеджер) - предварительная проверка инклюдед?~~
ОТМЕНА ПО ВРЕМЕНИ прикрутить блог (он же наши блюда, залить туда 6-7-9 блюд и пагинацию сделать по 3 - заливать туда сможет контент-менеджер)

~~далее прикрутить кеширование~~

~~прикрутить тестирование~~

~~перенести параметры в .env~~


прикрутить celery
прикрутить телеграм

~~почистить лишний код и прогнать flake~~

закрутить в docker
(да как вообще поймут что docker используется по коду в гитхабе?? шиза)

оплатить хостинг, залить, проверить
презентация тоже нужна
