from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class todo(models.Model):
    title = models.CharField(max_length=50)
    memo = models.TextField(max_length=400, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)   # date and time
    targetDate = models.DateTimeField(null=True, blank=True)    # date and time => models.DateField() is only for date and not time
    important = models.BooleanField(default=False)      # booleanField model

    # this connects a model to a user, for example this task is for Kyle. it takes the id of user
    # and saves that id in this field. Actually we can see the user id when we go to users in admin, we can see it in
    # url address.
    # We got to import the user to pass to ForeignKey method
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    
