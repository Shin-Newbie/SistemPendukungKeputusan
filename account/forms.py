from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Siswa

class CombinedRegistrationForm(forms.Form):
    nama_lengkap = forms.CharField(
        label="Nama Lengkap",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nama@contoh.com'})
    )
    sekolah = forms.CharField(
        label="Sekolah",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asal Sekolah'})
    )
    kelas = forms.ChoiceField(
        label="Kelas",
        choices=[('', 'Pilih Kelas'), ('10', 'Kelas 10'), ('11', 'Kelas 11'), ('12', 'Kelas 12')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        label="Password",
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    konfirmasi_password = forms.CharField(
        label="Konfirmasi Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Konfirmasi Password'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ini sudah terdaftar.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        konfirmasi_password = cleaned_data.get("konfirmasi_password")

        if password and konfirmasi_password and password != konfirmasi_password:
            self.add_error('konfirmasi_password', "Password dan konfirmasi tidak cocok.")
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = CustomUser.objects.create_user(
            email=data['email'],
            password=data['password'],
            jenis_user=CustomUser.JenisUser.SISWA
        )
        nama_split = data['nama_lengkap'].split(' ', 1)
        user.nama_depan = nama_split[0]
        if len(nama_split) > 1:
            user.nama_belakang = nama_split[1]
        user.save()

        Siswa.objects.create(
            user=user,
            nama_lengkap=data['nama_lengkap'],
            sekolah=data['sekolah'],
            kelas=data['kelas']
        )
        return user

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}))

class SiswaUpdateForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = ['nama_lengkap', 'sekolah', 'kelas']