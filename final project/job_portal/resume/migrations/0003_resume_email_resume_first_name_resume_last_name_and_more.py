# Generated by Django 4.1 on 2023-11-29 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume", "0002_skill_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="email",
            field=models.EmailField(default=1, max_length=30, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resume",
            name="first_name",
            field=models.CharField(default="None", max_length=100, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resume",
            name="last_name",
            field=models.CharField(default=None, max_length=100, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resume",
            name="phone",
            field=models.CharField(default=None, max_length=20, null=True),
            preserve_default=False,
        ),
    ]
