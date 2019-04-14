from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
# Create your views here.
from .forms import ComposeForm
from .models import Thread
class InboxView(TemplateView):
    template_name = 'index.html'


class ThreadView(LoginRequiredMixin,FormMixin, DetailView):
    template_name = 'index.html'
    form_class = ComposeForm
    success_url = './'

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj
        
    def get_queryset(self):
        return Thread.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
