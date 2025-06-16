from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', RedirectView.as_view(pattern_name='account:login', permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)