from django import template

from gift_wishes.models import Member, Family

register = template.Library()


@register.simple_tag
def get_family_id(request):
    if request.user.is_authenticated:
        members = Member.objects.filter(user=request.user)
        family = Family.objects.get(member=members[0])
        return family.id


@register.simple_tag
def get_family_id(request):
    if request.user.is_authenticated:
        user = request.user
        return user.id
