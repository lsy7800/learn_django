# Generated by Django 4.1.7 on 2023-02-23 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0006_phonenumber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="phonenumber",
            name="level",
            field=models.SmallIntegerField(
                choices=[(1, "一级"), (2, "二级"), (3, "三级"), (4, "四级"), (5, "五级")],
                default=1,
                verbose_name="等级",
            ),
        ),
    ]