from copy import deepcopy
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from askapp.views import ThreadMixin
from askapp.models import ThreadLike, Tag


@method_decorator(csrf_exempt, name='dispatch')
class AddArticle(PermissionRequiredMixin, ThreadMixin, CreateView):
    permission_required = 'askapp.add_thread'
    raise_exception = True

    def filter_tags(self, tags):
        if not tags:
            return None
        db_tags = Tag.objects.get_queryset()
        db_tags = {t.slug: t.id for t in db_tags}
        result = [db_tags[t] for t in tags if t in db_tags]
        return result

    def get_form_kwargs(self):
        kwargs = deepcopy(super().get_form_kwargs())
        tag_names = self.request.POST.getlist('tags')
        if tag_names:
            tags = self.filter_tags(tag_names)
            if tags:
                kwargs['data']['tags'] = tags
            else:
                del kwargs['data']['tags']
        return kwargs

    def form_invalid(self, form):
        response = json.dumps(form.errors)
        result = HttpResponse(response, status=400, content_type='application/json')
        return result

    def form_valid(self, form):
        super().form_valid(form)
        points = int(self.request.POST.get('points') or 0)
        if points:
            tl = ThreadLike(thread=form.instance, user=self.request.user, points=points)
            tl.save()
        result = HttpResponse(b'{"status": "OK"}', status=200, content_type='application/json')
        return result
