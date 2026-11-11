from django import forms

from .models import Inquiry, Product
from .i18n import translate


class InquiryForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(), required=False,
        widget=forms.HiddenInput(), label="Товар",
    )
    consent = forms.BooleanField(
        label="Согласен(на) на обработку персональных данных для ответа на запрос",
        required=True,
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput(), label="")

    class Meta:
        model = Inquiry
        fields = ("name", "email", "phone", "company", "message", "product")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@company.kz", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 ...", "autocomplete": "tel"}),
            "company": forms.TextInput(attrs={"placeholder": "Название компании"}),
            "message": forms.Textarea(attrs={"placeholder": "Какое оборудование вас интересует?", "rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop("language", "ru")
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(status=Product.Status.PUBLISHED)
        self.fields["name"].required = True
        self.fields["email"].required = True
        self.fields["message"].required = True
        for field_name, source in {
            "name": "Имя", "email": "Email", "phone": "Телефон",
            "company": "Компания", "message": "Сообщение",
            "consent": "Согласен(на) на обработку персональных данных для ответа на мой запрос.",
        }.items():
            self.fields[field_name].label = translate(source, lang)
        placeholders = {
            "ru": ("Ваше имя", "Название компании", "Какое оборудование вас интересует?"),
            "kk": ("Атыңыз", "Компания атауы", "Қандай жабдық қызықтырады?"),
            "en": ("Your name", "Company name", "What equipment are you interested in?"),
            "it": ("Il tuo nome", "Nome azienda", "Quali attrezzature ti interessano?"),
        }
        name, company, message = placeholders.get(lang, placeholders["ru"])
        self.fields["name"].widget.attrs["placeholder"] = name
        self.fields["company"].widget.attrs["placeholder"] = company
        self.fields["message"].widget.attrs["placeholder"] = message

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Не удалось отправить форму.")
        return value
