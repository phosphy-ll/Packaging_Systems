from django.conf import settings
from .i18n import LANGUAGES


def site_info(request):
    return {
        "static_export": settings.STATIC_EXPORT,
        "site_lang": getattr(request, "site_lang", "ru"),
        "site_languages": LANGUAGES,
        "company_email": settings.COMPANY_EMAIL,
        "nav_sections": [
            ("Линии розлива", "filling-lines"),
            ("Узлы оборудования", "equipment-units"),
            ("Водоподготовка", "water-treatment"),
            ("Б/У линии", "used-lines"),
            ("Запасные части", "spare-parts"),
            ("Сервис", "service"),
        ],
    }
