from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
import uuid

class Post(models.Model):
    
    title = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    tags = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name='shared_posts', blank=True)

    # def __str__(self):
    #     return self.title
    
    def get_detail_url(self):
        return reverse(
            'post:detail',
            kwargs={
                "uuid": self.uuid
            }
        )
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    