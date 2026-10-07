from django.urls import path
from . import views

urlpatterns = [
    path('calcular/', views.calcular_imc, name='calcular-imc'),
    path('historico/', views.historico_imc, name='historico-imc'),
    path('historico/limpar/', views.limpar_historico, name='limpar-historico'),
]
