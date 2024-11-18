from django.contrib import admin
from .models import File, Trash, Folder
# Register your models here.

admin.site.register(File)
admin.site.register(Folder)
admin.site.register(Trash)