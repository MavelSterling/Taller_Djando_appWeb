from django.contrib import admin
from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa




class UnivallunoAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'tipo', 'correo']
    search_fields = ['nombres', 'apellidos', 'correo']
    list_filter = ['tipo']

admin.site.register(Univalluno, UnivallunoAdmin)

class ArticuloDeportivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'deporte', 'valor']
    search_fields = ['nombre', 'deporte']
    list_filter = ['deporte']

admin.site.register(ArticuloDeportivo, ArticuloDeportivoAdmin)

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['univalluno', 'articulo_deportivo', 'fecha_prestamo', 'fecha_vencimiento']
    search_fields = ['univalluno__nombres', 'articulo_deportivo__nombre']

admin.site.register(Prestamo, PrestamoAdmin)

class MultaAdmin(admin.ModelAdmin):
    list_display = ['prestamo', 'valor_multa', 'pagada', 'fecha_pago']
    list_filter = ['pagada']

admin.site.register(Multa, MultaAdmin)
