import datetime
import requests
import json
import time as ti
import pytz
from .models import NIFTY,FINNIFTY,BANKNIFTY
j=0
IST = pytz.timezone('Asia/Kolkata')

def getdata(name):


    time=datetime.datetime.now(IST)
    if time.hour==15 and time.minute>30:
        return name.objects.all()
    elif time.hour>=16:
        return name.objects.all()
    elif time.hour==9 and time.minute<15:
        return name.objects.all()
    elif time.hour<9:
        return name.objects.all()
    else:
        
        global j
        if name==NIFTY:
            query="NIFTY"
        elif name==FINNIFTY:
            query="FINNIFTY"
        elif name==BANKNIFTY:
            query="BANKNIFTY"
        print(query)
        url=f"https://www.nseindia.com/api/option-chain-indices?symbol={query}"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response=requests.get(url,headers=headers)
        ti.sleep(0.2)
        if response.status_code==200:
            datas=json.loads(response.text)
            datas=datas["filtered"]["data"]
            if not name.objects.first():
                for data in datas:
                    db=name(CopenInterest=data["CE"]["openInterest"]\
                        ,CchangeinOpenInterest=data["CE"]["changeinOpenInterest"]\
                        ,CtotalTradedVolume=data["CE"]["totalTradedVolume"]\
                        ,CimpliedVolatility=data["CE"]["impliedVolatility"]\
                        ,ClastPrice=data["CE"]["lastPrice"]\
                        ,Cchange=data["CE"]["change"]\
                        ,CbidQty=data["CE"]["bidQty"]\
                        ,Cbidprice=data["CE"]["bidprice"]\
                        ,CaskPrice=data["CE"]["askPrice"]\
                        ,CaskQty=data["CE"]["askQty"]\
                        ,strikePrice=data["strikePrice"]\
                        ,PbidQty=data["PE"]["bidQty"]\
                        ,Pbidprice=data["PE"]["bidprice"]\
                        ,PaskPrice=data["PE"]["askPrice"]\
                        ,PaskQty=data["PE"]["askQty"]\
                        ,Pchange=data["PE"]["change"]\
                        ,PlastPrice=data["PE"]["lastPrice"]\
                        ,PimpliedVolatility=data["PE"]["impliedVolatility"]\
                        ,PtotalTradedVolume=data["PE"]["totalTradedVolume"]\
                        ,PchangeinOpenInterest=data["PE"]["changeinOpenInterest"]\
                        ,PopenInterest=data["PE"]["openInterest"]\
                        
                        )
                    db.save()
            else:
                first=name.objects.first()
                if first.starttime.hour!=time.hour or abs(first.starttime.minute-time.minute)>3:
                    i=0
                    for item in name.objects.all():
                        item.starttime=time
                        item.CopenInterest=datas[i]["CE"]["openInterest"]
                        item.CchangeinOpenInterest=datas[i]["CE"]["changeinOpenInterest"]
                        item.CtotalTradedVolume=datas[i]["CE"]["totalTradedVolume"]
                        item.CimpliedVolatility=datas[i]["CE"]["impliedVolatility"]
                        item.ClastPrice=datas[i]["CE"]["lastPrice"]
                        item.Cchange=datas[i]["CE"]["change"]
                        item.CbidQty=datas[i]["CE"]["bidQty"]
                        item.Cbidprice=datas[i]["CE"]["bidprice"]
                        item.CaskPrice=datas[i]["CE"]["askPrice"]
                        item.CaskQty=datas[i]["CE"]["askQty"]
                        item.strikePrice=datas[i]["strikePrice"]
                        item.PbidQty=datas[i]["PE"]["bidQty"]
                        item.Pbidprice=datas[i]["PE"]["bidprice"]
                        item.PaskPrice=datas[i]["PE"]["askPrice"]
                        item.PaskQty=datas[i]["PE"]["askQty"]
                        item.Pchange=datas[i]["PE"]["change"]
                        item.PlastPrice=datas[i]["PE"]["lastPrice"]
                        item.PimpliedVolatility=datas[i]["PE"]["impliedVolatility"]
                        item.PtotalTradedVolume=datas[i]["PE"]["totalTradedVolume"]
                        item.PchangeinOpenInterest=datas[i]["PE"]["changeinOpenInterest"]
                        item.PopenInterest=datas[i]["PE"]["openInterest"]
                        item.save()
                        i+=1

                    print(name.objects.first().starttime)
                    return name.objects.all()
                else:
                    return name.objects.all()
        elif response.status_code==401:
            return name.objects.all()
        else:
            if j==5:
                return name.objects.all()
            ti.sleep(0.1)
            print(j)
            j+=1
            getdata(name)