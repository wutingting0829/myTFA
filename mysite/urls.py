from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('account/', include('django.contrib.auth.urls')),
    path('fuzzy/', include('fuzzy.urls', namespace='fuzzy')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
