from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views


urlpatterns = [
    #api/username/kwh &load=geladeira &from=DataInicial &until=DataFinal
    #path('<str:user>/kwh', views.KwhList.as_view()),
    path('<str:user>/kwh', views.ListAndCreateKwh),
    path('', views.api_welcome_page),
]

urlpatterns = format_suffix_patterns(urlpatterns)