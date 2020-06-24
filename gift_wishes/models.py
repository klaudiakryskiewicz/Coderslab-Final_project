from django.db import models
from django.contrib.auth.models import User


class Family(models.Model):
    name = models.CharField(max_length=120)

    def member_count(self):
        members = Member.objects.filter(family_id=self.id)
        return len(members)

    def __str__(self):
        return f"{self.name} {self.member_count}"


class Member(models.Model):
    genders = [('F', 'Kobieta'), ('M', 'Mężczyzna'), ('None', '-')]
    name = models.CharField(max_length=120)
    age = models.IntegerField() #może zmienić na date_of_birth?
    gender = models.CharField(max_length=9, choices=genders, default='None')
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def wish_count(self):
        wishes = Wish.objects.filter(member_id=self.id)
        return len(wishes)

    def __str__(self):
        return f"{self.name}, {self.wish_count}"


class Wish(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True)
    link = models.CharField(max_length=300, null=True)
    price = models.IntegerField(null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def is_booked(self):
        if Present.objects.get(wish_id=self.id):
            return True
        return False


class Present(models.Model):
    wish = models.OneToOneField(Wish, on_delete=models.CASCADE)
    is_bought = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.wish.name} {self.wish.member.name} {self.is_bought}"
