import datetime
from calendar import monthrange, weekday
from .models import KwhTotal
from .serializers import TotalKwhSerializer

from django.db.models.aggregates import Sum

from api import serializers
from api import utils
from api.models import Load, KwhTotal, Total_by_Load

def por_dia_e_mes_e_ano(querySet, ti, tf):
    
    date = ti.split("-")
    init_year, init_month, init_day = int(date[0]), int(date[1]), int(date[2])
    date = tf.split("-")
    final_year, final_month, final_day = int(date[0]), int(date[1]), int(date[2])
    start_dt = datetime.date(init_year, init_month, init_day)
    end_dt =  datetime.date(final_year, final_month, final_day)

    date_range = utils.get_date_range(start_dt, end_dt)
    #for dt in date_range:
        #print(dt.strftime("%Y-%m-%d"))

    aggregated_values = []
    for dt in date_range:
        qs = querySet.filter(
            timestamp__month=dt.month
        ).filter(
            timestamp__day=dt.day
        ).aggregate(
            Sum("kwh")
        )

        total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{dt.day}/{dt.month}/{dt.year}")
        if total_kwh.kwh_sum != None:
            aggregated_values.append(total_kwh)
    return aggregated_values


def por_dias_de_um_mes(querySet, month):
    """
    Agrega os valores para cada dia de um mês.

    Args: 
        querySet: subconjunto de dados.
        month: mês que contém os dias a serem agregados.

    Returns:

    """

    today = datetime.datetime.today()
    last_day_of_month = monthrange(today.year, month)[1]
    aggregated_values = []
    print(aggregated_values)
    
    for day in range(1, last_day_of_month):
        qs = querySet.filter(
            timestamp__day=day
        ).filter(
            timestamp__month=month
        ).aggregate(
            Sum("kwh")
        )

        total_kwh = KwhTotal(
            kwh_sum=qs["kwh__sum"], 
            data=f"{day}"
        )

        if total_kwh.kwh_sum == None:
            total_kwh.kwh_sum = 0.0
        aggregated_values.append(total_kwh)
    
    return aggregated_values


def por_dias_de_uma_semana(querySet, week):
    """
    Agrega os valores para cada dia de uma mês.

    Args: 
        querySet: subconjunto de dados filtrado para um usuário.
        week: semana os dias a serem agregados.

    Returns:
        aggregated_values: lista contendo os valores
        agregados.
    """

    today = datetime.datetime.today()
    text_weekdays = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    aggregated_values = []
    
    querySet = querySet.filter(timestamp__week=week)

    # Monday = 0 and Sunday = 6
    week_day = int(weekday(today.year, today.month, today.day))

    # Extrair o primeiro dia da semana
    first_day_of_week = today.day - week_day

    i = 0
    for day in range(first_day_of_week, first_day_of_week + 7):
        qs = querySet.filter(
            timestamp__day=day
        ).aggregate(
            Sum("kwh")
        )

        total_kwh = KwhTotal(
            kwh_sum=qs["kwh__sum"], 
            data=f"{text_weekdays[i]}"
        )
        
        if total_kwh.kwh_sum == None:
            total_kwh.kwh_sum = 0.0
        aggregated_values.append(total_kwh)
        i += 1
    return aggregated_values



def por_hora_de_um_dia(querySet, day):
    """
    Agrega os valores para cada hora de um dia.

    Args: 
        querySet: subconjunto de dados.
        day: dia que contém as horas a serem agregadas.

    Returns:
        
    """
    today = datetime.datetime.today()
    #querySet = querySet.filter(timestamp__day=day)

    aggregated_values = []
    total_kwh = 0;
    
    # Realizar a soma, a fim de obter o total consumido
    # em cada hora do dia. 
    for hour in range(0, 24):
        qs = querySet.filter(
            timestamp__year=today.year
        ).filter(
            timestamp__month=today.month
        ).filter(
            timestamp__day=today.day
        ).filter(
            timestamp__hour=hour
        ).aggregate(
             Sum("kwh")
        )
        # Guarda as informações no modelo KwhTotal
        total_kwh = KwhTotal(kwh_sum=qs["kwh__sum"], data=f"{hour}h")
        if total_kwh.kwh_sum == None:
            total_kwh.kwh_sum = 0.0
        aggregated_values.append(total_kwh)

    return aggregated_values


def por_carga_em_um_mes(querySet):
    """
    Agrega os valores por carga.

    Args: 
        querySet: subconjunto de dados.
        month: mês que contém os dias a serem agregados.

    Returns:
        
    """

    today = datetime.datetime.today()
    loads = Load.objects.all()
    totals_by_load = []
    for load in loads:
        qs = querySet.filter(
            timestamp__year=today.year
        ).filter(
            timestamp__month=today.month
        ).filter(
            load__exact=load.id
        ).aggregate(
            Sum("kwh")
        )

        total_by_load = Total_by_Load(load_name=load.load, kwh_sum=qs["kwh__sum"])
        totals_by_load.append(total_by_load)
        
    return totals_by_load

def by_total_this_month(querySet):

    today = datetime.datetime.today()
    qs = querySet.filter(
        timestamp__month=today.month
    ).aggregate(
        Sum("kwh")
    )

    total_this_month = KwhTotal(kwh_sum=qs["kwh__sum"], data="aa")
    return total_this_month
