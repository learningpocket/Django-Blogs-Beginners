# Generated by Django 3.2.3 on 2021-06-18 01:21

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]