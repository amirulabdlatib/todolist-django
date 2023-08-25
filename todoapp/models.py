from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    task_user = models.ForeignKey(User,on_delete=models.CASCADE)
    task_name = models.CharField(max_length=500)
    task_status = models.BooleanField(default=False)
    

    def __str__(self):
        return self.task_name