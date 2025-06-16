from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email wajib diisi.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom user model
class CustomUser(AbstractUser):
    class JenisUser(models.IntegerChoices):
        ADMINISTRATOR = 1, 'Administrator'
        SISWA = 2, 'Siswa'

    username = None  # Remove default username
    email = models.EmailField(_('alamat email'), unique=True)
    jenis_user = models.PositiveSmallIntegerField(
        _('jenis user'),
        choices=JenisUser.choices,
        default=JenisUser.SISWA
    )

    first_name = None
    last_name = None
    nama_depan = models.CharField(_('nama depan'), max_length=30, blank=True)
    nama_belakang = models.CharField(_('nama belakang'), max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Hubungkan ke CustomUserManager
    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.nama_depan} {self.nama_belakang}".strip()

    def get_short_name(self):
        return self.nama_depan

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']
        verbose_name = _('Pengguna')
        verbose_name_plural = _('Pengguna')

# Model siswa
class Siswa(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='account_siswa')
    nama_lengkap = models.CharField(max_length=100)
    sekolah = models.CharField(max_length=100)
    kelas = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Siswa"
        verbose_name_plural = "Siswa"

    def __str__(self):
        return f"{self.nama_lengkap} - {self.sekolah}"
