"""
URL configuration for univalle_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from univalle_app.views import generar_multas_view
#from univalle_app.views import datos_articulos_por_deporte
from univalle_app import views
from django.shortcuts import render
from django.urls import path, re_path, include
from django.shortcuts import redirect

urlpatterns = [
    re_path(r'^$', lambda request: redirect('reportes', permanent=False)),
    path('admin/', admin.site.urls),

    # Vistas CRUD para Univalluno
    path('univalluno/', views.UnivallunoList.as_view(), name='univalluno-list'),
    path('univalluno/<int:pk>/', views.UnivallunoDetail.as_view(), name='univalluno-detail'),

    # Vistas CRUD para ArticuloDeportivo
    path('articulo/', views.ArticuloDeportivoList.as_view(), name='articulo-list'),
    path('articulo/<int:pk>/', views.ArticuloDeportivoDetail.as_view(), name='articulo-detail'),


    # Vistas CRUD para Prestamo
    path('prestamo/', views.PrestamoList.as_view(), name='prestamo-list'),
    path('prestamo/<int:pk>/', views.PrestamoDetail.as_view(), name='prestamo-detail'),


    # Vistas CRUD para Multa
    path('multa/', views.MultaList.as_view(), name='multa-list'),
    path('multa/<int:pk>/', views.MultaDetail.as_view(), name='multa-detail'),


    # Vistas especiales
    path('generar-multas/', views.generar_multas_view, name='generar-multas'),
    path('reporte-deporte/', views.ReporteArticulosPorDeporte.as_view(), name='reporte-deporte'),
    path('reporte-dia/', views.ReporteArticulosPorDia.as_view(), name='reporte-dia'),
    path('datos-articulos/', views.datos_articulos_por_deporte, name='datos-articulos'),
    
    path('reportes/', views.reportes_view, name='reportes'),
    path('', views.home, name='home'),
    path('multas_por_dia/', views.multas_por_dia, name='multas_por_dia'),



]




