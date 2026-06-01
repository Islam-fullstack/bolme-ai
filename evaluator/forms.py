from django import forms
from .models import HarakatBaholash


class HarakatBaholashForm(forms.ModelForm):
    class Meta:
        model = HarakatBaholash
        fields = [
            "ism", "familiya", "yosh", "harakat_turi", "daraja",
            "davomiylik_daqiqa", "masofа_km", "yurak_urishi", "izoh"
        ]
        widgets = {
            "ism": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ismingizni kiriting"}),
            "familiya": forms.TextInput(attrs={"class": "form-input", "placeholder": "Familiyangizni kiriting"}),
            "yosh": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Yoshingiz", "min": 5, "max": 120}),
            "harakat_turi": forms.Select(attrs={"class": "form-select"}),
            "daraja": forms.Select(attrs={"class": "form-select"}),
            "davomiylik_daqiqa": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Masalan: 45", "min": 1, "step": "0.5"}),
            "masofа_km": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Masalan: 5.2", "min": 0, "step": "0.1"}),
            "yurak_urishi": forms.NumberInput(attrs={"class": "form-input", "placeholder": "Masalan: 140", "min": 40, "max": 250}),
            "izoh": forms.Textarea(attrs={"class": "form-textarea", "placeholder": "Qo'shimcha ma'lumotlar...", "rows": 4}),
        }
        labels = {
            "ism": "Ism",
            "familiya": "Familiya",
            "yosh": "Yosh",
            "harakat_turi": "Harakat turi",
            "daraja": "Daraja",
            "davomiylik_daqiqa": "Davomiylik (daqiqa)",
            "masofа_km": "Masofa (km)",
            "yurak_urishi": "Yurak urishi (urib/daqiqa)",
            "izoh": "Izoh",
        }
