from datetime import datetime, timedelta, time
from restaurant.models import ContentText, ContentImage, Contentlink, ContentParameters


def get_content_text_from_postgre(title):
    try:
        return ContentText.objects.get(title=title).body
    except Exception:
        return f"Для изменения текста создайте запись '{title}' в таблице ContentText (необходимы полномочия администратора)"


def get_content_image_from_postgre(title):
    try:
        return ContentImage.objects.get(title=title)
    except Exception:
        str_part_1 = "Для изменения изображения создайте запись '"
        str_part_2 = "' в таблице ContentImage и загрузите изображение (необходимы полномочия администратора)"
        description = f"{str_part_1}{title}{str_part_2}"
        return ContentImage.objects.create(title="not_found", description=description, image=None)


def get_content_link_from_postgre(title):
    try:
        return Contentlink.objects.get(title=title)
    except Exception:
        text = f"Для создания ссылки создайте запись '{title}' в таблице ContentLink (необходимы полномочия администратора)"

        return Contentlink.objects.create(title="not_found", text="ссылка не найдена", link="#", description=text)


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
        period_of_booking = int(ContentParameters.objects.get(title="period_of_booking").body)
        work_start = time.fromisoformat(ContentParameters.objects.get(title="work_start").body)
        work_end = time.fromisoformat(ContentParameters.objects.get(title="work_end").body)
        confirm_timedelta = int(str(ContentParameters.objects.get(title="confirm_timedelta").body))

        return {"period_of_booking": period_of_booking, "work_start": work_start, "work_end": work_end,
                "confirm_timedelta": confirm_timedelta}
    except Exception:
        if ignored_error:
            work_start = time(8, 0, 0)
            work_end = time(23, 0, 0)
            period_of_booking = 14
            return {"period_of_booking": period_of_booking, "work_start": work_start, "work_end": work_end,
                    "confirm_timedelta": 45}
        return False
