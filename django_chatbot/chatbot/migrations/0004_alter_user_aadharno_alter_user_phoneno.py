# Generated by Django 4.1.11 on 2023-10-03 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='aadharNo',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='phoneNo',
            field=models.IntegerField(),
        ),
    ]