from django.urls import path
from . import views

urlpatterns = [
    path('run-rnaview/', views.run_rnaview, name='run_rnaview'),
]