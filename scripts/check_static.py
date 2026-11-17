#!/usr/bin/env python3
"""Sanity-check the generated public website without running Django."""
import argparse
import re
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="_site")
    args = p.parse_args()
    root = Path(args.output).resolve()
    assert (root / "index.html").is_file()
    assert (root / ".nojekyll").is_file()
    assert (root / "static" / "catalog" / "site.css").is_file()
    assert (root / "static" / "catalog" / "static_catalog.js").is_file()
    assert not (root / "admin").exists()
    assert not (root / "db.sqlite3").exists()
    assert not (root / "static" / "catalog" / "admin.css").exists()

    expected = {
        "ru": "Сейчас в продаже",
        "kk": "Қазір сатылымда",
        "en": "Available now",
    }
    for lang, label in expected.items():
        prefix = root / lang
        for folder in ("catalog", "contact", "privacy", "partners", "thanks"):
            assert (prefix / folder / "index.html").is_file(), (lang, folder)
        home = (prefix / "index.html").read_text(encoding="utf-8")
        catalog = (prefix / "catalog" / "index.html").read_text(encoding="utf-8")
        contact = (prefix / "contact" / "index.html").read_text(encoding="utf-8")
        assert f'lang="{lang}"' in home
        assert label in catalog
        assert "?lang=" not in home, "Language links must be static and crawlable"
        assert 'data-static-contact' in contact
        assert 'name="csrfmiddlewaretoken"' not in contact
        assert 'name="subject"' in contact
        assert 'name="_gotcha"' in contact
        assert 'href="/' not in home, "Public navigation must support repository paths"
        assert "data-category=" in catalog, "Catalog filters require product metadata"
        assert "formspree.io/f/" in contact or "disabled" in contact

    # Photo archive is uploaded separately. If it exists in the repository,
    # an accidental deployment without actual equipment photos must fail.
    repo_root = Path(__file__).resolve().parents[1]
    archive_exists = any((
        (repo_root / "Packaging_Systems_assets.zip").is_file(),
        (repo_root / "content" / "assets" / "Packaging_Systems_assets.zip").is_file(),
    ))
    if archive_exists:
        product_images = list((root / "media" / "products").rglob("*.webp"))
        partner_logos = list((root / "media" / "partners").rglob("*.webp"))
        assert len(product_images) >= 15, (
            f"Asset archive exists, but only {len(product_images)} product images exported"
        )
        assert len(partner_logos) >= 17, (
            f"Asset archive exists, but only {len(partner_logos)} partner logos exported"
        )
        catalog_en = (root / "en" / "catalog" / "index.html").read_text(encoding="utf-8")
        assert "/media/" not in catalog_en or "webp" in catalog_en
        print(f"Asset archive validated: {len(product_images)} product images, "
              f"{len(partner_logos)} partner logos.")
    else:
        print("Photos not in repository: upload Packaging_Systems_assets.zip once.")

    pages = list(root.rglob("index.html"))
    assert len(pages) >= 30, "Expected home, catalog, info pages and product in each language"
    for page in pages:
        text = page.read_text(encoding="utf-8")
        assert 'href="/admin/' not in text
        assert 'href="/admin-preview/' not in text
        assert not re.search(r'(?:href|src)="/(?:static|media)/', text)
        assert "DJANGO_SECRET_KEY" not in text

    print(f"Verified {len(pages)} static pages in {root}")

if __name__ == "__main__":
    main()
