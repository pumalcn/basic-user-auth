# Generated by Django 4.2.9 on 2024-01-09 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="EmailVerificationToken",
        ),
    ]
