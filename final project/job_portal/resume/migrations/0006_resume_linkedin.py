# Generated by Django 4.1 on 2023-11-29 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume", "0005_alter_resume_email_alter_resume_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="linkedIn",
            field=models.CharField(default="", max_length=100, null=True),
        ),
    ]
