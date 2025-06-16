# dashboard/urls.py
from django.urls import path
from .views import HomeView, input_nilai, hasil_rekomendasi, lihat_bobot_kriteria


app_name = 'dashboard'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('input/', input_nilai, name='input_nilai'),
    path('hasil/', hasil_rekomendasi, name='hasil_rekomendasi'),
    path('hasil_ahp/', lihat_bobot_kriteria, name='hitung_ahp'),
]
