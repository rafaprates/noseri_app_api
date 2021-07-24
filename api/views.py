import datetime
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


from api.serializers import KwhSerializer, ReaisSerializer, TotalKwhSerializer
from api.models import KwhTotal, Load, Kwh

def api_welcome_page(request):
    return HttpResponse("<h1> Bem-vindo(a) - NOSERI api </h1>")


# List GET and POST methods as accepted for this route.
@api_view(['GET', 'POST'])
def ListAndCreateKwh(request, user):
    """
    Lists and creates rows of Kwh table for spcified user. 
    It allows filtering. The filters are passed by the url. The filters are:
        * String <load> for a specific load;
        * String <time_delta> for a specific period of time.
    """
    
    user = User.objects.get(username=user)

    if request.method == 'GET':
        # Busca o usuário passado através da URL
        user = User.objects.get(username=user)

        querySet = Kwh.objects.all().filter(user=user.id)

        if request.GET.__contains__("debug"):
            # O dia de hoje
            today = datetime.date.today()

            # O total de dias deste mês
            total_days_in_month = monthrange(today.year, today.month)[1]

            # Todos os registros para este mês
            print("\nTodos os registros para o mes:")
            obj = Kwh.objects.filter(user=user.id).filter(timestamp__month=today.month)
            print(obj, "\n")

            # Objeto vázio que será preenchido com valores para cada dia.
            print("\nObjeto Vazio:")
            obj_vaz = Kwh.objects.none()
            print(obj_vaz, "\n")

            qs = Kwh.objects.all().filter(
                user=user.id
            ).filter(
                timestamp__month=today.month
            ).aggregate(
                Sum("kwh")
            )

            print("qs--->", qs)
            print(qs)
            print("qs['kwh__sum']", qs["kwh__sum"])


            total_kwh = KwhTotal(kwh_sum=3.14, data="aaaaa")
            print(total_kwh.data)
            print("total_kwh:", total_kwh)
            serializer = TotalKwhSerializer(total_kwh)
            print("SERLIAER", serializer.data)
            return Response(serializer.data)
            obj_2 = Kwh(user=user, load=Load.objects.get(pk=1), kwh=qs["kwh__sum"])
            print("obj_2:", obj_2)
            serializer = KwhSerializer(obj_2)
            print(serializer.data)
            print(obj_2)
            #serializer = TotalKwhPorDiaSerializer("kwh_total", qs["kwh__sum"])
            #print(serializer.data)
            #print("SERLIAZER--->", serializer.data)
            return Response(serializer.data)

            for day in range(total_days_in_month):
                cons = Kwh.objects.all().filter(user=user.id).filter(timestamp__month=today.month).filter(timestamp__day=day)
                print("1:", cons)
                cons = Kwh.objects.filter(user=user.id).filter(timestamp__month=today.month).filter(timestamp__day=day).aggregate(Sum("kwh"))
                print("2: cons", cons)
                print(cons)
                for o in cons:
                    print(o)
                    print(o.kwh, o.timestamp.day)
                    # somar os que tem dias iguais


            serializer = KwhSerializer(obj, many=True)
            return Response(serializer.data)

        if request.GET.__contains__("load"):
            load = request.GET.__getitem__("load").lower()
            load = Load.objects.get(load=load)
            querySet = querySet.filter(load__exact=load.id)

        if request.GET.__contains__("ti"):
            timeInit = request.GET.__getitem__("ti")
            date = timeInit.split("-")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            querySet = querySet.filter(timestamp__date__gte=datetime.date(year, month, day))

        if request.GET.__contains__("tf"):
            timeFinal = request.GET.__getitem__("tf")
            date = timeFinal.split("-")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            querySet = querySet.filter(timestamp__date__lte=datetime.date(year, month, day))

        if request.GET.__contains__("fixedPeriod"):
            period = request.GET.__getitem__("fixedPeriod")
            today = datetime.date.today()
            print(today.day)

            if period == "day":
                print("\n ----- Day -----\n")
                querySet = querySet.filter(
                    user=User.objects.get(username=user)
                ).filter(
                    timestamp__day=today.day
                )

                last_day_of_month = monthrange(today.year, today.month)[1]

                foo = []
                for hour in range(0, 24):
                    qs = querySet.filter(
                        timestamp__hour=hour
                    ).aggregate(
                        Sum("kwh")
                    )
                    total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{hour}h")
                    if total_kwh.kwh_sum == None:
                        total_kwh.kwh_sum = 0.0
                    foo.append(total_kwh)



                serializer = TotalKwhSerializer(foo, many=True)
                print("serializer:", serializer.data)
                return Response(serializer.data)


            elif period == "week":
                print("\n ----- Week -----\n")
                querySet = querySet.filter(
                    user=User.objects.get(username=user)
                ).filter(
                    timestamp__week=today.isocalendar().week
                )

                week_day = int(weekday(today.year, today.month, today.day))
                print("week_day", week_day)
                print("today", today.day)
                first_day_of_week = today.day - week_day
                print("first_day_of_week", first_day_of_week)

                foo = []

                i = -1
                for day in range(first_day_of_week, first_day_of_week + 7):
                    i += 1
                    qs = querySet.filter(
                        timestamp__day=day
                    ).aggregate(
                        Sum("kwh")
                    )

                    days = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]

                    total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{days[i]}")
                    if total_kwh.kwh_sum == None:
                        total_kwh.kwh_sum = 0.0
                    foo.append(total_kwh)

                serializer = TotalKwhSerializer(foo, many=True)
                print("serializer:", serializer.data)
                return Response(serializer.data)

            elif period == "month":
                print("\n ----- Month -----\n")
                querySet = querySet.filter(
                    user=User.objects.get(username=user)
                ).filter(
                    timestamp__month=today.month
                )

                print("querySet:\n", querySet)

                last_day_of_month = monthrange(today.year, today.month)[1]

                foo = []
                for day in range(1, last_day_of_month):
                    qs = querySet.filter(
                        timestamp__day=day
                    ).aggregate(
                        Sum("kwh")
                    )
                    total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{day}")
                    if total_kwh.kwh_sum == None:
                        total_kwh.kwh_sum = 0.0
                    foo.append(total_kwh)
                serializer = TotalKwhSerializer(foo, many=True)
                return Response(serializer.data)



        if request.GET.__contains__("type"):
            if request.GET.__getitem__("type") == "circular":
                print("#####################")

                today = datetime.datetime.today()
                last_day_of_month = monthrange(today.year, today.month)[1]

                foo = []

                loads = Load.objects.all()
                loads_list = []
                for load in loads:
                    loads_list.append(load.load)

                print("loads_list:", loads_list)
                print("loads:", loads)

                for day in range(1, last_day_of_month):
                    qs = querySet.filter(
                        timestamp__day=day
                    ).filter(
                        
                    ).aggregate(
                        Sum("kwh")
                    )
                    total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{day}")
                    if total_kwh.kwh_sum == None:
                        total_kwh.kwh_sum = 0.0
                    foo.append(total_kwh)
                serializer = TotalKwhSerializer(foo, many=True)
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