from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from gift_wishes.forms import WishForm, MemberForm, FamilyForm
from gift_wishes.models import Wish, Member, Present, Family
from gift_wishes.templatetags.tags import get_family_id, get_user_id, get_family


def index(request):
    if request.user.is_authenticated:
        family_id = get_family_id(request)
        member_number = Member.objects.filter(family=family_id).count()
        user = request.user
        control_member = Member.objects.filter(user=user)
        control_member_number = control_member.count()
        presents = Present.objects.filter(user=user)
        present_number = presents.count()
        present_to_buy = presents.filter(is_bought=False).count()
        return render(request, 'home.html',
                      {'member_number': member_number, 'control_member_number': control_member_number,
                       'control_member': control_member, 'present_number': present_number,
                       'present_to_buy': present_to_buy})
    return render(request, 'base.html')


class AddWishView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    form_class = WishForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("wish-list", kwargs={'id': self.object.member.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['member'].queryset = Member.objects.filter(user=self.request.user)
        return form


class WishListView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request, id):
        wishes = Wish.objects.filter(member_id=id, present__isnull=True)
        return render(request, 'wishlist.html', {'objects': wishes})


class PresentListView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        id = get_user_id(request)
        presents = Present.objects.filter(user_id=id)
        return render(request, 'presentlist.html', {'objects': presents})


class FamilyMembersView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        id = get_family_id(request)
        members = Member.objects.filter(family_id=id)
        return render(request, 'memberlist.html', {'objects': members})


class AddMemberView(CreateView):
    form_class = MemberForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("family")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.family = get_family(self.request)
        obj.main_member = False
        obj.save()
        self.object = obj
        return HttpResponseRedirect(self.get_success_url())


class AddMainMemberView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request, id):
        form = MemberForm()
        return render(request, 'form.html', {'form': form, 'id': id})

    def post(self, request, id):
        form = MemberForm(request.POST)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.family = Family.objects.get(id=id)
        obj.main_member = True
        obj.save()
        return redirect('family')


class AddFamilyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = FamilyForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = FamilyForm(request.POST)
        if form.is_valid():
            obj = form.save()
            id = obj.id
            return redirect(f'/add-main-member/{id}')
        return render(request, 'registration/signup.html', {'form': form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy("add-family")

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class SignUpFamilyView(View):

    def get(self, request, id):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form, 'id': id})

    def post(self, request, id):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect(f'/add-main-member/{id}')
        return render(request, 'registration/signup.html', {'form': form, 'id': id})


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
        return redirect(f"/present-list")


class WishView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        family_id = get_family_id(request)
        members = Member.objects.filter(family=family_id)
        return render(request, 'wishes.html', {'members': members})
