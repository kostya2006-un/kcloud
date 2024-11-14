from django.urls import include, re_path, path
from .views import ActivateWithCodeView

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('auth/activate_with_code/', ActivateWithCodeView.as_view(), name='activate_with_code'),
]