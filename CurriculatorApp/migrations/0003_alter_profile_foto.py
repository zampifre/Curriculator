# Generated by Django 4.0.4 on 2022-05-09 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CurriculatorApp', '0002_alter_profile_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='foto',
            field=models.ImageField(blank=True, default='static/images/unknow.png', null=True, upload_to='static/images/'),
        ),
    ]
