from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    


class Posts(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    

    def count_likes(self):
        return self.likes.count()
    
    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "message": self.message,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
            "people_liked": list(self.likes.values_list("username", flat=True))
        }

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_rel")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_rel")
