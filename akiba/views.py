from django.shortcuts import render_to_response
from django.views.generic import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
            'user': request.user,
        }
        return render_to_response('index.html', context)
