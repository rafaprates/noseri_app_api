import datetime
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView

from rest_framework.decorators import api_view


from api.serializers import KwhSerializer
from api.models import Load, Kwh

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

        querySet = Kwh.objects.all()

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
            if period == "day":
                today = datetime.date.today()
                querySet = querySet.filter(timestamp__date__gte=datetime.date(today.year, today.month, today.day))
                querySet = querySet.filter(timestamp__date__lte=datetime.date(today.year, today.month, today.day))
            elif period == "week":
                this_week = datetime.date.today()
                querySet = querySet.filter(timestamp__date__gte=datetime.date(this_week.year, this_week.month, this_week.day))
                querySet = querySet.filter(timestamp__date__lte=datetime.date(this_week.year, this_week.month, this_week.day))
            else:
                pass

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