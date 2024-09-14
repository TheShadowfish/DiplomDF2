from restaurant.models import ContentText


def when_not_found_content_text(title):
    return f"Для изменения текста создайте запись '{title}' в таблице ContentText (необходимы полномочия администратора)"

def when_not_found_content_image(title):
    return (f"Для изменения изображения создайте запись '{title}' в таблице ContentImage и загрузите изображение (необходимы полномочия администратора)",
    "{ % static 'image/no_image.png' %}")

def when_not_found_link(title):
    return f"Для создания ссылки создайте запись '{title}' в таблице ContentLink (необходимы полномочия администратора)"

def get_content_text_from_postgre(title):
    try:
        return ContentText.objects.get(title=title).body
    except:
        return when_not_found_content_text(title)