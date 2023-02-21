from django.db import models

# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=34)
    password = models.CharField(max_length=64)
    age = models.IntegerField()


class UserList(models.Model):
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=11)

    def __str__(self):
        return self.name
