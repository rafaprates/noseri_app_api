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

        #TODO: checar se load foi passado.
        if not request.GET.__contains__("load"):
            querySet = Kwh.objects.filter(user__exact = user.id)
            print(querySet)
            serializer = KwhSerializer(querySet, many=True)
            return Response(serializer.data)
        

        # Busca na URL o parametro load e busca o objeto correspondente
        load = request.GET.__getitem__('load').lower()
        load = Load.objects.get(load=load)

        # Retorna todas as linhas que contem o usuário especificado no Model (tabela) Kwh
        # E dessas linhas retorna apenas aquelas que contenha a carga especificada por load
        querySet = Kwh.objects.filter(user__exact = user.id).filter(load__exact = load.id)

        # Filtro para o tsStart, tsEnd
        #start_date = request.GET.__getitem__('tsStart')
        #end_date = request.GET.__getitem__('tsEnd')
        #querySet = querySet.filter(pub_date__range=(start_date, end_date))

        serializer = KwhSerializer(querySet, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        load = Load.objects.get(load=request.POST.__getitem__('load').lower())
        kwh = request.POST.__getitem__('kwh')
        Kwh.objects.create(user=user, load=load, kwh=kwh)
        return Response(status.HTTP_201_CREATED)
