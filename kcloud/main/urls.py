from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import FileViewSet, FolderViewSet

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')
router.register(r'folders', FolderViewSet, basename='folders')

urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)