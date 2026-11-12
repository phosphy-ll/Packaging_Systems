"""Initial translations for categories and specifications found in company materials.

Translations are seeded only for matching source values. Edited admin data is
never overwritten; untranslated fields fall back to the original Russian text.
"""
from .models import Category, Product, ProductSpecification

CATEGORY_TEXT = {
    "filling-lines": ("Линии розлива", "Құю желілері", "Filling lines"),
    "equipment-units": ("Узлы и оборудование", "Жабдық тораптары", "Equipment units"),
    "water-treatment": ("Системы водоподготовки", "Су дайындау жүйелері", "Water treatment systems"),
    "used-lines": ("Б/У линии", "Қолданылған желілер", "Used lines"),
    "spare-parts": ("Запасные части", "Қосалқы бөлшектер", "Spare parts"),
}

# Source names/values from the Bertolaso presentation as entered in the catalog.
SPEC_TEXT = {
    "Производительность": (
        "Требует проверки: в названии 8 000 бут/ч, для триблока указано 10 000 бут/ч",
        ("Өнімділік",
         "Тексеру қажет: желі атауында 8 000 бөтелке/сағ, триблок үшін 10 000 бөтелке/сағ көрсетілген"),
        ("Capacity",
         "Verification required: line title states 8,000 bottles/hour, while the triblock states 10,000 bottles/hour"),
    ),
    "Общая производительность (по презентации)": (
        "8 000 бут/час; триблок: 10 000 бут/час (уточнить)",
        ("Жалпы өнімділік (презентация бойынша)",
         "8 000 бөтелке/сағ; триблок: 10 000 бөтелке/сағ (нақтылау қажет)"),
        ("Overall capacity (per presentation)",
         "8,000 bottles/hour; triblock: 10,000 bottles/hour (to be verified)"),
    ),
    "Триблок": (
        "Bertolaso 40.40.6, 2006 г.",
        ("Триблок", "Bertolaso 40.40.6, 2006 ж."),
        ("Rinsing/filling/capping triblock", "Bertolaso 40.40.6, 2006"),
    ),
    "Этикетировщик": (
        "PE Универсал-Мастер, 2004 г., 16 столиков",
        ("Затбелгі жапсыру машинасы", "PE Универсал-Мастер, 2004 ж., 16 позиция"),
        ("Labeling machine", "PE Universal-Master, 2004, 16 stations"),
    ),
    "Коробоформовщик": (
        "APSOL, 2015 г.",
        ("Қорап құрастыру машинасы", "APSOL, 2015 ж."),
        ("Case erector", "APSOL, 2015"),
    ),
    "Укладчик коробов": (
        "APSOL, 2015 г.",
        ("Қорапқа салу машинасы", "APSOL, 2015 ж."),
        ("Case packer", "APSOL, 2015"),
    ),
    "Компрессор": (
        "Atlas Copco, 8,5 бар",
        ("Компрессор", "Atlas Copco, 8,5 бар"),
        ("Compressor", "Atlas Copco, 8.5 bar"),
    ),
    "Конвейеры": (
        "PROCONV-CHAIN",
        ("Конвейерлер", "PROCONV-CHAIN"),
        ("Conveyors", "PROCONV-CHAIN"),
    ),
    "Условия": (
        "EXW Incoterms 2020, Казахстан",
        ("Жеткізу шарттары", "EXW Incoterms 2020, Қазақстан"),
        ("Delivery terms", "EXW Incoterms 2020, Kazakhstan"),
    ),
}


def seed_catalog_translations():
    """Fill blank translation fields for known unchanged Russian entries only."""
    for slug, (ru, kk, en) in CATEGORY_TEXT.items():
        category = Category.objects.filter(slug=slug).first()
        if category is None or category.name != ru:
            continue
        changes = []
        for field_name, translated in (("name_kk", kk), ("name_en", en)):
            if not getattr(category, field_name):
                setattr(category, field_name, translated)
                changes.append(field_name)
        if changes:
            category.save(update_fields=changes)

    product = Product.objects.filter(
        slug="liniya-rozliva-bertolaso-40-40-6"
    ).first()
    if product is None:
        return
    for spec in ProductSpecification.objects.filter(product=product):
        translated = SPEC_TEXT.get(spec.name)
        if translated is None or spec.value != translated[0]:
            continue
        updates = []
        for code, (name, value) in (("kk", translated[1]), ("en", translated[2])):
            for field, translated_value in (
                (f"name_{code}", name),
                (f"value_{code}", value),
            ):
                if not getattr(spec, field):
                    setattr(spec, field, translated_value)
                    updates.append(field)
        if updates:
            spec.save(update_fields=updates)
