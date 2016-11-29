# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging

from django.shortcuts import render_to_response
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

testVariable = os.environ.get('TEST_VARIABLE')


def index(request):
    #logging.debug("this is what you get: ", testVariable)
    logging.debug('This is a debug message')

    return HttpResponse("Hello, world. This is the beginning of something new for {}.".format(testVariable))

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, world. This is something new for {}.".format(testVariable))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        c = {}
        c.update(csrf(request))

        return render_to_response('login.html', c)

class AuthView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/loggedin')
        else:
            return HttpResponseRedirect('/invalid')

class LoggedInView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('you are logged in')