from django import template
from django.utils.translation import get_language
from catalog.i18n import translate

register = template.Library()

@register.simple_tag(takes_context=True)
def tr(context, value):
    request = context.get("request")
    return translate(value, getattr(request, "site_lang", "ru"))

@register.filter
def localized(obj, field_name):
    """Use admin-managed fields and fall back to the Russian original."""
    original = getattr(obj, field_name, "")
    lang = get_language()
    if lang not in ("kk", "en"):
        return original
    translated_field = f"{field_name}_{lang}"
    if hasattr(obj, translated_field):
        return getattr(obj, translated_field) or original
    if hasattr(obj, "translations"):
        translated = next(
            (item for item in obj.translations.all() if item.language == lang),
            None,
        )
        if translated:
            return getattr(translated, field_name, "") or original
    return original

@register.filter
def t(value, lang):
    return translate(value, lang)
