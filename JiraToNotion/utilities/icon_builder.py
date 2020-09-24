from constants.icons import Icon
from constants.theme import Theme


def get_icon(icon: Icon, theme: Theme):
    url = __icon_to_url(icon)
    if theme == Theme.DARK:
        url.replace("000000", "FFFFFF")
    return url


def __icon_to_url(icon: Icon):
    switcher = {
        Icon.DEV: "https://img.icons8.com/ios/250/000000/source-code.png",
    }

    return switcher.get(icon, "")
