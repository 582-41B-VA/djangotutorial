from django.db import models


class Subscription(models.Model):
    name = models.CharField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.name)
