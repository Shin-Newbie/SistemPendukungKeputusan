from django import forms
from .models import Kriteria, InputSiswa

class InputNilaiForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Ambil daftar kriteria yang dikirim dari view
        kriteria_list = kwargs.pop('kriteria_list', None)
        super().__init__(*args, **kwargs)
        
        if kriteria_list:
            # Buat field input untuk setiap kriteria secara dinamis
            for kriteria in kriteria_list:
                self.fields[f'nilai_{kriteria.id}'] = forms.FloatField(
                    label=kriteria.nama,
                    required=True,
                    min_value=0,
                    max_value=100,
                    widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
                )

    def save(self, user):
        # Simpan setiap nilai yang valid ke database
        for name, value in self.cleaned_data.items():
            # Ekstrak ID kriteria dari nama field (contoh: 'nilai_1' -> 1)
            kriteria_id = int(name.split('_')[1])
            kriteria = Kriteria.objects.get(id=kriteria_id)
            
            # Gunakan update_or_create untuk membuat data baru atau memperbarui yang sudah ada
            InputSiswa.objects.update_or_create(
                user=user,
                kriteria=kriteria,
                defaults={'nilai': value}
            )