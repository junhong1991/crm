from django.db import models
from django.contrib.auth.models import AbstractUser


# class UserInfo(AbstractUser):
#     """用户信息表"""
#     nid = models.AutoField(primary_key=True)
#     create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
#
#     def __str__(self):
#         return self.username

class CustomerInfo(models.Model):
    """客户信息表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='客户姓名', max_length=20, unique=True)
    age = models.IntegerField(verbose_name='年龄')
    email = models.CharField(verbose_name='邮箱', max_length=32)
    company = models.CharField(verbose_name='公司', max_length=32)
