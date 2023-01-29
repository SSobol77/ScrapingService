from datetime import datetime

from django.shortcuts import render
from datetime import datetime
from zoneinfo import ZoneInfo

def home(request):
    date = datetime.now(ZoneInfo("America/New_York"))
    name = 'Serg'
    _context = {'date':date,'name':name}
    return render(request, 'home.html',_context)
