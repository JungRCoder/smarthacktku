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
def start(request):
    if request.method=='GET':
        now = datetime.datetime.now()
        context = {'now':now}
        return render(request, 'startEat/start.html', context)

@login_required
@checkVerify_required
def challenge(request):
    if request.method=='GET':
        now = datetime.datetime.now()
        context = {'now':now}
        return render(request, 'startEat/challenge.html', context)

@login_required
@checkVerify_required
def game(request):
    if request.method=='GET':
        now = datetime.datetime.now()
        context = {'now':now}
        return render(request, 'startEat/game.html', context)

@login_required
@checkVerify_required
def end(request):
    if request.method=='GET':
        now = datetime.datetime.now()
        context = {'now':now}
        return render(request, 'startEat/end.html', context)