from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20, unique=True)
    upwd = models.CharField(max_length=20)
    uemail = models.EmailField(max_length=30)

    recver = models.CharField(max_length=10, null=True)
    upostal = models.CharField(max_length=6, null=True)
    uphone = models.CharField(max_length=11, null=True)

class Adress(models.Model):
    pro = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True, default=None)
    street = models.CharField(max_length=20, null=True, default=None)
    uaddrs = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, related_name='uaddrs')
    ushipaddrs = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, related_name='ushipaddrs')
    def __str__(self):
        return '%s,%s,%s'%(self.pro, self.city, self.street)
