# Generated by Django 2.2.13 on 2020-07-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sudoku',
            name='size',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
