# Generated by Django 5.0.6 on 2024-06-11 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_payments"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payments",
            name="data",
            field=models.DateField(auto_now_add=True, null=True, verbose_name="оплаты"),
        ),
    ]