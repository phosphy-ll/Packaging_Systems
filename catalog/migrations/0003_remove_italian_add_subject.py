from django.db import migrations, models


def remove_italian_data(apps, schema_editor):
    apps.get_model("catalog", "PageTranslation").objects.filter(language="it").delete()
    apps.get_model("catalog", "ProductTranslation").objects.filter(language="it").delete()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0002_translations_partners")]

    operations = [
        migrations.AddField(
            model_name="inquiry",
            name="subject",
            field=models.CharField("Тема обращения", max_length=180, blank=True, default=""),
        ),
        migrations.RunPython(remove_italian_data, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="pagetranslation",
            name="language",
            field=models.CharField(
                "Язык", choices=[("kk", "Қазақша"), ("en", "English")], max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="producttranslation",
            name="language",
            field=models.CharField(
                "Язык", choices=[("kk", "Қазақша"), ("en", "English")], max_length=2,
            ),
        ),
    ]
