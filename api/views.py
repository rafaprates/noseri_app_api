import datetime
from datetime import date
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api import serializers

#from .filters import *
from . import filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView

from rest_framework.decorators import api_view

from calendar import monthrange, weekday

from . import aggregators
from .utils import get_date_range


from api.serializers import KwhSerializer, LoadSerializer, ReaisSerializer, TotalByLoadSerializer, TotalKwhSerializer, TrackedLoadsSerializer
from api.models import KwhTotal, Load, Kwh, Total_by_Load, TrackedLoads, UserLoadAssociation

from api import utils

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

        # Filtra apenas as cargas registradas para o usuário
        foo = UserLoadAssociation.objects.all().filter(user=user.id)

        if request.GET.__contains__("debug"):
            pass
            
        # ---> Início dos filtros
        if request.GET.__contains__("load"):
            load = request.GET.__getitem__("load").lower()
            querySet = filters.filter_by_load(querySet, load)

        if request.GET.__contains__("ti"):
            ti = request.GET.__getitem__("ti")
            querySet = filters.filter_by_time_gt(querySet, ti)

        if request.GET.__contains__("tf"):
            tf = request.GET.__getitem__("tf")
            querySet = filters.filter_by_time_lt(querySet, tf)
        # <--- Fim dos filtros

        # ---> Início dos agregadores
        if request.GET.__contains__("aggregator"):
            aggregator = request.GET.__getitem__("aggregator")
            serializer = []

            if aggregator == "by_days_in_a_month":
                month = today.month
                aggregated_values = aggregators.por_dias_de_um_mes(querySet, month)
                
            if aggregator == "by_days_in_a_week":
                week = today.isocalendar().week
                aggregated_values = aggregators.por_dias_de_uma_semana(querySet, week)

            if aggregator == "by_hours_in_a_day":
                day = today.day
                aggregated_values = aggregators.por_hora_de_um_dia(querySet, day)

            if aggregator == "by_day_month_year":
                ti = request.GET.__getitem__("ti")
                tf = request.GET.__getitem__("tf")
                aggregated_values = aggregators.por_dia_e_mes_e_ano(querySet, ti, tf)

            if aggregator == "by_total_this_month":
                month = today.month
                aggregated_values = aggregators.por_total_este_mes(querySet, month)

            if aggregator == "total_this_month":
                pass

            if aggregator == "by_total_this_week":
                pass

            if aggregator == "by_total_today":
                pass

            if aggregator == "by_load_in_a_month":
                aggregated_values = aggregators.por_carga_em_um_mes(querySet)
                serializer = TotalByLoadSerializer(aggregated_values, many=True)
                return Response(serializer.data)

            # Antes de retornar, aplica-se, se solicitado, o 
            # modificador de colunas que calcula o preço da tarifa
            unidade = request.GET.__getitem__("unidade")
            if unidade == "reais":
                for val in aggregated_values:
                    val.kwh_sum = utils.calcular_kwh_em_reais(val.kwh_sum)

            serializer = TotalKwhSerializer(aggregated_values, many=True)
            return Response(serializer.data)
        # <---  Fim dos agregadores


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

    if request.method == 'GET':
        loads = Load.objects.all()
        print(loads)
        serializer = LoadSerializer(loads, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        load = request.POST.__getitem__('load').lower()
        Load.objects.create(load=load)
        return Response(status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def ListAndCreateUserLoad(request, user):

    user = User.objects.get(username=user)
    # Clean "middle man model"
    TrackedLoads.objects.all().delete()
    
    if request.method == 'GET'  :

        # 
        tracked_load_qs = UserLoadAssociation.objects.all().filter(user__id=user.id)
        values = tracked_load_qs.values("load")

        # Create a list with tracked Loads.
        tracked_loads = []

        # Register tracked Load objects.
        for load in values:
            load_id = load["load"]
            load = Load.objects.get(pk=load_id)
            tracked_loads.append(load)
            tracked_untracked_loads = TrackedLoads.objects.create(load=load, isTracked=True)

        # Register remaining Load only if not in tracked Load.
        loads = Load.objects.all()
        for load in loads:
            if load not in tracked_loads:
                print(load)
                tracked_untracked_loads = TrackedLoads.objects.create(load=load, isTracked=False)

    
        for load in TrackedLoads.objects.all():
           print(load.load, load.isTracked)

        object = TrackedLoads.objects.all()
        serializer = TrackedLoadsSerializer(object, many=True)

        return Response(serializer.data)
    
    if request.method == "POST":
        pass