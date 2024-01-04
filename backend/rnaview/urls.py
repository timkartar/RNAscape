from django.urls import path
from . import views

urlpatterns = [
    path('run-rnaview/', views.run_rnaview, name='run_rnaview'),
    path('run-regen_plot/', views.run_regen_plot, name='run_regen_plot'),
    path('get-npz-file/', views.get_npz_file, name='get_npz_file'),
]