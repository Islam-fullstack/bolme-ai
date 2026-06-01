from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Count, Max, Min
from django.http import JsonResponse
from .models import HarakatBaholash
from .forms import HarakatBaholashForm
from .services import ai_tahlil_qil


def bosh_sahifa(request):
    so_nggi = HarakatBaholash.objects.all()[:6]
    statistika = {
        "jami": HarakatBaholash.objects.count(),
        "o_rtacha_baho": HarakatBaholash.objects.aggregate(Avg("baho"))["baho__avg"] or 0,
        "o_rtacha_davomiylik": HarakatBaholash.objects.aggregate(Avg("davomiylik_daqiqa"))["davomiylik_daqiqa__avg"] or 0,
        "eng_yaxshi_baho": HarakatBaholash.objects.aggregate(Max("baho"))["baho__max"] or 0,
    }
    return render(request, "evaluator/bosh_sahifa.html", {
        "so_nggi": so_nggi,
        "statistika": statistika,
    })


def baholash_qoshish(request):
    if request.method == "POST":
        form = HarakatBaholashForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            ma_lumot = {
                "ism": obj.ism,
                "familiya": obj.familiya,
                "yosh": obj.yosh,
                "harakat_turi": obj.get_harakat_turi_display(),
                "daraja": obj.get_daraja_display(),
                "davomiylik_daqiqa": obj.davomiylik_daqiqa,
                "masofa_km": obj.masofа_km,
                "yurak_urishi": obj.yurak_urishi,
                "izoh": obj.izoh,
            }
            tahlil, baho = ai_tahlil_qil(ma_lumot)
            obj.ai_tahlil = tahlil
            obj.baho = baho
            obj.save()
            messages.success(request, "Baholash muvaffaqiyatli saqlandi!")
            return redirect("natija_korinishi", pk=obj.pk)
        else:
            messages.error(request, "Iltimos, barcha maydonlarni to'g'ri to'ldiring.")
    else:
        form = HarakatBaholashForm()
    return render(request, "evaluator/baholash_form.html", {"form": form})


def natija_korinishi(request, pk):
    obj = get_object_or_404(HarakatBaholash, pk=pk)
    return render(request, "evaluator/natija.html", {"obj": obj})


def natijalar_royxati(request):
    harakat_turi = request.GET.get("tur", "")
    daraja = request.GET.get("daraja", "")
    qs = HarakatBaholash.objects.all()
    if harakat_turi:
        qs = qs.filter(harakat_turi=harakat_turi)
    if daraja:
        qs = qs.filter(daraja=daraja)
    harakat_turlari = HarakatBaholash.HARAKAT_TURLARI
    darajalar = HarakatBaholash.DARAJA_CHOICES
    return render(request, "evaluator/royxat.html", {
        "natijalar": qs,
        "harakat_turlari": harakat_turlari,
        "darajalar": darajalar,
        "joriy_tur": harakat_turi,
        "joriy_daraja": daraja,
    })


def statistika(request):
    harakat_turlari_stats = (
        HarakatBaholash.objects.values("harakat_turi")
        .annotate(soni=Count("id"), o_rtacha=Avg("baho"), davomiylik=Avg("davomiylik_daqiqa"))
        .order_by("-soni")
    )
    darajalar_stats = (
        HarakatBaholash.objects.values("daraja")
        .annotate(soni=Count("id"), o_rtacha=Avg("baho"))
        .order_by("-o_rtacha")
    )
    umumiy = {
        "jami": HarakatBaholash.objects.count(),
        "o_rtacha_baho": HarakatBaholash.objects.aggregate(Avg("baho"))["baho__avg"] or 0,
        "max_baho": HarakatBaholash.objects.aggregate(Max("baho"))["baho__max"] or 0,
        "min_baho": HarakatBaholash.objects.aggregate(Min("baho"))["baho__min"] or 0,
        "o_rtacha_davomiylik": HarakatBaholash.objects.aggregate(Avg("davomiylik_daqiqa"))["davomiylik_daqiqa__avg"] or 0,
        "o_rtacha_masofa": HarakatBaholash.objects.aggregate(Avg("masofа_km"))["masofа_km__avg"] or 0,
    }
    return render(request, "evaluator/statistika.html", {
        "harakat_turlari_stats": harakat_turlari_stats,
        "darajalar_stats": darajalar_stats,
        "umumiy": umumiy,
    })


def api_statistika(request):
    """JSON API for charts"""
    harakat_turlari_stats = list(
        HarakatBaholash.objects.values("harakat_turi")
        .annotate(soni=Count("id"), o_rtacha=Avg("baho"))
        .order_by("-soni")
    )
    so_nggi_7 = list(
        HarakatBaholash.objects.order_by("-sana")[:7]
        .values("ism", "baho", "harakat_turi", "davomiylik_daqiqa")
    )
    return JsonResponse({
        "harakat_turlari": harakat_turlari_stats,
        "so_nggi_7": so_nggi_7,
    })
