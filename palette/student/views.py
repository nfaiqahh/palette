from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #context = {
    # 'what': what
    # }
    #return render(request, 'mainmenu.html', context)
    return render(request, 'mainmenu.html')