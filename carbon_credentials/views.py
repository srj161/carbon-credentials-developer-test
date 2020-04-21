from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect

from . import forms
from . import csv_uploader


def index(request):
    return render(request, 'index.html')


class UploadView(View):
    form = forms.UploadForm
    template = 'upload.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'form': self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            csv_uploader.upload(
                request.FILES['upload_file'], form.cleaned_data['file_type'])

        return render(request, self.template, {'form': form})


def explore(request):
    pass


def visualise(request):
    pass
