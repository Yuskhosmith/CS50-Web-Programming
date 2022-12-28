from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return{
            "user": self.user.username,
            "post": self.post,
            "timestamp": self.timestamp
        }

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_details")
    following = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='following')

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "following": self.following.username
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "post": self.post.post
        }

