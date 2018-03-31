#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from threading import Thread
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from eatTogether.forms import *
from main.models import *
from userLogin.views import checkVerify_required
from django.forms.utils import ErrorList


# Create your views here.
class ErrorMessage(ErrorList):
    def __str__(self):
        return ', '.join([e for e in self])
    
@login_required
@checkVerify_required
def eating(request):
    if request.method=='GET':
        now = datetime.datetime.now()
        print('55555')
        context = {'now':now}
        return render(request, 'eatTogether/eating.html', context)
    

@login_required
@checkVerify_required
def invite(request):
    if request.method=='GET':
        now = datetime.datetime.now()  
        form = InviteForm()
        context = {'now':now, 'inviteForm':form}
        return render(request, 'eatTogether/invite.html', context)
    
    title = request.POST.get('title')
    inviteForm = InviteForm(data=request.POST, error_class=ErrorMessage)
    context = {'inviteForm':inviteForm}
    if not inviteForm.is_valid():
            return render(request, 'eatTogether/invite.html', context)
    inviteForm = inviteForm.save(commit=False)
    inviteForm.save()
    
    print(title)
    invite = Invite.objects.get(title=title)
    context = {'invite':invite}
    return render(request, 'eatTogether/show.html', context)
    