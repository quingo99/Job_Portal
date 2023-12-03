# Generated by Django 4.1 on 2023-10-23 19:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mainsite", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employerprofile",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employer_addresses",
                to="mainsite.address",
            ),
        ),
        migrations.AlterField(
            model_name="employerprofile",
            name="found_date",
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
    ]