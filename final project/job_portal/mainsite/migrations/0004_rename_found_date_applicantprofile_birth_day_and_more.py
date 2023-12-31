# Generated by Django 4.1 on 2023-10-25 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainsite", "0003_remove_applicantprofile_birthday_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="applicantprofile", old_name="found_date", new_name="birth_day",
        ),
        migrations.RenameField(
            model_name="applicantprofile", old_name="Phone", new_name="phone",
        ),
        migrations.AddField(
            model_name="applicantprofile",
            name="first_name",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="applicantprofile",
            name="last_name",
            field=models.CharField(default="", max_length=100),
        ),
    ]
