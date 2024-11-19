from .models import File, Folder
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(source='owner.email')

    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'size', 'uploaded_at', 'is_shared', 'parent_folder', 'owner']
        read_only_fields = ['id', 'size', 'uploaded_at']

    def create(self, validated_data):
        # Размер файла вычисляется автоматически в save()
        return File.objects.create(**validated_data)


class FolderSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(source='owner.email')

    class Meta:
        model = Folder
        fields = ['id', 'name', 'owner']
        read_only_fields = ['id']
