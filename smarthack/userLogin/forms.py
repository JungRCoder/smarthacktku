# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from userLogin.models import UserProfile


class UserForm(forms.ModelForm):
    username = forms.CharField(label="帳號")
    password = forms.CharField(widget=forms.PasswordInput(), label='密碼')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='確認密碼')
    email = forms.CharField(widget=forms.EmailInput(), label="電子信箱", max_length=75,)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password!=password2:
            raise forms.ValidationError('密碼不相符')
        return password2

class UserProfileForm(forms.ModelForm):
    fullName = forms.CharField(max_length=128, label='姓名')

    class Meta:
        model = UserProfile
        fields = ('fullName', )


class EditUserForm(forms.ModelForm):
    username = forms.CharField(label="帳號")
    email = forms.CharField(widget=forms.EmailInput(), label="電子信箱", max_length=75,)

    class Meta:
        model = User
        fields = ('username', 'email')
        
class ForgetForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(), label="電子信箱", max_length=75,)

    class Meta:
        model = User
        fields = ('email',)