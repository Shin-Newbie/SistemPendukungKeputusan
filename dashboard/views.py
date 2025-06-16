from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Kriteria, Jurusan, PreferensiJurusan, InputSiswa
from .ahp_logic import AHPProcessor
from .forms import InputNilaiForm # <- Pastikan impor ini benar
from django.views.decorators.cache import never_cache
from account.models import CustomUser
from django.contrib import messages

@login_required
@never_cache
def dashboard_home(request):
    """
    Menampilkan halaman dashboard utama.
    """
    total_kriteria = Kriteria.objects.count()
    total_jurusan = Jurusan.objects.count()
    total_preferensi = PreferensiJurusan.objects.count()
    total_pengguna = CustomUser.objects.filter(jenis_user=CustomUser.JenisUser.SISWA).count()

    context = {
        'page_title': 'Dashboard',
        'total_kriteria': total_kriteria,
        'total_jurusan': total_jurusan,
        'total_preferensi': total_preferensi,
        'total_pengguna': total_pengguna,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
@never_cache
def input_nilai(request):
    """
    Menangani input nilai dari siswa menggunakan Django Form.
    """
    kriteria_list = Kriteria.objects.all().order_by('id')
    
    if request.method == 'POST':
        form = InputNilaiForm(request.POST, kriteria_list=kriteria_list)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Nilai Anda telah berhasil diinput! Hasil rekomendasi akan segera ditampilkan.')
            return redirect('dashboard:hasil_rekomendasi')
    else:
        # Untuk GET request, muat nilai yang sudah ada sebelumnya ke dalam form
        initial_data = {}
        for kriteria in kriteria_list:
            input_siswa = InputSiswa.objects.filter(user=request.user, kriteria=kriteria).first()
            if input_siswa:
                initial_data[f'nilai_{kriteria.id}'] = input_siswa.nilai
        
        form = InputNilaiForm(kriteria_list=kriteria_list, initial=initial_data)

    context = {
        'form': form,
        'page_title': 'Input Nilai Mata Pelajaran'
    }
    return render(request, 'dashboard/input_nilai.html', context)

@login_required
@never_cache
def hasil_rekomendasi(request):
    """
    Menampilkan hasil rekomendasi dengan memanggil AHPProcessor.
    """
    processor = AHPProcessor(user=request.user)
    hasil = processor.dapatkan_rekomendasi()

    context = {
        'hasil': hasil,
        'page_title': 'Hasil Rekomendasi Jurusan'
    }
    return render(request, 'dashboard/hasil_rekomendasi.html', context)

@login_required
@never_cache
def lihat_bobot_kriteria(request):
    """
    View terpisah untuk menampilkan hasil perhitungan AHP (bobot dan konsistensi).
    """
    processor = AHPProcessor()
    processor.hitung_bobot_kriteria()

    kriteria_zipped = zip(processor.kriteria_list, processor.bobot_kriteria) if processor.bobot_kriteria is not None else []
    
    context = {
        'kriteria_zipped': kriteria_zipped,
        'CI': processor.consistency_index,
        'CR': processor.konsistensi_rasio,
        'is_konsisten': processor.is_konsisten,
        'page_title': 'Analisis Bobot Kriteria (AHP)'
    }
    return render(request, 'dashboard/hasil_ahp.html', context)