from django.urls import path
from . import views

urlpatterns = [
    path('run-rnascape/', views.run_rnascape, name='run_rnascape'),
    path('run-regen_plot/', views.run_regen_plot, name='run_regen_plot'),
    path('get-npz-file/', views.get_npz_file, name='get_npz_file'),
    path('get-log-file/', views.get_log_file, name='get_log_file'),
]