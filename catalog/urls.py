from django.urls import path

from . import views

app_name = "catalog"
urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.product_list, name="product_list"),
    path("catalog/<slug:slug>/", views.product_detail, name="product_detail"),
    path("directions/<slug:slug>/", views.info_page, name="page"),
    path("contact/", views.contact, name="contact"),
    path("thanks/", views.thanks, name="thanks"),
    path("privacy/", views.privacy, name="privacy"),
]
