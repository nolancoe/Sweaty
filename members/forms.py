from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from core.models import user_profile
from django.contrib.auth import authenticate


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = user_profile
        fields = ('profile_pic',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = user_profile
        fields = ('email', 'username', 'gamertag', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            profile = user_profile.objects.exclude(pk=self.instance.pk).get(email=email)
        except user_profile.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % user_profile)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            profile = user_profile.objects.exclude(pk=self.instance.pk).get(username=username)
        except user_profile.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = user_profile
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountSettingsForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    gamertag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login = None
    is_superuser = None
    is_staff = None
    is_active = None
    date_joined = None


    class Meta(UserChangeForm):
        model = user_profile
        fields = ('username', 'gamertag', 'email', 'first_name', 'last_name', 'profile_pic', 'password',)


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    class Meta:
        model = user_profile
        fields = ('old_password', 'new_password1', 'new_password2')


