import datetime
from calendar import monthrange, weekday
from .models import KwhTotal
from .serializers import TotalKwhSerializer

from django.db.models.aggregates import Sum

from api import serializers

def por_dia_e_mes_e_ano(querySet):
    
    today = datetime.datetime.today()
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
    return


def por_dia_do_mes(querySet, month):
    today = datetime.datetime.today()
    last_day_of_month = monthrange(today.year, month)[1]

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
    return serializer


def por_dia_da_semana(querySet, week):
    today = datetime.datetime.today()
    text_weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]
    
    querySet = querySet.filter(timestamp__week=week)

    # week_day: 0 -> Domingo e 6 -> Sábado
    week_day = int(weekday(today.year, today.month, today.day))
    first_day_of_week = today.day - week_day

    foo = []

    i = -1
    for day in range(first_day_of_week, first_day_of_week + 7):
        i += 1
        qs = querySet.filter(
            timestamp__day=day
        ).aggregate(
            Sum("kwh")
        )

        total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{text_weekdays[i]}")
        
        if total_kwh.kwh_sum == None:
            total_kwh.kwh_sum = 0.0
        foo.append(total_kwh)

    serializer = TotalKwhSerializer(foo, many=True)
    return serializer


def por_hora_de_um_dia(querySet, day):
    today = datetime.datetime.today()
    print("\n ----- Day -----\n")
    # Filtra o conjunto querySet e retorna um subconjunto
    # divido em horas [00, 01, ..., 22, 23], onde cada hora
    # está associada à potência total consumida em seu 
    # período
    querySet = querySet.filter(timestamp__day=day)

    foo = []
    
    # Realizar a sofa, a fim de obter o total consumido
    # em cada hora do dia. 
    for hour in range(0, 24):
        qs = querySet.filter(
            timestamp__hour=hour
        ).aggregate(
             Sum("kwh")
        )
        # Guarda as informações no modelo KwhTotal
        total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{hour}h")
        if total_kwh.kwh_sum == None:
            total_kwh.kwh_sum = 0.0
        foo.append(total_kwh)
    print(foo)

    serializer = TotalKwhSerializer(foo, many=True)
    return serializer


def por_carga_em_um_mes(querySet):
    today = datetime.datetime.today()

    querySet = querySet.filter(
        timestamp__month=today.month
    )

    print("\n\n querySet \n", querySet, "\n\n")

