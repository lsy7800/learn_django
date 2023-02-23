from django.db import models


class PhoneNumber(models.Model):
    mobile = models.CharField(max_length=11, verbose_name="手机号")

    lv_choice = (
        (1, "一级"),
        (2, "二级"),
        (3, "二级"),
        (4, "二级"),
        (5, "二级")
    )

    level = models.SmallIntegerField(choices=lv_choice, default=1, verbose_name="等级")
    status = models.BooleanField(default=False, verbose_name="状态")
    price = models.IntegerField(default=99, verbose_name="价格")

    def __str__(self):
        return self.mobile
