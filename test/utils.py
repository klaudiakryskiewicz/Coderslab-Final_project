from faker import Faker

from gift_wishes.models import Member, Family, Wish, Present
from django.contrib.auth.models import User

faker = Faker("pl_PL")


def create_fake_users():
    for _ in range(3):
        User.objects.create(username=faker.name(), password=faker.password())


def create_fake_members(family):
    create_fake_users()
    for _ in range(5):
        user = User.objects.order_by('?')[0]
        Member.objects.create(name=faker, family=family, user=user)


def fake_family_data():
    return {
        "name": faker.name(),
    }


def create_fake_family():
    family = Family.objects.create(**fake_family_data())
    create_fake_members(family)


def create_fake_wishes():
    create_fake_family()
    for _ in range(10):
        member = Member.objects.order_by('?')[0]
        Wish.objects.create(name=faker.word(), description=faker.text(), link=faker.word(), price=faker.random_number(),
                            member=member)


def create_fake_presents():
    create_fake_wishes()
    wishes = Wish.objects.order_by('?')
    for wish in wishes:
        user = User.objects.order_by('?')[0]
        Present.objects.create(user=user, wish=wish)
