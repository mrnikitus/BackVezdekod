# Generated by Django 4.0.5 on 2022-06-19 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_meme_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]
