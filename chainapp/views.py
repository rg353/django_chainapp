from django.shortcuts import render
from .models import NIFTY,FINNIFTY,BANKNIFTY
from . import getinfo
import time
# Create your views here.

def home(request):
    if request.GET.get("q"):
        param=request.GET.get("q")
        if param=="NIFTY":
            datas=getinfo.getdata(NIFTY)
        elif param=="FINNIFTY":
            datas=getinfo.getdata(FINNIFTY)
        elif param=="BANKNIFTY":
            datas=getinfo.getdata(BANKNIFTY)
        else:
            datas=getinfo.getdata(NIFTY)
    else:
        datas=getinfo.getdata(NIFTY)
    return render(request,"chainapp/home.html",context={"datas":datas})