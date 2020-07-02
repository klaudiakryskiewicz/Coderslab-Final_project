import os
import sys

import pytest
from django.contrib.auth.models import User
from django.test import Client

from test.utils import create_fake_presents

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User(username='Superadmin')
    user.set_password("ABChaslo")
    user.save()
    return user


@pytest.fixture
def set_up():
    create_fake_presents()
