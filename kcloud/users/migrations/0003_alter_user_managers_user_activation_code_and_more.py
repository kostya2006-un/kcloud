# Generated by Django 5.1.3 on 2024-11-14 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='activation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='activation_code_expires',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
