from django.shortcuts import render
from .models import Consumerprofile
from django.contrib.auth.decorators import login_required
from . forms import ProfileForm
from django.contrib.auth.models import User

# Create your views here.

@login_required
def conprofile(request):
    if request.method == 'GET':
        profile = Consumerprofile.objects.filter(user=request.user)
        return render(request,'consumer/conprofile.html',{'profile':profile,'form':ProfileForm})
        #return render(request,'consumer/conprofile.html',{'profile':'profile','user':request.user.username,'form':ProfileForm})
    else:
        pass


def editProfile(request,user_pk):
    profile = Consumerprofile.objects.filter(user=request.user)
    return render(request,'consumer/conprofile.html',{'profile':profile,'form':ProfileForm,'user_pk':user_pk})