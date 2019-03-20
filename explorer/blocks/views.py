from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import BlockModel
from smdataxs.models import Smdatax

def block_detailed_view(request, block_hash):
    block = BlockModel.objects.get(block_hash=block_hash)
    smdatax = Smdatax.objects.filter(host_block=block_hash)
    info = {
        'info_blocks': block, 
        'info_datas': smdatax
    }
    return render(request, "block/detail.html", info)

def search_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('search', None)
        try:
            if user_input.startswith("0000"):
                block = BlockModel.objects.get(block_hash=user_input)
                smdatax = Smdatax.objects.filter(host_block=user_input)
                info = {
                    'info_blocks': block,
                    'info_datas': smdatax
                }
                return render(request, "search.html", info)
            else:
                return render(request, 'home.html')
        except ObjectDoesNotExist:
            return render(request, 'home.html')