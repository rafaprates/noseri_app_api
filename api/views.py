import datetime
from datetime import date
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api import serializers




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView

from rest_framework.decorators import api_view

from calendar import monthrange, weekday

from . import aggregators
from .utils import get_date_range


from api.serializers import KwhSerializer, ReaisSerializer, TotalByLoadSerializer, TotalKwhSerializer
from api.models import KwhTotal, Load, Kwh, Total_by_Load

def api_welcome_page(request):
    return HttpResponse("<h1> Bem-vindo(a) - NOSERI api </h1>")


# List GET and POST methods as accepted for this route.
@api_view(['GET', 'POST'])
def ListAndCreateKwh(request, user):

    user = User.objects.get(username=user)
    today = datetime.date.today()

    if request.method == 'GET':
        # Filtra por usuário. 
        querySet = Kwh.objects.all().filter(user=user.id)

        if request.GET.__contains__("debug"):
            pass
            

        if request.GET.__contains__("load"):
            # Filtra o conjunto de dados, retirando todas as instâncias
            # em que load não ocorre.
            load = request.GET.__getitem__("load").lower()
            load = Load.objects.get(load=load)
            querySet = querySet.filter(load__exact=load.id)


        if request.GET.__contains__("ti"):
            # Filtra o conjunto de dados, retornando um subconjunto
            # onde, em todas as instâncias, timestamp >= ti
            inferior_limit_date = request.GET.__getitem__("ti")
            print(inferior_limit_date)
            date = inferior_limit_date.split("-")
            init_year, init_month, init_day = int(date[0]), int(date[1]), int(date[2])
            querySet = querySet.filter(timestamp__date__gte=datetime.date(init_year, init_month, init_day))


        if request.GET.__contains__("tf"):
            # Filtra o conjunto de dados, retornando um subconjunto
            # onde, em todas as instâncias, timestamp <= tf
            superior_date_limit = request.GET.__getitem__("tf")
            date = superior_date_limit.split("-")
            final_year, final_month, final_day = int(date[0]), int(date[1]), int(date[2])
            querySet = querySet.filter(timestamp__date__lte=datetime.date(final_year, final_month, final_day))

        if request.GET.__contains__("unidade"):
            print("\n\nANTES: querySet\n", querySet, "\n\n")
            unidade = request.GET.__getitem__("unidade")
            print("EM REAIS")
            if unidade == "reais":
                for q in querySet:
                    print(q)
                    q = q.emReais()
                    print(q)

            print("\n\nDEPOIS querySet\n", querySet, "\n\n")

 
        if request.GET.__contains__("fixedPeriod"):
            # Retorna um subconjunto filtrado por um período de tempo
            # Os períodos de tempos suportados são: day, week & month.
            period = request.GET.__getitem__("fixedPeriod")

            if period == "day":
                day = today.day
                serializer = aggregators.por_hora_de_um_dia(querySet, day)
                return Response(serializer.data) 

            elif period == "week":
                week = today.isocalendar().week
                print("\n\nweek querySet\n", querySet, "\n\n")
                serializer = aggregators.por_dia_da_semana(querySet, week)
                print(serializer.data)
                return Response(serializer.data)

            elif period == "month":
                serializer = aggregators.por_dia_do_mes(querySet, today.month)
                return Response(serializer.data)

            elif period == "undefined":
                #ti = datetime.date(init_year, init_month, init_day)
                #tf = datetime.date(final_year, final_month, final_day)
                start_dt = datetime.date(init_year, init_month, init_day)
                end_dt =  datetime.date(final_year, final_month, final_day)

                date_range = get_date_range(start_dt, end_dt)
                #for dt in date_range:
                    #print(dt.strftime("%Y-%m-%d"))

                foo = []
                for dt in date_range:
                    qs = querySet.filter(
                        timestamp__month=dt.month
                    ).filter(
                        timestamp__day=dt.day
                    ).aggregate(
                        Sum("kwh")
                    )

                    print(qs)

                    total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{dt.day}/{dt.month}/{dt.year}")
                    if total_kwh.kwh_sum != None:
                        #total_kwh.kwh_sum = 0.0
                        foo.append(total_kwh)
                serializer = TotalKwhSerializer(foo, many=True)
                return Response(serializer.data)


        if request.GET.__contains__("type"):
            if request.GET.__getitem__("type") == "circular":
                loads = Load.objects.all()
                totals_by_load = []
                for load in loads:
                    print(load)
                    qs = querySet.filter(
                        load__exact=load.id
                    ).aggregate(
                        Sum("kwh")
                    )

                    print("\n\n qs", qs, "\n\n")
                    total_by_load = Total_by_Load(load_name=load.load, kwh_sum=qs["kwh__sum"])
                    totals_by_load.append(total_by_load)
                print(totals_by_load)
            serializer = TotalByLoadSerializer(totals_by_load, many=True)
            return Response(serializer.data)


        if request.GET.__contains__("unidade"):
            unidade = request.GET.__getitem__("unidade")
            if unidade == "reais":
                for q in querySet:
                    q = q.emReais()
                    

        serializer = KwhSerializer(querySet, many=True)
        return Response(serializer.data)
      

    if request.method == 'POST':
        load = Load.objects.get(load=request.POST.__getitem__('load').lower())
        kwh = request.POST.__getitem__('kwh')
        Kwh.objects.create(user=user, load=load, kwh=kwh)
        return Response(status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def ListAndCreateLoad(request):

    if request.method == 'POST':
        load = request.POST.__getitem__('load').lower()
        Load.objects.create(load=load)
        return Response(status.HTTP_201_CREATED)