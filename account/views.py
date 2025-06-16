# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CombinedRegistrationForm, CustomAuthenticationForm, SiswaUpdateForm
from .models import Siswa
from dashboard.models import InputSiswa
from django.views.decorators.cache import never_cache

def registrasi(request):
    if request.method == "POST":
        form = CombinedRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Registrasi berhasil! Silakan login.")
            return redirect("account:login")
        else:
            messages.error(request, "Terdapat kesalahan pada input Anda. Silakan periksa kembali.")
    else:
        form = CombinedRegistrationForm()
        
    return render(request, "account/register.html", {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  
            login(request, user)
            
            if hasattr(user, 'account_siswa'):
                messages.success(request, f'Selamat datang, {user.account_siswa.nama_lengkap}!')
            else:
                messages.success(request, f'Selamat datang, {user.email}!')
            
            return redirect('dashboard:home') 
        else:
                messages.error(request, 'Email atau password yang Anda masukkan salah. Silakan coba lagi.')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'account/login.html', {'form': form})

@login_required
@never_cache
def user_logout(request):
    logout(request)
    messages.info(request, 'Anda telah berhasil logout.')
    return redirect('account:login')


@login_required
@never_cache
def profile(request):
    try:
        siswa = request.user.account_siswa
    except Siswa.DoesNotExist:
        messages.error(request, 'Profil siswa tidak ditemukan.')
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = SiswaUpdateForm(request.POST, instance=siswa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('account:profile')
    else:
        form = SiswaUpdateForm(instance=siswa)

    # Ambil nilai siswa
    nilai_siswa = InputSiswa.objects.filter(user=request.user).select_related('kriteria')
    nilai_mapel = {item.kriteria.nama: item.nilai for item in nilai_siswa}

    context = {
        'form': form,
        'nilai_mapel': nilai_mapel
    }
    return render(request, 'account/profile.html', context)