# Generated by Django 4.1.11 on 2023-10-03 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_userdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password1', models.CharField(max_length=128)),
                ('password2', models.CharField(max_length=128)),
                ('userID', models.CharField(max_length=20)),
                ('aadharNo', models.IntegerField(max_length=12)),
                ('phoneNo', models.IntegerField(max_length=10)),
                ('language', models.CharField(max_length=50)),
            ],
        ),
    ]
