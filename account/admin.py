from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Siswa

class AdminUserCustom(UserAdmin):
    list_display = ('email', 'nama_depan', 'nama_belakang', 'jenis_user', 'is_staff')
    list_filter = ('jenis_user', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nama_depan', 'nama_belakang')
    ordering = ('email',)  # Order by email
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informasi Pribadi', {'fields': ('nama_depan', 'nama_belakang')}),
        ('Hak Akses', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'jenis_user', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'jenis_user', 'is_staff', 'is_superuser'),
        }),
    )

class AdminSiswa(admin.ModelAdmin):
    list_display = ('user', 'nama_lengkap', 'sekolah', 'kelas')
    search_fields = ('nama_lengkap', 'sekolah', 'user__email')
    raw_id_fields = ('user',)

admin.site.register(CustomUser, AdminUserCustom)
admin.site.register(Siswa, AdminSiswa)