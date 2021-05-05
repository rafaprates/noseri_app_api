from django.contrib.auth.models import User
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt



from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import KwhSerializer
from api.models import Load, Kwh



@api_view(['GET', 'POST'])
def ListAndCreateKwh(request, user):
    user = User.objects.get(username=user)

    if request.method == 'GET':
        # Busca o usuário passado através da URL
        user = User.objects.get(username=user)

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
