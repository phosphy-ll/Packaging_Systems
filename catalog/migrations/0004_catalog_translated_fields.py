from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_remove_italian_add_subject"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="name_kk",
            field=models.CharField("Название (KZ)", max_length=120, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="category",
            name="name_en",
            field=models.CharField("Название (EN)", max_length=120, blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField("Название (RU)", max_length=120),
        ),
        migrations.AddField(
            model_name="productspecification",
            name="name_kk",
            field=models.CharField("Параметр (KZ)", max_length=150, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="productspecification",
            name="value_kk",
            field=models.CharField("Значение (KZ)", max_length=300, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="productspecification",
            name="name_en",
            field=models.CharField("Параметр (EN)", max_length=150, blank=True, default=""),
        ),
        migrations.AddField(
            model_name="productspecification",
            name="value_en",
            field=models.CharField("Значение (EN)", max_length=300, blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="productspecification",
            name="name",
            field=models.CharField("Параметр (RU)", max_length=150),
        ),
        migrations.AlterField(
            model_name="productspecification",
            name="value",
            field=models.CharField("Значение (RU)", max_length=300),
        ),
    ]
