# Generated by Django 4.1.7 on 2023-02-21 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=34)),
                ("password", models.CharField(max_length=64)),
                ("age", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="UserList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("password", models.CharField(max_length=64)),
                ("age", models.IntegerField()),
                ("phone_number", models.CharField(max_length=11)),
            ],
        ),
    ]
