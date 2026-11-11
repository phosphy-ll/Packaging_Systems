from django.conf import settings


def site_info(request):
    return {
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
