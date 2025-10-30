from typing_extensions import Required
from django.db import models


class Subscription(models.Model):
    name = models.CharField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    name = models.CharField(blank=True)
    email = models.EmailField(blank=True, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    payment_id = models.CharField(blank=True)

    def fulfill(self, name: str, email: str, payment_id: str) -> None:
        self.name = name
        self.email = email
        self.payment_id = payment_id
        self.save()
