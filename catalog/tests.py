from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, Inquiry, Page, Product


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Линии розлива", slug="filling-lines")
        cls.published = Product.objects.create(
            title="Тестовая линия", category=cls.category,
            status=Product.Status.PUBLISHED, availability=Product.Availability.AVAILABLE,
            manufacturer="Test", price=10000,
        )
        cls.draft = Product.objects.create(
            title="Секретный черновик", category=cls.category, status=Product.Status.DRAFT,
        )

    def test_home_and_catalog_load(self):
        self.assertEqual(self.client.get(reverse("catalog:home")).status_code, 200)
        response = self.client.get(reverse("catalog:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовая линия")
        self.assertNotContains(response, "Секретный черновик")

    def test_draft_is_not_public(self):
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(self.published.get_absolute_url()).status_code, 200)

    def test_filter_and_search(self):
        response = self.client.get(reverse("catalog:product_list"), {"q": "Test", "condition": "used"})
        self.assertContains(response, "Тестовая линия")
        response = self.client.get(reverse("catalog:product_list"), {"q": "unrelated"})
        self.assertNotContains(response, "Тестовая линия")

    def test_auto_slug_is_generated(self):
        self.assertTrue(self.published.slug)
        self.assertTrue(self.draft.slug)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_contact_saves_and_sends_email(self):
        response = self.client.post(reverse("catalog:contact"), {
            "name": "Тест", "email": "test@example.com", "phone": "+77770000000",
            "company": "Test Co", "message": "Прошу информацию",
            "product": str(self.published.pk), "consent": "on", "website": "",
        })
        self.assertRedirects(response, reverse("catalog:thanks"))
        inquiry = Inquiry.objects.get()
        self.assertEqual(inquiry.product, self.published)
        self.assertTrue(inquiry.email_sent)
        self.assertEqual(len(mail.outbox), 1)

    def test_consent_is_required(self):
        response = self.client.post(reverse("catalog:contact"), {
            "name": "Тест", "email": "test@example.com", "message": "Вопрос", "website": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_honeypot(self):
        response = self.client.post(reverse("catalog:contact"), {
            "name": "Бот", "email": "bot@example.com", "message": "Спам",
            "consent": "on", "website": "https://spam.invalid",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_content_seed_is_idempotent(self):
        call_command("seed_content")
        count = Page.objects.count()
        call_command("seed_content")
        self.assertEqual(Page.objects.count(), count)
        self.assertTrue(Page.objects.filter(slug="service").exists())
        self.assertEqual(Product.objects.filter(title="Линия розлива Bertolaso 40.40.6").count(), 1)
        product = Product.objects.get(title="Линия розлива Bertolaso 40.40.6")
        self.assertEqual(product.status, Product.Status.PUBLISHED)



class UpgradeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_content")

    def test_four_languages_switch_and_session(self):
        url=reverse("catalog:home")
        for lang in ("ru", "kk", "en", "it"):
            response=self.client.get(url, {"lang":lang})
            self.assertEqual(response.status_code,200)
            self.assertContains(response, f'lang="{lang}"')
        response=self.client.get(url)
        self.assertContains(response, "Impianti di")

    def test_partner_page(self):
        response=self.client.get(reverse("catalog:partners"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"SIPA")

    def test_preview_staff_only(self):
        from django.contrib.auth import get_user_model
        product=Product.objects.get(title="Линия розлива Bertolaso 40.40.6")
        product.status=Product.Status.DRAFT
        product.save(update_fields=["status"])
        url=reverse("catalog:preview_product",kwargs={"pk":product.pk})
        self.assertEqual(self.client.get(url).status_code,302)
        self.assertEqual(self.client.get(product.get_absolute_url()).status_code,404)
        user=get_user_model().objects.create_user(username="previewer",password="test1234",is_staff=True)
        self.client.force_login(user)
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Предпросмотр товара")

    def test_translations_exist_for_seeded_products_and_pages(self):
        from .models import PageTranslation, ProductTranslation, Partner
        self.assertEqual(PageTranslation.objects.filter(page__slug="service").count(),3)
        self.assertEqual(ProductTranslation.objects.filter(product__title="Линия розлива Bertolaso 40.40.6").count(),3)
        self.assertGreaterEqual(Partner.objects.count(),16)
