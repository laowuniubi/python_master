# Generated by Django 2.2.1 on 2019-06-27 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20190627_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='icon',
            field=models.FileField(default='default.jpg', upload_to='images'),
        ),
    ]