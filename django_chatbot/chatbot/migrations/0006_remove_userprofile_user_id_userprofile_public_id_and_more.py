# Generated by Django 4.1.11 on 2023-10-03 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatbot', '0005_userprofile_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_id',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='public_id',
            field=models.CharField(default='0', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
