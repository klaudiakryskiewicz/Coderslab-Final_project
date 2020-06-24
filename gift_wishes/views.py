from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from gift_wishes.models import Wish, Member, Present


class AddWishView(CreateView):
    def get(self, request, **kwargs):
        pass


class WishListView(View):
    def get(self, request, id):
        wishes = Wish.objects.filter(member_id=id)
        return render(request, 'list.html', {'objects': wishes})


class PresentListView(View):
    def get(self, request, id):
        presents = Present.objects.filter(user_id=id)
        return render(request, 'list.html', {'objects':presents})


class FamilyMembersView(View):
    def get(self, request, id):
        members = Member.objects.filter(family_id=id)
        return render(request, 'list.html', {'objects': members})


class AddMemberView(CreateView):
    def get(self, request, **kwargs):
        pass


class AddFamilyView(CreateView):
    def get(self, request, **kwargs):
        pass


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'
