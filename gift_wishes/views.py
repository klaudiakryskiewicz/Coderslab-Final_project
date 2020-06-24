from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from gift_wishes.models import Wish, Member, Family, Present


class AddWishView(CreateView):
    def get(self, request, **kwargs):
        pass


class WishListView(View):
    def get(self, request):
        pass


class PresentListView(View):
    def get(self, request):
        pass


class FamilyMembersView(View):
    def get(self, request):
        pass


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
