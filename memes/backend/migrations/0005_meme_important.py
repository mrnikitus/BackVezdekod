# Generated by Django 4.0.5 on 2022-06-19 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_like_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='important',
            field=models.BooleanField(default=False, help_text='Отметить, чтобы мем показывался чаще других', verbose_name='Важный'),
        ),
    ]