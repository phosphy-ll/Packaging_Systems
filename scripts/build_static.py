#!/usr/bin/env python3
"""Build static RU/KZ/EN site from existing Django views, without publishing Django.

Run: python scripts/build_static.py --output _site
The database is temporary and deleted after rendering. The public artifact
contains HTML/CSS/JS and explicitly selected media only, never the admin or DB.
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("ru", "kk", "en")
SAFE_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_ATTR = re.compile(r'(?P<attr>\b(?:href|src|action))=(?P<q>["\'])(?P<url>[^"\']*)(?P=q)')
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
PDF_SUFFIXES = {".pdf"}
MAX_FILE_SIZE = 20 * 1024 * 1024


def fail(message):
    raise ValueError(message)


def public_input_path(filename, allowed_suffixes):
    """Only allow repository content/images and content/documents, never traversal."""
    if not isinstance(filename, str) or not filename:
        fail("Image/document path must be a nonempty string")
    allowed_roots = [ROOT / "content" / "images", ROOT / "content" / "documents"]
    path = (ROOT / filename).resolve()
    if not any(path.is_relative_to(root.resolve()) for root in allowed_roots):
        fail(f"File must be under content/images or content/documents: {filename}")
    if path.suffix.lower() not in allowed_suffixes:
        fail(f"Unsupported file extension: {filename}")
    if not path.is_file():
        fail(f"Missing content file: {filename}")
    if path.stat().st_size > MAX_FILE_SIZE:
        fail(f"File is larger than 20 MB: {filename}")
    return path


def load_catalog():
    path = ROOT / "content" / "catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("products")
    if not isinstance(items, list):
        fail("content/catalog.json must contain a products array")
    seen = set()
    for item in items:
        if not isinstance(item, dict) or not SAFE_SLUG.fullmatch(str(item.get("slug", ""))):
            fail(f"Invalid product slug: {item}")
        slug = item["slug"]
        if slug in seen:
            fail(f"Duplicate product slug: {slug}")
        seen.add(slug)
    return items


def apply_products(items):
    from django.core.files.base import ContentFile
    from PIL import Image
    from catalog.models import Category, Product, ProductDocument, ProductImage, ProductSpecification, ProductTranslation

    slugs = [item["slug"] for item in items]
    # Seed data is the initial content source, not an automatically published listing.
    # Only items explicitly present in catalog.json may be included in the build.
    Product.objects.exclude(slug__in=slugs).delete()

    for entry in items:
        slug = entry["slug"]
        seeded = entry.get("source") == "seed"
        item = Product.objects.filter(slug=slug).first()
        if seeded and item is None:
            fail(f"Seed product not found: {slug}")
        if item is None:
            required = ("title", "category")
            for field in required:
                if not isinstance(entry.get(field), str) or not entry[field]:
                    fail(f"{slug}: required field {field} is missing")
            cat = Category.objects.filter(slug=entry["category"]).first()
            if not cat:
                fail(f"{slug}: unknown category {entry['category']}")
            item = Product(slug=slug, title=entry["title"], category=cat)

        if "category" in entry:
            cat = Category.objects.filter(slug=entry["category"]).first()
            if not cat:
                fail(f"{slug}: unknown category {entry['category']}")
            item.category = cat

        simple_fields = (
            "title", "summary", "description", "manufacturer", "model_name",
            "container_type", "condition", "availability", "currency"
        )
        for field in simple_fields:
            if field in entry:
                setattr(item, field, entry[field])
        for field in ("production_year", "capacity_per_hour"):
            if field in entry:
                setattr(item, field, entry[field])
        if "price" in entry:
            item.price = Decimal(str(entry["price"])) if entry["price"] is not None else None
        if "featured" in entry:
            item.featured = bool(entry["featured"])
        item.status = entry.get("status", "draft")
        if item.status not in Product.Status.values:
            fail(f"{slug}: invalid status {item.status}")
        if item.condition not in Product.Condition.values or item.availability not in Product.Availability.values:
            fail(f"{slug}: invalid condition/availability")
        if item.currency not in Product.Currency.values:
            fail(f"{slug}: invalid currency")
        item.full_clean()
        item.save()

        if "translations" in entry:
            if not isinstance(entry["translations"], dict):
                fail(f"{slug}: translations must be a dictionary")
            for language, fields in entry["translations"].items():
                if language not in ("kk", "en") or not isinstance(fields, dict):
                    fail(f"{slug}: only kk/en translations are supported")
                allowed = {"title", "summary", "description"}
                if set(fields) - allowed:
                    fail(f"{slug}: unknown translation fields")
                translated, _ = ProductTranslation.objects.get_or_create(product=item, language=language)
                for key in allowed:
                    if key in fields:
                        setattr(translated, key, fields[key])
                translated.full_clean()
                translated.save()

        if "specifications" in entry:
            if not isinstance(entry["specifications"], list):
                fail(f"{slug}: specifications must be a list")
            item.specifications.all().delete()
            for index, spec in enumerate(entry["specifications"]):
                if not isinstance(spec, dict):
                    fail(f"{slug}: specification must be an object")
                fields = {k: spec.get(k, "") for k in (
                    "name", "value", "name_kk", "value_kk", "name_en", "value_en"
                )}
                s = ProductSpecification(product=item, sort_order=index, **fields)
                s.full_clean()
                s.save()

        if "images" in entry:
            if not isinstance(entry["images"], list):
                fail(f"{slug}: images must be a list")
            if entry.get("images_from_archive") and entry["images"]:
                fail(f"{slug}: use either images_from_archive or images, not both")
            item.images.all().delete()
            for number, filename in enumerate(entry["images"], 1):
                path = public_input_path(filename, IMAGE_SUFFIXES)
                with Image.open(path) as img:
                    img.verify()
                new = ProductImage(
                    product=item, sort_order=number, is_cover=(number == 1),
                    alt_text=f"{item.title}: photo {number}",
                )
                new.image.save(
                    f"{slug}-{number}{path.suffix.lower()}",
                    ContentFile(path.read_bytes()), save=True,
                )

        if "documents" in entry:
            if not isinstance(entry["documents"], list):
                fail(f"{slug}: documents must be a list")
            item.documents.all().delete()
            for number, document in enumerate(entry["documents"], 1):
                if not isinstance(document, dict):
                    fail(f"{slug}: documents entries must be objects")
                path = public_input_path(document.get("file"), PDF_SUFFIXES)
                if not path.read_bytes().startswith(b"%PDF-"):
                    fail(f"{slug}: invalid PDF: {path}")
                doc = ProductDocument(product=item, title=document.get("title", path.name))
                doc.file.save(
                    f"{slug}-document-{number}.pdf",
                    ContentFile(path.read_bytes()), save=True,
                )


def make_routes():
    from catalog.models import Page, Product
    routes = [
        "/", "/catalog/", "/partners/", "/contact/", "/privacy/", "/thanks/",
    ]
    routes += [f"/directions/{p.slug}/" for p in Page.objects.filter(is_published=True).exclude(slug="home")]
    routes += [p.get_absolute_url() for p in Product.objects.filter(
        status="published", category__is_active=True
    ).exclude(availability="sold")]
    return sorted(set(routes))


def rel_root(route):
    # e.g. /catalog/item/ => en/catalog/item/index.html => ../../../
    levels = 1 + len([part for part in route.strip("/").split("/") if part])
    return "../" * levels


def rewrite_urls(html, route, lang):
    """Relative links work on both project Pages (/Packaging_Systems/) and a real domain."""
    root = rel_root(route)

    def transform(match):
        url = match.group("url")
        if url.startswith("?lang=") and url[6:] in LANGUAGES:
            result = root + url[6:] + route.lstrip("/")
        elif url.startswith("/") and not url.startswith("//"):
            parts = urlsplit(url)
            if parts.path.startswith(("/static/", "/media/")):
                result = root + parts.path.lstrip("/")
            elif parts.path.startswith("/admin/") or parts.path.startswith("/admin-preview/"):
                raise ValueError("Admin link in a public static page")
            else:
                result = root + lang + parts.path
            if parts.query:
                result += "?" + parts.query
            if parts.fragment:
                result += "#" + parts.fragment
        else:
            result = url
        return f"{match.group('attr')}={match.group('q')}{result}{match.group('q')}"

    return LINK_ATTR.sub(transform, html)


def copy_public_media(out):
    """Only export media referenced by currently published products and active partners."""
    from django.conf import settings
    from catalog.models import Partner, Product

    media = Path(settings.MEDIA_ROOT).resolve()
    names = set()
    for product in Product.objects.filter(
        status="published", category__is_active=True
    ).exclude(availability="sold"):
        names.update(photo.image.name for photo in product.images.all() if photo.image)
        names.update(document.file.name for document in product.documents.all() if document.file)
    for partner in Partner.objects.filter(is_active=True):
        if partner.logo:
            names.add(partner.logo.name)

    for name in names:
        source = (media / name).resolve()
        if not source.is_relative_to(media) or not source.is_file():
            fail(f"Invalid or missing public media file: {name}")
        target = out / "media" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="_site", help="Generated static output directory")
    args = parser.parse_args()
    out = (ROOT / args.output).resolve()
    if out == ROOT or ROOT not in out.parents:
        fail("Choose a dedicated output directory, e.g. _site, not the project root")
    items = load_catalog()

    with tempfile.TemporaryDirectory(prefix="packaging-build-") as workspace:
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
        os.environ["DATABASE_URL"] = "sqlite:///" + str(Path(workspace) / "export.sqlite3")
        os.environ["DJANGO_DEBUG"] = "1"
        os.environ["DJANGO_SECRET_KEY"] = "static-build-only-never-published"
        os.environ["ALLOWED_HOSTS"] = "testserver,localhost"
        os.environ["STATIC_EXPORT"] = "1"
        os.environ["DJANGO_SECURE_SSL_REDIRECT"] = "0"
        sys.path.insert(0, str(ROOT))

        import django
        django.setup()
        from django.conf import settings
        from django.core.management import call_command
        from django.test import Client

        settings.MEDIA_ROOT = Path(workspace) / "media"
        settings.MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
        call_command("migrate", interactive=False, verbosity=0)
        call_command("seed_content", verbosity=0)
        asset_pack = ROOT / "content" / "assets" / "Packaging_Systems_assets.zip"
        if not asset_pack.exists():
            asset_pack = ROOT / "Packaging_Systems_assets.zip"
        if asset_pack.exists():
            call_command("import_assets", zip_path=str(asset_pack), verbosity=0)
        else:
            print("WARNING: photo archive not uploaded; the first product will show placeholders.")
        apply_products(items)
        routes = make_routes()

        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        shutil.copytree(
            ROOT / "catalog" / "static", out / "static",
            ignore=shutil.ignore_patterns("admin.css", "admin_photos.js"),
        )
        copy_public_media(out)

        client = Client()
        count = 0
        for lang in LANGUAGES:
            for route in routes:
                response = client.get(route, {"lang": lang})
                if response.status_code != 200:
                    fail(f"Failed to render {lang} {route}: HTTP {response.status_code}")
                html = rewrite_urls(response.content.decode("utf-8"), route, lang)
                dest = out / lang / route.strip("/") / "index.html"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(html, encoding="utf-8")
                count += 1

        (out / "index.html").write_text(
            '<!doctype html><html lang="ru"><meta charset="utf-8">'
            '<meta name="robots" content="noindex">'
            '<meta http-equiv="refresh" content="0;url=ru/">'
            '<title>Packaging Systems</title><a href="ru/">Открыть сайт</a></html>',
            encoding="utf-8",
        )
        (out / "404.html").write_text(
            '<!doctype html><html lang="ru"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>404 | Packaging Systems</title>'
            '<main style="font-family:Arial,sans-serif;max-width:650px;margin:15vh auto">'
            '<h1>Страница не найдена</h1><p><a href="./ru/">Вернуться на главную</a></p></main>',
            encoding="utf-8",
        )
        (out / ".nojekyll").write_text("", encoding="utf-8")
        print(f"Built {count} static pages ({len(routes)} routes x {len(LANGUAGES)} languages) in {out}")
        print(f"Images/documents published: {sum(1 for p in (out / 'media').rglob('*') if p.is_file()) if (out / 'media').exists() else 0}")


if __name__ == "__main__":
    main()
