from django.db import models


# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=34)
    password = models.CharField(max_length=64)
    age = models.IntegerField()


class Department(models.Model):
    title = models.CharField(verbose_name="部门名称", max_length=10)

    def __str__(self):
        return self.title


class UserList(models.Model):
    name = models.CharField(verbose_name='用户名', max_length=64)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    # 性别
    gender_choice = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice, default=1)
    phone_number = models.CharField(verbose_name="电话", max_length=11)
    salary = models.DecimalField(verbose_name="薪资", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间", null=True, blank=True)
    # to 表示与哪张表进行关联
    # to_fields 表示与表中的哪一列数据进行关联
    # on_delete=models.CASCADE 表示级联删除，删除部门后与之关联的表信息均会删除
    # on_delete=models.SET_NULL 表示删除部门后与之关联的信息会设置为空
    department = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    """定义一个靓号数据库"""
    mobile = models.CharField(max_length=11, verbose_name="手机号")

    lv_choice = (
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
        (5, "五级")
    )

    level = models.SmallIntegerField(choices=lv_choice, default=1, verbose_name="等级")

    status_choices = (
        (1, "以售卖"),
        (2, "待售卖")
    )

    status = models.SmallIntegerField(choices=status_choices, default=2, verbose_name="状态")
    price = models.IntegerField(default=99, verbose_name="价格")

    def __str__(self):
        return self.mobile
