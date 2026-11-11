from django.utils import translation
from .i18n import LANGUAGES


class SiteLanguageMiddleware:
    """Persist the chosen language via session and Django translation context."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        selected = request.GET.get("lang")
        if selected in LANGUAGES:
            request.session["site_lang"] = selected
        lang = request.session.get("site_lang", "ru")
        if lang not in LANGUAGES:
            lang = "ru"
        request.site_lang = lang
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        try:
            return self.get_response(request)
        finally:
            translation.deactivate()
