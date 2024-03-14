from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default = now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete = models.CASCADE)
    source = models.CharField(max_length = 255)
    
    def __str__(self) -> str:
        return self.source
    # model meta cua django giup thuc hien 1 so chuc nang
    class Meta:
        # sap xep giam dan theo ngay
        ordering = ['-date']

class Source(models.Model):
    name = models.CharField(max_length = 255)
    
    
    def __str__(self) -> str:
        return self.name
    
         