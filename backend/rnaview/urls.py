from django.urls import path
from . import views

urlpatterns = [
    path('run-rnaview/', views.run_rnaview, name='run_rnaview'),
    path('run-regen_labels/', views.run_regen_labels, name='run_regen_labels'),
    path('test-get/', views.test_get, name='test_get'),
]