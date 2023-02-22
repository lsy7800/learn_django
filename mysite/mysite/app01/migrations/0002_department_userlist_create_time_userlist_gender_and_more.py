# Generated by Django 4.1.7 on 2023-02-22 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
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
                ("title", models.CharField(max_length=10, verbose_name="部门名称")),
            ],
        ),
        migrations.AddField(
            model_name="userlist",
            name="create_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="入职时间"),
        ),
        migrations.AddField(
            model_name="userlist",
            name="gender",
            field=models.SmallIntegerField(
                choices=[(1, "男"), (2, "女")], default=1, verbose_name="性别"
            ),
        ),
        migrations.AddField(
            model_name="userlist",
            name="salary",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, verbose_name="薪资"
            ),
        ),
        migrations.AlterField(
            model_name="userlist",
            name="age",
            field=models.IntegerField(verbose_name="年龄"),
        ),
        migrations.AlterField(
            model_name="userlist",
            name="name",
            field=models.CharField(max_length=64, verbose_name="用户名"),
        ),
        migrations.AlterField(
            model_name="userlist",
            name="password",
            field=models.CharField(max_length=64, verbose_name="密码"),
        ),
        migrations.AlterField(
            model_name="userlist",
            name="phone_number",
            field=models.CharField(max_length=11, verbose_name="电话"),
        ),
        migrations.AddField(
            model_name="userlist",
            name="department",
            field=models.ForeignKey(
                blank=True,
                default=1,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app01.department",
                verbose_name="部门",
            ),
        ),
    ]
