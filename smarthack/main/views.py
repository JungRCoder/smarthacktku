#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import datetime
from main.models import *
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from threading import Thread
import time
from userLogin.views import checkVerify_required


# Create your views here.


@login_required
@checkVerify_required
def main(request):
    if request.method=='GET':
        now = datetime.datetime.now()

        context = {'now':now}
        return render(request, 'main/main.html', context)
    
@login_required
@checkVerify_required
def wakeup(request):
    if request.method=='GET':
        now = datetime.datetime.now()
        print('999999')
        context = {'now':now}
        return render(request, 'main/wakeup.html', context)
