from .models import Load

def filter_by_load(querySet):
    load = request.GET.__getitem__("load").lower()
    load = Load.objects.get(load=load)
    querySet = querySet.filter(load__exact=load.id)
    return querySet