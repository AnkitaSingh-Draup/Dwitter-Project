from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dweets(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dweet=models.CharField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    like = models.ManyToManyField(User,related_name='like',null=True, blank=True)

class Comments(models.Model):
    comment = models.CharField(max_length=100)
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    dweet = models.ForeignKey(Dweets, on_delete=models.CASCADE)


class Followers(models.Model):
    followed_by=models.ForeignKey(User,related_name='Followed_by',on_delete=models.CASCADE)
    following=models.ForeignKey(User,related_name='Following',on_delete=models.CASCADE)
