from restaurant.models import ContentText, ContentImage, Contentlink


def when_not_found_content_text(title):
    return f"Для изменения текста создайте запись '{title}' в таблице ContentText (необходимы полномочия администратора)"

def when_not_found_content_image(title):
    return ContentImage.objects.create(title='not_found', description=f"Для изменения изображения создайте запись '{title}' в таблице ContentImage и загрузите изображение (необходимы полномочия администратора)", image = None)

def when_not_found_link(title):
    return f"Для создания ссылки создайте запись '{title}' в таблице ContentLink (необходимы полномочия администратора)"

def get_content_text_from_postgre(title):
    try:
        return ContentText.objects.get(title=title).body
    except:
        return when_not_found_content_text(title)

def get_content_image_from_postgre(title):
    try:
        return ContentImage.objects.get(title=title)
    except:
        return when_not_found_content_image(title)


class ContentLink:
    pass


def get_content_link_from_postgre(title):
    try:
        return Contentlink.objects.get(title=title)
    except:
        return when_not_found_link(title)