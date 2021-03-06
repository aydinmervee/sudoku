# Generated by Django 2.2.13 on 2020-07-05 14:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0003_sudoku_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='sudoku',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sudoku',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
