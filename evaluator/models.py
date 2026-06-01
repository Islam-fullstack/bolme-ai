from django.db import models
from django.utils import timezone


class HarakatBaholash(models.Model):
    """Model for evaluating human movement continuity"""
    HARAKAT_TURLARI = [
        ("yugurish", "Yugurish"),
        ("yurish", "Yurish"),
        ("suzish", "Suzish"),
        ("velosiped", "Velosiped minish"),
        ("gimnastika", "Gimnastika"),
        ("boshqa", "Boshqa"),
    ]

    DARAJA_CHOICES = [
        ("boshlangich", "Boshlang'ich"),
        ("orta", "O'rta"),
        ("yuqori", "Yuqori"),
        ("professional", "Professional"),
    ]

    ism = models.CharField(max_length=100, verbose_name="Ism")
    familiya = models.CharField(max_length=100, verbose_name="Familiya")
    yosh = models.PositiveIntegerField(verbose_name="Yosh")
    harakat_turi = models.CharField(max_length=50, choices=HARAKAT_TURLARI, verbose_name="Harakat turi")
    daraja = models.CharField(max_length=50, choices=DARAJA_CHOICES, verbose_name="Daraja")
    davomiylik_daqiqa = models.FloatField(verbose_name="Davomiylik (daqiqa)")
    masofа_km = models.FloatField(verbose_name="Masofa (km)", default=0)
    yurak_urishi = models.PositiveIntegerField(verbose_name="Yurak urishi (urib/min)", default=0)
    izoh = models.TextField(blank=True, verbose_name="Izoh")
    ai_tahlil = models.TextField(blank=True, verbose_name="AI Tahlili")
    baho = models.FloatField(null=True, blank=True, verbose_name="Umumiy baho (0-100)")
    sana = models.DateTimeField(default=timezone.now, verbose_name="Sana")

    class Meta:
        verbose_name = "Harakat baholash"
        verbose_name_plural = "Harakat baholashlar"
        ordering = ["-sana"]

    def __str__(self):
        return f"{self.ism} {self.familiya} - {self.get_harakat_turi_display()} ({self.sana.strftime('%d.%m.%Y')})"


class StatistikaMa_lumot(models.Model):
    """Cached statistics"""
    kalit = models.CharField(max_length=100, unique=True)
    qiymat = models.JSONField()
    yangilangan = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Statistika"
