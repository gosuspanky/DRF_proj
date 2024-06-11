# Generated by Django 5.0.6 on 2024-06-11 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lessons",
                to="materials.course",
                verbose_name="Курс",
            ),
        ),
    ]
