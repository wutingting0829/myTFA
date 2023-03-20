from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'fuzzy'

urlpatterns = [
    path('fuzzy/', views.fuzzy_extractor, name='fuzzy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print(settings.MEDIA_URL)
