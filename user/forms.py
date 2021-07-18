from django import forms
from django.contrib.auth import get_user_model
from .models import Link
from django.forms import inlineformset_factory

from acm.models import UserOnlineJudge, JudgeName


class UserProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Provide a strong password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text="Confirm your password")

    class Meta:
        model = get_user_model()
        fields = ['student_id']
        # fields = ['student_id', 'github', 'linkedIn', 'facebook']

        help_texts = {
            'student_id': "Enter your university ID",
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        # user = self.instance
        user = kwargs.get('instance', None)

        if user.is_active:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False

    def clean(self):
        user = self.instance

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('password', "Password don't match.")
            self.add_error('confirm_password', "Password don't match.")

    def save(self, commit=True, **kwargs):
        user = super(UserProfileUpdateForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        is_new = kwargs['is_new']

        if commit and is_new:
            user.is_active = True
            user.set_password(password)
            user.save()
        elif commit and not is_new:
            if password:
                user.set_password(password)
            user.save()

        return user


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['user']

        help_texts = {
            'github': "Enter your github profile link",
            'linkedIn': "Enter your LinkedIn profile link",
            'facebook': "Enter Your Facebook profile link",
        }

    def clean_github(self):
        link = self.cleaned_data.get('github')
        return link

    def clean_linkedIn(self):
        link = self.cleaned_data.get('linkedIn')
        return link

    def clean_facebook(self):
        link = self.cleaned_data.get('facebook')
        return link


class Testing(forms.ModelForm):
    class Meta:
        model = UserOnlineJudge
        fields = ['name', 'link']


TestForm = inlineformset_factory(Link, UserOnlineJudge, form=Testing, extra=1, can_delete=False)


