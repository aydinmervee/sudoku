# Generated by Django 2.2.13 on 2020-07-04 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0002_sudoku_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='sudoku',
            name='solution',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]
