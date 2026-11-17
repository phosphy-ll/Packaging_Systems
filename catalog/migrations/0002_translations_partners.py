from django.db import migrations, models
import django.db.models.deletion
import catalog.models


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Partner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Название")),
                ("website", models.URLField(blank=True, verbose_name="Сайт производителя")),
                ("logo", models.ImageField(blank=True, upload_to="partners/", validators=[catalog.models.validate_upload_size], verbose_name="Логотип")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать на сайте")),
            ],
            options={"verbose_name": "Партнёр / производитель", "verbose_name_plural": "Наши партнёры", "ordering": ("sort_order", "name")},
        ),
        migrations.CreateModel(
            name="PageTranslation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(choices=[("kk", "Қазақша"), ("en", "English"), ("it", "Italiano")], max_length=2, verbose_name="Язык")),
                ("title", models.CharField(blank=True, max_length=180, verbose_name="Заголовок")),
                ("lead", models.TextField(blank=True, verbose_name="Вступление")),
                ("body", models.TextField(blank=True, verbose_name="Основной текст")),
                ("page", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="translations", to="catalog.page")),
            ],
            options={"verbose_name": "Перевод страницы", "verbose_name_plural": "Переводы страниц", "unique_together": {("page", "language")}},
        ),
        migrations.CreateModel(
            name="ProductTranslation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(choices=[("kk", "Қазақша"), ("en", "English"), ("it", "Italiano")], max_length=2, verbose_name="Язык")),
                ("title", models.CharField(blank=True, max_length=220, verbose_name="Название")),
                ("summary", models.CharField(blank=True, max_length=350, verbose_name="Краткое описание")),
                ("description", models.TextField(blank=True, verbose_name="Полное описание")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="translations", to="catalog.product")),
            ],
            options={"verbose_name": "Перевод товара", "verbose_name_plural": "Переводы товаров", "unique_together": {("product", "language")}},
        ),
    ]
