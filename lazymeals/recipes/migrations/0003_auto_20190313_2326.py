# Generated by Django 2.1.7 on 2019-03-13 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20190312_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='url',
            field=models.CharField(max_length=1024, unique=True, verbose_name='url'),
        ),
    ]