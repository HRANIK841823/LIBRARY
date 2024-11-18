from django.db import models
#user
from django.contrib.auth.models import User
class UserAccount(models.Model):
    user=models.OneToOneField(User,related_name="account",on_delete=models.CASCADE)
    balance=models.DecimalField(default=0,max_digits=12,decimal_places=2)
    balance_after_transiction=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,default=0)
    def __str__(self) :
        return f"self.user.username"