# Initial schema for Packaging Systems.
import catalog.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=180, unique=True, verbose_name="URL-имя")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Отображается")),
            ],
            options={"verbose_name": "Категория", "verbose_name_plural": "Категории", "ordering": ("sort_order", "name")},
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=180, unique=True, verbose_name="URL-имя")),
                ("title", models.CharField(max_length=180, verbose_name="Заголовок")),
                ("lead", models.TextField(blank=True, verbose_name="Вступление")),
                ("body", models.TextField(blank=True, verbose_name="Основной текст")),
                ("is_published", models.BooleanField(default=True, verbose_name="Опубликована")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
            ],
            options={"verbose_name": "Информационная страница", "verbose_name_plural": "Информационные страницы", "ordering": ("title",)},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=180, unique=True, verbose_name="URL-имя")),
                ("status", models.CharField(
                    choices=[("draft", "Черновик"), ("published", "Опубликован"), ("archived", "Архив")],
                    default="draft", max_length=12, verbose_name="Публикация",
                )),
                ("condition", models.CharField(
                    choices=[("new", "Новое"), ("used", "Б/У"), ("spare", "Запасная часть")],
                    default="used", max_length=8, verbose_name="Состояние",
                )),
                ("availability", models.CharField(
                    choices=[("available", "В наличии"), ("request", "Под заказ"), ("sold", "Продано")],
                    default="request", max_length=12, verbose_name="Наличие",
                )),
                ("summary", models.CharField(blank=True, max_length=350, verbose_name="Краткое описание")),
                ("description", models.TextField(blank=True, verbose_name="Полное описание")),
                ("manufacturer", models.CharField(blank=True, max_length=120, verbose_name="Производитель")),
                ("model_name", models.CharField(blank=True, max_length=120, verbose_name="Модель")),
                ("production_year", models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Год выпуска")),
                ("capacity_per_hour", models.PositiveIntegerField(blank=True, null=True, verbose_name="Производительность (шт/час)")),
                ("container_type", models.CharField(blank=True, max_length=150, verbose_name="Тип тары")),
                ("price", models.DecimalField(
                    blank=True, decimal_places=2, max_digits=13, null=True,
                    validators=[django.core.validators.MinValueValidator(0)], verbose_name="Цена",
                )),
                ("currency", models.CharField(
                    choices=[("KZT", "₸ (KZT)"), ("EUR", "€ (EUR)"), ("USD", "$ (USD)")],
                    default="EUR", max_length=3, verbose_name="Валюта",
                )),
                ("featured", models.BooleanField(default=False, verbose_name="На главной")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
                ("category", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, related_name="products", to="catalog.category", verbose_name="Категория",
                )),
            ],
            options={"verbose_name": "Товар", "verbose_name_plural": "Товары", "ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(
                    upload_to="products/%Y/%m/", verbose_name="Фотография",
                    validators=[
                        django.core.validators.FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"]),
                        catalog.models.validate_upload_size,
                    ],
                )),
                ("alt_text", models.CharField(blank=True, max_length=200, verbose_name="Описание фото")),
                ("is_cover", models.BooleanField(default=False, verbose_name="Главная фотография")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                ("product", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name="images", to="catalog.product", verbose_name="Товар",
                )),
            ],
            options={"verbose_name": "Фотография", "verbose_name_plural": "Фотографии", "ordering": ("-is_cover", "sort_order", "pk")},
        ),
        migrations.CreateModel(
            name="ProductSpecification",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Параметр")),
                ("value", models.CharField(max_length=300, verbose_name="Значение")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                ("product", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name="specifications", to="catalog.product", verbose_name="Товар",
                )),
            ],
            options={"verbose_name": "Характеристика", "verbose_name_plural": "Характеристики", "ordering": ("sort_order", "pk")},
        ),
        migrations.CreateModel(
            name="ProductDocument",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150, verbose_name="Название документа")),
                ("file", models.FileField(
                    upload_to="documents/%Y/%m/", verbose_name="PDF",
                    validators=[
                        django.core.validators.FileExtensionValidator(allowed_extensions=["pdf"]),
                        catalog.models.validate_upload_size,
                    ],
                )),
                ("product", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="catalog.product", verbose_name="Товар",
                )),
            ],
            options={"verbose_name": "PDF-документ", "verbose_name_plural": "PDF-документы"},
        ),
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Имя")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("phone", models.CharField(blank=True, max_length=60, verbose_name="Телефон")),
                ("company", models.CharField(blank=True, max_length=180, verbose_name="Компания")),
                ("message", models.TextField(verbose_name="Сообщение")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Получена")),
                ("consent_at", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Согласие получено")),
                ("email_sent", models.BooleanField(default=False, verbose_name="Отправлено на email")),
                ("processed", models.BooleanField(default=False, verbose_name="Обработана")),
                ("admin_note", models.TextField(blank=True, verbose_name="Заметка менеджера")),
                ("product", models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name="inquiries", to="catalog.product", verbose_name="Интересующий товар",
                )),
            ],
            options={"verbose_name": "Заявка", "verbose_name_plural": "Заявки", "ordering": ("-created_at",)},
        ),
    ]
