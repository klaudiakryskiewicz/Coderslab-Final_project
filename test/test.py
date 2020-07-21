from gift_wishes.models import Family, Member, Present, Wish
from .utils import create_fake_family
import pytest




#czy ilość członków jest taka sama jak w bazie - response.contex
@pytest.mark.django_db
def test_member_list(client, user, set_up):
    client.login(username='Superadmin', password='ABChaslo')
    response = client.get("/family/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_wish(client, user, set_up):
    client.login(username='Superadmin', password='ABChaslo')
    response = client.get("/add-wish/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_member(client, user, set_up):
    client.login(username='Superadmin', password='ABChaslo')
    response = client.get("/add-member/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_present_list(client, user, set_up):
    client.login(username='Superadmin', password='ABChaslo')
    response = client.get("/present-list/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_wish_list(client, user, set_up):
    member = Member.objects.order_by('?')[0]
    response = client.get(f'/wish-list/{member.id}/')

    assert response.status_code == 200