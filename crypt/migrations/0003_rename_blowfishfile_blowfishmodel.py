# Generated by Django 4.2.7 on 2023-11-11 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypt', '0002_alter_blowfishfile_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlowfishFile',
            new_name='BlowfishModel',
        ),
    ]
