from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
def base(request):
    return render(request,'landing_page.html')

def no_permission(request):
    return HttpResponse('You have no permission')
