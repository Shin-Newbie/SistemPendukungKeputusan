from django.contrib import admin
from django.urls import path, include
from mysite.views import *
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import dashboard_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_home, name='login'),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
