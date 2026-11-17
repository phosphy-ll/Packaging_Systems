"""Import approved equipment photographs and producer logos from ZIP asset pack.

Usage: python manage.py import_assets --zip Packaging_Systems_assets.zip
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, BadZipFile

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from PIL import Image, UnidentifiedImageError

from catalog.models import Partner, Product, ProductImage
from catalog.seed_extra import PARTNERS


class Command(BaseCommand):
    help = "Импорт фотографий линии и логотипов из ZIP; безопасно повторять."

    def add_arguments(self, parser):
        parser.add_argument("--zip", dest="zip_path", required=True, help="Путь к архиву Packaging_Systems_assets.zip")

    def handle(self, *args, **options):
        archive=Path(options["zip_path"]).expanduser()
        if not archive.is_file():
            raise CommandError(f"Архив не найден: {archive}")
        product=Product.objects.filter(title="Линия розлива Bertolaso 40.40.6").first()
        if not product:
            raise CommandError("Сначала выполните python manage.py seed_content")
        added=0
        try:
            with ZipFile(archive) as z:
                for i in range(1,16):
                    name=f"equipment/equipment_{i:02d}.webp"
                    if name not in z.namelist():
                        continue
                    if z.getinfo(name).file_size > 20*1024*1024:
                        raise CommandError(f"Слишком большой файл: {name}")
                    alt=f"Импорт из презентации: фото {i}"
                    if ProductImage.objects.filter(product=product,alt_text=alt).exists():
                        continue
                    raw=z.read(name)
                    try:
                        with Image.open(BytesIO(raw)) as picture:
                            picture.verify()
                    except (UnidentifiedImageError, OSError) as e:
                        raise CommandError(f"Некорректное изображение {name}: {e}")
                    image=ProductImage(product=product,alt_text=alt,sort_order=i,is_cover=(i==1))
                    image.image.save(f"bertolaso_{i:02d}.webp",ContentFile(raw),save=True)
                    added+=1
                for i,company in enumerate(PARTNERS,1):
                    path=f"partners/partner_{i:02d}.webp"
                    if path not in z.namelist():
                        continue
                    if z.getinfo(path).file_size > 20*1024*1024:
                        raise CommandError(f"Слишком большой файл: {path}")
                    partner=Partner.objects.get(name=company)
                    if partner.logo:
                        continue
                    raw=z.read(path)
                    try:
                        with Image.open(BytesIO(raw)) as picture:
                            picture.verify()
                    except (UnidentifiedImageError,OSError) as e:
                        raise CommandError(f"Некорректное изображение {path}: {e}")
                    partner.logo.save(f"partner_{i:02d}.webp",ContentFile(raw),save=True)
        except BadZipFile:
            raise CommandError("Это не ZIP-архив")
        self.stdout.write(self.style.SUCCESS(f"Импорт завершён. Добавлено фотографий: {added}. Логотипы партнёров обновлены."))
