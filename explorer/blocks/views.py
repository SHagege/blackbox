from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import BlockModel

def block_detailed_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('search', None)
        try:
            if user_input.startswith("0000"):
                block = BlockModel.objects.get(block_hash=user_input)
                info = {
                    'height': block.block_height
                }
            else:
                block = BlockModel.objects.get(id=user_input)
                info = {
                    'hash': block.block_hash
                }
            return render(request, "block/detail.html", info)
        except ObjectDoesNotExist:
            return render(request, 'home.html') 