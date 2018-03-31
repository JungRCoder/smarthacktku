# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from eatTogether.models import *

defaultError = {
    'required': '必填',
    'unique': '已存在',
    #'invalid', ...,
}


class InviteForm(forms.ModelForm):
    title = forms.CharField(label="Title", error_messages=defaultError, required=True)
    day = forms.DateTimeField(label="Date", error_messages=defaultError, required=True)
    place = forms.CharField(label="Place", error_messages=defaultError, required=True)
    count = forms.CharField(label="Count", error_messages=defaultError, required=True)
    pw = forms.CharField(label="PW", error_messages=defaultError, required=True)
    comment = forms.CharField(label="Comment", error_messages=defaultError, required=True)
    
    class Meta:
        model = Invite
        fields = ('title', 'day', 'place', 'count', 'pw', 'comment',)