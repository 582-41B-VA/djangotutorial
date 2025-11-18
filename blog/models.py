from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import bad_keywords_validator


class Post(models.Model):
    title = models.CharField(_("title"))
    body = models.TextField(_("body"))
    pub_date = models.DateTimeField(_("date published"))

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(_("name"))
    email = models.EmailField(_("email"))
    body = models.TextField(_("body"), validators=[bad_keywords_validator])
    created = models.DateTimeField(_("date created"), auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
