from django.urls import path
from . import views

urlpatterns = [
    path("", views.bosh_sahifa, name="bosh_sahifa"),
    path("baholash/", views.baholash_qoshish, name="baholash_qoshish"),
    path("natija/<int:pk>/", views.natija_korinishi, name="natija_korinishi"),
    path("natijalar/", views.natijalar_royxati, name="natijalar_royxati"),
    path("statistika/", views.statistika, name="statistika"),
    path("api/statistika/", views.api_statistika, name="api_statistika"),
]
