from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from gift_wishes.forms import WishForm, MemberForm, FamilyForm
from gift_wishes.models import Wish, Member, Present


def index(request):
    return render(request, 'base.html')


class AddWishView(CreateView):
    form_class = WishForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("wish-list", kwargs={'id': self.object.member.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['member'].queryset = Member.objects.filter(user=self.request.user)
        return form


class WishListView(View):
    def get(self, request, id):
        wishes = Wish.objects.filter(member_id=id)
        for wish in wishes:
            if wish.is_booked:
                wish.delete()
        return render(request, 'wishlist.html', {'objects': wishes})


class PresentListView(View):
    def get(self, request, id):
        presents = Present.objects.filter(user_id=id)
        return render(request, 'presentlist.html', {'objects': presents})


class FamilyMembersView(View):
    def get(self, request, id):
        members = Member.objects.filter(family_id=id)
        return render(request, 'memberlist.html', {'objects': members})


class AddMemberView(CreateView):
    form_class = MemberForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("family", kwargs={'id': self.object.family.id})

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.user = self.request.user
        obj.save()
        self.object = obj
        return HttpResponseRedirect(self.get_success_url())


class AddFamilyView(CreateView):
    form_class = FamilyForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("family", kwargs={'id': self.object.family.id})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("add-family")
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        retval = super().form_valid(form)
        Member.objects.create(user=self.object)  # uzupełnij sobie


class SignUpFamilyView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("add-member")
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        retval = super().form_valid(form)
        Member.objects.create(user=self.object)  # uzupełnij sobie
