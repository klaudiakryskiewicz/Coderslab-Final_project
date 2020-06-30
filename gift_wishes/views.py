from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from gift_wishes.forms import WishForm, MemberForm, FamilyForm
from gift_wishes.models import Wish, Member, Present
from gift_wishes.templatetags.tags import get_family_id


def index(request):
    family_id = get_family_id(request)
    member_number = Member.objects.filter(family=family_id).count()
    user = request.user
    control_member = Member.objects.filter(user=user)
    control_member_number = control_member.count()
    presents = Present.objects.filter(user=user)
    present_number = presents.count()
    present_to_buy = presents.filter(is_bought=False).count()
    return render(request, 'home.html', {'member_number': member_number, 'control_member_number': control_member_number,
                                         'control_member': control_member, 'present_number':present_number,
                                         'present_to_buy':present_to_buy})


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
        wishes = Wish.objects.filter(member_id=id, present__isnull=True)
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


class SignUpFamilyView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("add-member")
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        retval = super().form_valid(form)
        Member.objects.create(user=self.object)  # uzupełnij sobie


class InviteView(View):
    def get(self, request):
        return render(request, 'invite.html')


class BookWish(View):
    def post(self, request):
        wish_id = request.POST.get("wish_id")
        wish = Wish.objects.get(id=wish_id)
        member = Member.objects.get(id=wish.member_id)
        user = request.user
        Present.objects.create(wish_id=wish_id, user_id=user.id)
        return redirect(f"/wish-list/{member.id}")


class BuyPresent(View):
    def post(self, request):
        present_id = request.POST.get("present_id")
        present = Present.objects.get(id=present_id)
        present.is_bought = True
        present.save()
        user = request.user
        return redirect(f"/present-list/{user.id}")
