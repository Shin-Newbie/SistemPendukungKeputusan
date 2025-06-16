# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home/', views.dashboard_home, name='home'),
    path('input/', views.input_nilai, name='input_nilai'),
    path('hasil/', views.hasil_rekomendasi, name='hasil_rekomendasi'),
    path('hasil_ahp/', views.lihat_bobot_kriteria, name='hitung_ahp'),
]
