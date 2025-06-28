from django import forms
from .models import Kriteria, InputSiswa

class InputNilaiForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kriteria_list = kwargs.pop('kriteria_list', None)
        super().__init__(*args, **kwargs)
        
        if kriteria_list:
            for kriteria in kriteria_list:
                self.fields[f'nilai_{kriteria.id}'] = forms.FloatField(
                    label=kriteria.nama,
                    required=True,
                    min_value=0,
                    max_value=100,
                    widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
                )

    def save(self, user):
        for name, value in self.cleaned_data.items():
            kriteria_id = int(name.split('_')[1])
            kriteria = Kriteria.objects.get(id=kriteria_id)
            
            InputSiswa.objects.update_or_create(
                user=user,
                kriteria=kriteria,
                defaults={'nilai': value}
            )