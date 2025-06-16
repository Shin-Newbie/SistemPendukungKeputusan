# dashboard/admin.py
from django.contrib import admin
from .models import *

admin.site.register(Kriteria)
admin.site.register(Jurusan)
admin.site.register(PreferensiJurusan)
admin.site.register(InputSiswa)
admin.site.register(MatriksPerbandinganKriteria)
