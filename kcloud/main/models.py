import os

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


def user_file_upload_path(instance, filename):
    """Генерация пути для сохранения файла: user_<id>/<filename>."""
    return f"user_{instance.owner.id}/{now().strftime('%Y/%m/%d')}/{filename}"


class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    name = models.CharField(max_length=255, blank=True, null=True, help_text="Имя файла. По умолчанию используется имя загружаемого файла.")  # Имя файла (уникальное для пользователя)
    file = models.FileField(upload_to=user_file_upload_path)  # Путь загрузки
    size = models.BigIntegerField(editable=False)  # Размер файла (байты)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Время загрузки
    is_shared = models.BooleanField(default=False)  # Флаг общего доступа
    parent_folder = models.ForeignKey(
        "Folder", on_delete=models.SET_NULL, null=True, blank=True, related_name="files"
    )

    class Meta:
        unique_together = ('owner', 'name')  # Имя файла должно быть уникальным для каждого пользователя

    def __str__(self):
        return f"{self.name} ({self.size} bytes)"

    def save(self, *args, **kwargs):
        # Если файл уже существует, определяем его размер
        if not self.name:
            self.name = os.path.basename(self.file.name)

        if self.file and not self.size:
            self.size = self.file.size

        # Проверяем, не превышает ли файл лимит хранилища
        if self.owner.storage_used + self.size > self.owner.storage_limit:
            raise ValueError("Превышен лимит хранения данных.")

        super().save(*args, **kwargs)

        # Обновляем использованное пространство владельца
        self.owner.storage_used += self.size
        self.owner.save()

    def delete(self, *args, **kwargs):
        # Уменьшаем использованное пространство владельца перед удалением файла
        self.owner.storage_used -= self.size
        self.owner.save()

        super().delete(*args, **kwargs)


class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    parent_folder = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name="subfolders")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("owner", "name", "parent_folder")

    def __str__(self):
        return f"Folder: {self.name}"


class Trash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trash")
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="trash_item")
    deleted_at = models.DateTimeField(auto_now_add=True)  # Дата удаления

    def __str__(self):
        return f"Trash: {self.file.name}"