# Generated by Django 4.1.3 on 2023-08-29 12:05

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_userprofile_id_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
