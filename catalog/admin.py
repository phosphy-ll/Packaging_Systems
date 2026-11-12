from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category, Inquiry, Page, Product, ProductDocument, ProductImage, ProductSpecification, PageTranslation, ProductTranslation, Partner,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    class Media:
        js = ("catalog/admin_photos.js",)

    model = ProductImage
    extra = 1
    fields = ("image", "preview", "alt_text", "is_cover", "sort_order")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" width="96" style="height:64px;object-fit:contain"/>', obj.image.url)
        return "—"
    preview.short_description = "Просмотр"


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 2


class ProductDocumentInline(admin.TabularInline):
    model = ProductDocument
    extra = 0


class ProductTranslationInline(admin.StackedInline):
    model = ProductTranslation
    extra = 0
    max_num = 2
    fields = ("language", "title", "summary", "description")
    verbose_name = "Перевод товара"
    verbose_name_plural = "Переводы товара: қазақша / English"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title", "category", "status", "availability", "condition",
        "price", "currency", "featured", "updated_at",
    )
    list_editable = ("status", "availability", "featured")
    list_filter = ("status", "availability", "condition", "category", "featured")
    search_fields = ("title", "manufacturer", "model_name", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25
    inlines = [ProductImageInline, ProductSpecificationInline, ProductDocumentInline, ProductTranslationInline]
    change_form_template = "admin/catalog/product/change_form.html"
    fieldsets = (
        ("Публикация", {"fields": ("title", "slug", "category", "status", "availability", "condition", "featured")}),
        ("Описание", {"fields": ("summary", "description")}),
        ("Технические параметры", {"fields": ("manufacturer", "model_name", "production_year", "capacity_per_hour", "container_type")}),
        ("Цена", {"fields": ("price", "currency")}),
        ("Служебная информация", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


class PageTranslationInline(admin.StackedInline):
    model = PageTranslation
    extra = 0
    max_num = 2
    verbose_name_plural = "Переводы страницы"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    list_editable = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageTranslationInline]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "product", "created_at", "email_sent", "processed")
    list_filter = ("processed", "email_sent", "created_at")
    search_fields = ("name", "subject", "email", "company", "message")
    readonly_fields = (
        "name", "subject", "email", "phone", "company", "message", "product",
        "created_at", "consent_at", "email_sent",
    )
    fields = (
        "name", "subject", "email", "phone", "company", "message", "product",
        "created_at", "consent_at", "email_sent", "processed", "admin_note",
    )
    actions = ("mark_processed",)

    @admin.action(description="Отметить выбранные как обработанные")
    def mark_processed(self, request, queryset):
        queryset.update(processed=True)

    def has_add_permission(self, request):
        return False


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "logo_preview", "website", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name",)
    readonly_fields = ("logo_preview",)
    fields = ("name", "website", "logo", "logo_preview", "sort_order", "is_active")

    @admin.display(description="Логотип")
    def logo_preview(self, obj):
        if obj.pk and obj.logo:
            return format_html(
                '<img src="{}" alt="" style="width:120px;height:65px;object-fit:contain">',
                obj.logo.url,
            )
        return "Добавьте логотип"
