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
    original = getattr(obj, field_name, "")
    lang = get_language()
    if lang == "ru" or not hasattr(obj, "translations"):
        return original
    translation = next((x for x in obj.translations.all() if x.language == lang), None)
    return getattr(translation, field_name, "") or original

@register.filter
def t(value, lang):
    return translate(value, lang)
