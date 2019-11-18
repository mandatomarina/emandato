# Create your views here.
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from .models import Conteudo
from .utils import ConteudoCalendar


def calendar(request, year=2019, month=11):
  comunic = Conteudo.objects.order_by('data').filter(
    data__year=year, data__month=month
  )
  cal = ConteudoCalendar(comunic).formatmonth(year, month)
  return render_to_response('calendar.html', {'calendar': mark_safe(cal),})