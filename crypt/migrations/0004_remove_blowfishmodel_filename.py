# Generated by Django 4.2.7 on 2023-11-11 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypt', '0003_rename_blowfishfile_blowfishmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blowfishmodel',
            name='filename',
        ),
    ]
