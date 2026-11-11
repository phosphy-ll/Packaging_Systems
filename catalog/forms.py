from django import forms

from .models import Inquiry, Product


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
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(status=Product.Status.PUBLISHED)
        self.fields["name"].required = True
        self.fields["email"].required = True
        self.fields["message"].required = True

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Не удалось отправить форму.")
        return value
