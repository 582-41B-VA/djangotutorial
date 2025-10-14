from django.db import models
from .validators import bad_keywords_validator


class Post(models.Model):
    title = models.CharField()
    body = models.TextField()
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField()
    email = models.EmailField()
    body = models.TextField(validators=[bad_keywords_validator])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
