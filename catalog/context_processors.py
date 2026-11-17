from django.conf import settings
import re
from .i18n import LANGUAGES


def site_info(request):
    form_id = settings.FORMSPREE_FORM_ID if re.fullmatch(r"[a-zA-Z0-9]{6,24}", settings.FORMSPREE_FORM_ID) else ""
    return {
        "static_export": settings.STATIC_EXPORT,
        "formspree_form_id": form_id,
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
