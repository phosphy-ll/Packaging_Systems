"""Catalog, editable content and customer inquiries."""
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify as django_slugify


TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e",
    "ё": "yo", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y", "ь": "",
    "э": "e", "ю": "yu", "я": "ya",
}


def safe_slug(value):
    latin = "".join(TRANSLIT.get(char.lower(), char.lower()) for char in value)
    return django_slugify(latin)[:170] or f"item-{uuid.uuid4().hex[:8]}"


def ensure_slug(instance, source):
    if instance.slug:
        return
    base = safe_slug(source)
    proposed = base
    counter = 2
    while type(instance).objects.filter(slug=proposed).exclude(pk=instance.pk).exists():
        proposed = f"{base}-{counter}"
        counter += 1
    instance.slug = proposed


def validate_upload_size(uploaded):
    if uploaded.size > 20 * 1024 * 1024:
        raise ValidationError("Максимальный размер файла: 20 МБ.")


class Category(models.Model):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("URL-имя", unique=True, max_length=180, blank=True)
    description = models.TextField("Описание", blank=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Отображается", default=True)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        ensure_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликован"
        ARCHIVED = "archived", "Архив"

    class Condition(models.TextChoices):
        NEW = "new", "Новое"
        USED = "used", "Б/У"
        SPARE = "spare", "Запасная часть"

    class Availability(models.TextChoices):
        AVAILABLE = "available", "В наличии"
        REQUEST = "request", "Под заказ"
        SOLD = "sold", "Продано"

    class Currency(models.TextChoices):
        KZT = "KZT", "₸ (KZT)"
        EUR = "EUR", "€ (EUR)"
        USD = "USD", "$ (USD)"

    title = models.CharField("Название", max_length=220)
    slug = models.SlugField("URL-имя", unique=True, max_length=180, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория"
    )
    status = models.CharField("Публикация", choices=Status.choices, default=Status.DRAFT, max_length=12)
    condition = models.CharField("Состояние", choices=Condition.choices, default=Condition.USED, max_length=8)
    availability = models.CharField(
        "Наличие", choices=Availability.choices, default=Availability.REQUEST, max_length=12
    )
    summary = models.CharField("Краткое описание", max_length=350, blank=True)
    description = models.TextField("Полное описание", blank=True)
    manufacturer = models.CharField("Производитель", max_length=120, blank=True)
    model_name = models.CharField("Модель", max_length=120, blank=True)
    production_year = models.PositiveSmallIntegerField("Год выпуска", null=True, blank=True)
    capacity_per_hour = models.PositiveIntegerField("Производительность (шт/час)", null=True, blank=True)
    container_type = models.CharField("Тип тары", max_length=150, blank=True)
    price = models.DecimalField(
        "Цена", max_digits=13, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField("Валюта", choices=Currency.choices, max_length=3, default=Currency.EUR)
    featured = models.BooleanField("На главной", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def save(self, *args, **kwargs):
        ensure_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    @property
    def cover_image(self):
        return next(iter(self.images.all()), None)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Товар")
    image = models.ImageField(
        "Фотография", upload_to="products/%Y/%m/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"]), validate_upload_size],
    )
    alt_text = models.CharField("Описание фото", max_length=200, blank=True)
    is_cover = models.BooleanField("Главная фотография", default=False)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ("-is_cover", "sort_order", "pk")
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Фото: {self.product}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications", verbose_name="Товар")
    name = models.CharField("Параметр", max_length=150)
    value = models.CharField("Значение", max_length=300)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ("sort_order", "pk")
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return f"{self.name}: {self.value}"


class ProductDocument(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="documents", verbose_name="Товар")
    title = models.CharField("Название документа", max_length=150)
    file = models.FileField(
        "PDF", upload_to="documents/%Y/%m/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"]), validate_upload_size],
    )

    class Meta:
        verbose_name = "PDF-документ"
        verbose_name_plural = "PDF-документы"

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.file and hasattr(self.file, "read"):
            position = self.file.tell()
            try:
                if self.file.read(5) != b"%PDF-":
                    raise ValidationError({"file": "Загрузите корректный PDF-файл."})
            finally:
                self.file.seek(position)


class Page(models.Model):
    slug = models.SlugField("URL-имя", unique=True, max_length=180)
    title = models.CharField("Заголовок", max_length=180)
    lead = models.TextField("Вступление", blank=True)
    body = models.TextField("Основной текст", blank=True)
    is_published = models.BooleanField("Опубликована", default=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        ordering = ("title",)
        verbose_name = "Информационная страница"
        verbose_name_plural = "Информационные страницы"

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    name = models.CharField("Имя", max_length=150)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=60, blank=True)
    company = models.CharField("Компания", max_length=180, blank=True)
    message = models.TextField("Сообщение")
    product = models.ForeignKey(
        Product, verbose_name="Интересующий товар", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="inquiries",
    )
    created_at = models.DateTimeField("Получена", auto_now_add=True)
    consent_at = models.DateTimeField("Согласие получено", default=timezone.now)
    email_sent = models.BooleanField("Отправлено на email", default=False)
    processed = models.BooleanField("Обработана", default=False)
    admin_note = models.TextField("Заметка менеджера", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} / {self.created_at:%d.%m.%Y}"


class PageTranslation(models.Model):
    language = models.CharField(
        "Язык", choices=[("kk", "Қазақша"), ("en", "English"), ("it", "Italiano")],
        max_length=2,
    )
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="translations")
    title = models.CharField("Заголовок", max_length=180, blank=True)
    lead = models.TextField("Вступление", blank=True)
    body = models.TextField("Основной текст", blank=True)

    class Meta:
        unique_together = ("page", "language")
        verbose_name = "Перевод страницы"
        verbose_name_plural = "Переводы страниц"

    def __str__(self):
        return f"{self.page} ({self.language})"


class ProductTranslation(models.Model):
    language = models.CharField(
        "Язык", choices=[("kk", "Қазақша"), ("en", "English"), ("it", "Italiano")],
        max_length=2,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="translations")
    title = models.CharField("Название", max_length=220, blank=True)
    summary = models.CharField("Краткое описание", max_length=350, blank=True)
    description = models.TextField("Полное описание", blank=True)

    class Meta:
        unique_together = ("product", "language")
        verbose_name = "Перевод товара"
        verbose_name_plural = "Переводы товаров"

    def __str__(self):
        return f"{self.product} ({self.language})"


class Partner(models.Model):
    name = models.CharField("Название", max_length=150)
    website = models.URLField("Сайт производителя", blank=True)
    logo = models.ImageField(
        "Логотип", upload_to="partners/", blank=True,
        validators=[validate_upload_size],
    )
    sort_order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "Партнёр / производитель"
        verbose_name_plural = "Наши партнёры"

    def __str__(self):
        return self.name
