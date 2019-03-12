# Generated by Django 2.1.7 on 2019-03-12 00:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name='extra data'),
        ),
        migrations.AddField(
            model_name='sourcewebsite',
            name='name',
            field=models.CharField(default='name', max_length=128, verbose_name='name'),
            preserve_default=False,
        ),
    ]
