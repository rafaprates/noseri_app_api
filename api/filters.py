from .models import Load
import datetime

def filter_by_load(querySet, load):
    load = Load.objects.get(load=load)
    querySet = querySet.filter(load__exact=load.id)
    return querySet

def filter_by_time_gt(querySet, ti):
    date = ti.split("-")
    init_year, init_month, init_day = int(date[0]), int(date[1]), int(date[2])
    querySet = querySet.filter(
        timestamp__date__gte=datetime.date(
            init_year, init_month, init_day
        )
    )
    return querySet

def filter_by_time_lt(querySet, tf):
    date = tf.split("-")
    final_year, final_month, final_day = int(date[0]), int(date[1]), int(date[2])
    querySet = querySet.filter(
        timestamp__date__lte=datetime.date(
            final_year, final_month, final_day
        )
    )
    return querySet