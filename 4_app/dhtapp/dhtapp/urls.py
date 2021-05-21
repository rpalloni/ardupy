from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', views.store_data, name='store'),
    path('fetch/', views.fetch_data, name='fetch'),
    path('plot/', views.chart_data, name='plot'),
    path('view/', views.view_plot, name='view'),
]
