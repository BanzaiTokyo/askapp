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


from django.conf.urls import include, url
from django.contrib import admin

from akiba.views import index, HomeView, LoginView, AuthView, LoggedInView

# please continue the login tutorial
# https://www.youtube.com/watch?v=CFypO_LNmcc

urlpatterns = [
    url(regex = r'^$',
        view = HomeView.as_view(),
        name = "homepage"),

    url(regex=r'^login$',
        view= LoginView.as_view(),
        name="login"),

    url(regex=r'^auth',
        view=AuthView.as_view(),
        name="auth"),

    url(regex=r'^loggedin',
        view=LoggedInView.as_view(),
        name="loggedin"),

    url(r'^admin/', include(admin.site.urls)),
]
