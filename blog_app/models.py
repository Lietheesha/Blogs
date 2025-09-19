from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " by " + str(self.user.username)

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)]) 

