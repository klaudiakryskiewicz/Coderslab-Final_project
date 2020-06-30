from django import forms

from gift_wishes.models import Family, Member, Wish


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['user']


class WishForm(forms.ModelForm):
    class Meta:
        model = Wish
        fields = '__all__'


