from django.db import models
from django.contrib.auth.models import User


class Family(models.Model):
    name = models.CharField(max_length=120)


class Member(models.Model):
    genders = [('F', 'Kobieta'), ('M', 'Mężczyzna'), ('None', '-')]
    name = models.CharField(max_length=120)
    age = models.IntegerField()
    gender = models.CharField(max_length=9, choices=genders, default='None')
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)


class Wish(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    link = models.CharField(max_length=300)
    price = models.IntegerField()
    Member = models.ManyToManyField(Member)


class Present(models.Model):
    wish = models.OneToOneField(Wish, on_delete=models.CASCADE)
    is_bought = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
