from datetime import timedelta, date

from datetime import timedelta, date

def get_date_range(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def calcular_kwh_em_reais(kwh):
    TE = 0.68350
    em_reais = kwh * TE
    return round(em_reais, 2)


