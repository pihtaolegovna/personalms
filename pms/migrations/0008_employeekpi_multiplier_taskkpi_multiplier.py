# Generated by Django 4.2.16 on 2024-10-29 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0007_employeedepartment_can_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeekpi',
            name='multiplier',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
        ),
        migrations.AddField(
            model_name='taskkpi',
            name='multiplier',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
        ),
    ]
