from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from blocks.models import BlockModel

def home_view(request, *args, **kwargs):
    try:
        block = BlockModel.objects.all()
        info = {
            'blocks': block
            }
        return render(request, "home.html", info)
    except ObjectDoesNotExist:
        return render(request, "home.html", {})

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})
