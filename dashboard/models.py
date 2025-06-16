from django.db import models
from django.conf import settings

class Kriteria(models.Model):
    kode = models.CharField(max_length=10, null=True, unique=True)
    nama = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.kode} - {self.nama}"
    
class Jurusan(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.kode} - {self.nama}"
    
class PreferensiJurusan(models.Model):
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE)
    nilai = models.FloatField()

    def __str__(self):
        return f"{self.jurusan} - {self.kriteria}: {self.nilai}"


class InputSiswa(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE)
    nilai = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.kriteria.nama}: {self.nilai}"

class MatriksPerbandinganKriteria(models.Model):
    kriteria1 = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='kriteria1')
    kriteria2 = models.ForeignKey(Kriteria, on_delete=models.CASCADE, related_name='kriteria2')
    nilai = models.FloatField()

    def __str__(self):
        return f"{self.kriteria1.nama} dibanding {self.kriteria2.nama}: {self.nilai}"



