# Generated by Django 2.0.1 on 2018-05-10 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_user_header'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='header',
            new_name='header_image',
        ),
    ]