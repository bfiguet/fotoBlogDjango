# Generated by Django 5.0.4 on 2024-04-29 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='word_count',
            field=models.IntegerField(null=True),
        ),
    ]