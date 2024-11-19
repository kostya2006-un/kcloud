from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .serializers import FileSerializer, FolderSerializer
from rest_framework import viewsets, status
from rest_framework import permissions
from .models import File, Folder
# Create your views here.


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parent_folder', 'is_shared']
    search_fields = ['name']
    ordering_fields = ['uploaded_at', 'size']

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        folder_id = request.data.get("parent_folder")
        if folder_id:
            try:
                folder = Folder.objects.get(id=folder_id)
            except Folder.DoesNotExist:
                return Response(
                    {"detail": "Папка не найдена."},
                    status=status.HTTP_404_NOT_FOUND
                )
            if folder.owner != request.user:
                return Response(
                    {"detail": "Вы не можете добавлять файлы в чужую папку."},
                    status=status.HTTP_403_FORBIDDEN
                )

                # Если всё в порядке, продолжаем создание файла
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parent_folder']
    search_fields = ['name']

    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)