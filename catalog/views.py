import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import InquiryForm
from .models import Category, Page, Product

logger = logging.getLogger(__name__)


def visible_products():
    return (
        Product.objects.filter(status=Product.Status.PUBLISHED, category__is_active=True)
        .exclude(availability=Product.Availability.SOLD)
        .select_related("category")
        .prefetch_related("images")
    )


def home(request):
    home_page = Page.objects.filter(slug="home", is_published=True).first()
    featured = list(
        visible_products().filter(featured=True).exclude(
            availability=Product.Availability.SOLD
        )[:3]
    )
    if len(featured) < 3:
        seen = [p.pk for p in featured]
        featured.extend(
            visible_products().exclude(pk__in=seen).exclude(
                availability=Product.Availability.SOLD
            )[:3 - len(featured)]
        )
    return render(request, "catalog/home.html", {
        "home_page": home_page,
        "featured": featured,
        "categories": Category.objects.filter(is_active=True)[:5],
        "page_title": "Packaging Systems | Оборудование для розлива",
    })


def product_list(request):
    products = visible_products()
    query = request.GET.get("q", "").strip()[:120]
    category = request.GET.get("category", "")
    condition = request.GET.get("condition", "")
    sort = request.GET.get("sort", "newest")
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(manufacturer__icontains=query)
            | Q(model_name__icontains=query)
            | Q(description__icontains=query)
        )
    if category:
        products = products.filter(category__slug=category)
    if condition in Product.Condition.values:
        products = products.filter(condition=condition)
    sort_by = {"newest": "-created_at", "price_low": "price", "price_high": "-price"}
    products = products.order_by(sort_by.get(sort, "-created_at"))
    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "catalog/product_list.html", {
        "page_obj": page_obj,
        "categories": Category.objects.filter(is_active=True),
        "query": query,
        "selected_category": category,
        "selected_condition": condition,
        "selected_sort": sort,
        "search_params": params.urlencode(),
        "page_title": "Сейчас в продаже | Packaging Systems",
    })


def product_detail(request, slug):
    product = get_object_or_404(
        visible_products().prefetch_related("specifications", "documents"),
        slug=slug,
    )
    return render(request, "catalog/product_detail.html", {
        "product": product,
        "page_title": f"{product.title} | Packaging Systems",
    })


def info_page(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, "catalog/info_page.html", {
        "page": page, "page_title": f"{page.title} | Packaging Systems",
    })


@require_http_methods(["GET", "POST"])
def contact(request):
    initial = {}
    if request.method == "GET":
        product = visible_products().filter(slug=request.GET.get("product", "")).first()
        if product:
            initial["product"] = product.pk
    form = InquiryForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        inquiry = form.save()
        product_title = inquiry.product.title if inquiry.product else "Без привязки к товару"
        body = (
            f"Новая заявка с сайта Packaging Systems\n\n"
            f"Имя: {inquiry.name}\n"
            f"Email: {inquiry.email}\n"
            f"Телефон: {inquiry.phone or 'Не указан'}\n"
            f"Компания: {inquiry.company or 'Не указана'}\n"
            f"Оборудование: {product_title}\n\n"
            f"Сообщение:\n{inquiry.message}\n"
        )
        try:
            if not settings.EMAIL_HOST and not settings.DEBUG and settings.EMAIL_BACKEND != "django.core.mail.backends.locmem.EmailBackend":
                return redirect("catalog:thanks")
            sent = EmailMessage(
                subject="Packaging Systems: новая заявка",
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.COMPANY_EMAIL],
                reply_to=[inquiry.email],
            ).send(fail_silently=False)
            if sent:
                inquiry.email_sent = True
                inquiry.save(update_fields=["email_sent"])
        except Exception:
            logger.exception("Failed to email inquiry %s; stored in database", inquiry.pk)
        return redirect("catalog:thanks")
    return render(request, "catalog/contact.html", {
        "form": form,
        "page_title": "Обратная связь | Packaging Systems",
    })


def thanks(request):
    return render(request, "catalog/thanks.html", {
        "page_title": "Заявка получена | Packaging Systems",
    })


def privacy(request):
    return render(request, "catalog/privacy.html", {
        "page_title": "Обработка персональных данных | Packaging Systems",
    })
