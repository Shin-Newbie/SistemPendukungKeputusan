import numpy as np
from .models import Kriteria, Jurusan, MatriksPerbandinganKriteria, PreferensiJurusan, InputSiswa

# Maksimal nilai yang mungkin untuk input siswa (misal: 100 untuk skala 0-100)
MAX_STUDENT_SCORE = 100.0

class AHPProcessor:
    def __init__(self, user=None):
        self.user = user
        self.kriteria_list = Kriteria.objects.all().order_by('id')
        self.jurusan_list = Jurusan.objects.all()
        self.n = self.kriteria_list.count()
        self.bobot_kriteria = None
        self.consistency_index = 0
        self.konsistensi_rasio = None
        self.is_konsisten = False

    def hitung_bobot_kriteria(self):
        if self.n == 0:
            print("[DEBUG AHP] self.n adalah 0. Tidak ada kriteria.") # DEBUG
            return False

        matriks = np.ones((self.n, self.n))
        for i in range(self.n):
            for j in range(i + 1, self.n):
                try:
                    perbandingan = MatriksPerbandinganKriteria.objects.get(
                        kriteria1=self.kriteria_list[i],
                        kriteria2=self.kriteria_list[j]
                    )
                    matriks[i, j] = perbandingan.nilai
                    matriks[j, i] = 1.0 / perbandingan.nilai
                except MatriksPerbandinganKriteria.DoesNotExist:
                    try: # Mencari perbandingan terbalik jika tidak ada yang langsung
                        perbandingan = MatriksPerbandinganKriteria.objects.get(
                            kriteria1=self.kriteria_list[j],
                            kriteria2=self.kriteria_list[i]
                        )
                        matriks[j, i] = perbandingan.nilai
                        matriks[i, j] = 1.0 / perbandingan.nilai
                    except MatriksPerbandinganKriteria.DoesNotExist:
                        # Jika perbandingan tidak ada sama sekali, asumsikan 1 (sama penting)
                        # ATAU biarkan sebagai 1 (dari np.ones) jika itu yang diinginkan
                        # Untuk AHP yang benar, semua perbandingan harus ada.
                        print(f"[DEBUG AHP] Peringatan: Perbandingan antara {self.kriteria_list[i].nama} dan {self.kriteria_list[j].nama} tidak ditemukan. Menggunakan nilai default 1.") # DEBUG
                        matriks[i,j] = 1.0 # Pastikan ini di set
                        matriks[j,i] = 1.0 # Pastikan ini di set
                        pass
        
        print(f"\n[DEBUG AHP] Jumlah Kriteria (self.n): {self.n}") # DEBUG
        print(f"[DEBUG AHP] Matriks Perbandingan Akhir Sebelum Normalisasi: \n{matriks}") # DEBUG

        # Normalisasi dan hitung bobot
        kolom_total = matriks.sum(axis=0)
        print(f"[DEBUG AHP] Total per Kolom: {kolom_total}") # DEBUG

        if np.any(kolom_total == 0):
            print("[DEBUG AHP] Error: Ada kolom total yang nol. Pastikan semua perbandingan ada.") # DEBUG
            return False 
        
        matriks_normal = matriks / kolom_total
        print(f"[DEBUG AHP] Matriks Normalisasi: \n{matriks_normal}") # DEBUG
        
        self.bobot_kriteria = matriks_normal.mean(axis=1)
        print(f"[DEBUG AHP] Bobot Kriteria Dihitung: {self.bobot_kriteria}") # DEBUG

        # Hitung Konsistensi
        eigenvalues, _ = np.linalg.eig(matriks)
        
        print(f"[DEBUG AHP] Semua Eigenvalues: {eigenvalues}") # DEBUG
        print(f"[DEBUG AHP] Bagian Real dari Eigenvalues: {np.real(eigenvalues)}") # DEBUG

        # Perbaikan di sini: Ambil bagian real dari semua eigenvalue, lalu cari nilai maksimumnya
        lambda_max = np.max(np.real(eigenvalues)) 
        
        print(f"[DEBUG AHP] Lambda Maks (setelah perbaikan): {lambda_max}") # DEBUG

        self.consistency_index = (lambda_max - self.n) / (self.n - 1) if (self.n - 1) != 0 else 0
        
        RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_dict.get(self.n, 1.49)
        
        self.konsistensi_rasio = self.consistency_index / RI if RI != 0 else 0
        self.is_konsisten = self.konsistensi_rasio < 0.1
        
        print(f"[DEBUG AHP] CI yang disimpan: {self.consistency_index}") # DEBUG
        print(f"[DEBUG AHP] CR yang disimpan: {self.konsistensi_rasio}") # DEBUG
        print(f"[DEBUG AHP] Matriks Konsisten: {self.is_konsisten}") # DEBUG
        
        return True

    def dapatkan_rekomendasi(self):
        if self.bobot_kriteria is None:
            if not self.hitung_bobot_kriteria():
                return []

        bobot_dict = {kriteria.nama: bobot for kriteria, bobot in zip(self.kriteria_list, self.bobot_kriteria)}
        
        nilai_input_queryset = InputSiswa.objects.filter(user=self.user).select_related('kriteria')
        nilai_input_dict = {item.kriteria.nama: item.nilai for item in nilai_input_queryset}

        hasil_rekomendasi = []
        for jurusan in self.jurusan_list:
            skor_total = 0.0
            for kriteria in self.kriteria_list:
                bobot = bobot_dict.get(kriteria.nama, 0)
                nilai_siswa = nilai_input_dict.get(kriteria.nama, 0)
                
                preferensi = PreferensiJurusan.objects.filter(jurusan=jurusan, kriteria=kriteria).first()
                nilai_preferensi = preferensi.nilai if preferensi else 0.0
                
                normalized_nilai = nilai_siswa / MAX_STUDENT_SCORE if MAX_STUDENT_SCORE > 0 else 0.0
                
                skor_total += (normalized_nilai * nilai_preferensi) * bobot
            
            hasil_rekomendasi.append({'jurusan': jurusan, 'skor': skor_total})
            
        return sorted(hasil_rekomendasi, key=lambda x: x['skor'], reverse=True)