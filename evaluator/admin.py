from django.contrib import admin
from .models import HarakatBaholash


@admin.register(HarakatBaholash)
class HarakatBaholashAdmin(admin.ModelAdmin):
    list_display = ["ism", "familiya", "yosh", "harakat_turi", "daraja", "davomiylik_daqiqa", "baho", "sana"]
    list_filter = ["harakat_turi", "daraja", "sana"]
    search_fields = ["ism", "familiya"]
    readonly_fields = ["ai_tahlil", "baho", "sana"]
    ordering = ["-sana"]
