from django.shortcuts import render
from django.http import JsonResponse
from .models import Voto

# Create your views here.
def votos_list(request):
    votos = Voto.objects.all().order_by('-data')

    data = {"results": list(votos.values())}
    return JsonResponse(data)
