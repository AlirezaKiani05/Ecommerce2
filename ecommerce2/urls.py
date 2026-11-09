from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from ecommerce2.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('users.urls')),
    path('api/payments/', include('payments.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
]
if settings.IS_DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)

    # kc.bat start-dev
