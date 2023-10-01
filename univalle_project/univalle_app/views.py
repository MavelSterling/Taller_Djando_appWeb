from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, time

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count

from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa
from .serializers import UnivallunoSerializer, ArticuloDeportivoSerializer, PrestamoSerializer, MultaSerializer
from django.http import JsonResponse
from django.db.models.functions import TruncDate

from django.db.models import Sum
from django.http import HttpResponse
from django.template import loader

# Vistas CRUD para Univalluno
class UnivallunoList(generics.ListCreateAPIView):
    queryset = Univalluno.objects.all()
    serializer_class = UnivallunoSerializer

class UnivallunoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Univalluno.objects.all()
    serializer_class = UnivallunoSerializer

# Vistas CRUD para ArticuloDeportivo
class ArticuloDeportivoList(generics.ListCreateAPIView):
    queryset = ArticuloDeportivo.objects.all()
    serializer_class = ArticuloDeportivoSerializer

class ArticuloDeportivoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticuloDeportivo.objects.all()
    serializer_class = ArticuloDeportivoSerializer

# Vistas CRUD para Prestamo
class PrestamoList(generics.ListCreateAPIView):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

class PrestamoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

# Vistas CRUD para Multa
class MultaList(generics.ListCreateAPIView):
    queryset = Multa.objects.all()
    serializer_class = MultaSerializer

class MultaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Multa.objects.all()
    serializer_class = MultaSerializer

@api_view(['POST'])
def generar_multas_view(request):
    generar_multas()
    return Response({"message": "Multas generadas con éxito"}, status=status.HTTP_200_OK)

def generar_multas():
    now = timezone.now()
    #vencimiento = datetime.combine(now.date(), time(20, 0))
    vencimiento = timezone.make_aware(datetime.combine(now.date(), time(20, 0)))  # Hacerla aware

    if now > vencimiento:
        prestamos_sin_devolver = Prestamo.objects.filter(fecha_vencimiento__lte=now, articulo_deportivo__isnull=False)
        for prestamo in prestamos_sin_devolver:
            valor_multa = prestamo.articulo_deportivo.valor * 0.15  # 15% del valor del artículo
            Multa.objects.create(prestamo=prestamo, valor_multa=valor_multa)

class ReporteArticulosPorDeporte(views.APIView):
    def get(self, request, *args, **kwargs):
        inicio_fecha = self.request.query_params.get('inicio_fecha', None)
        fin_fecha = self.request.query_params.get('fin_fecha', None)

        # Si no se proporcionan fechas, podemos devolver un mensaje de error o establecer fechas por defecto.
        if not inicio_fecha or not fin_fecha:
            return Response({'error': 'Se requieren las fechas de inicio y fin para generar el reporte.'}, status=status.HTTP_400_BAD_REQUEST)

        prestamos = Prestamo.objects.filter(fecha_prestamo__range=[inicio_fecha, fin_fecha])
        
        reporte = {}
        for prestamo in prestamos:
            deporte = prestamo.articulo_deportivo.deporte
            if deporte in reporte:
                reporte[deporte] += 1
            else:
                reporte[deporte] = 1

        # Si no hay datos para reportar, podemos devolver un mensaje adecuado.
        if not reporte:
            return Response({'message': 'No hay datos para reportar en el rango de fechas proporcionado.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(reporte)


class ReporteArticulosPorDia(views.APIView):
    def get(self, request, *args, **kwargs):
        inicio_fecha = self.request.query_params.get('inicio_fecha', None)
        fin_fecha = self.request.query_params.get('fin_fecha', None)
        data = (Prestamo.objects
                .annotate(day=TruncDate('fecha_prestamo'))
                .values('day')
                .annotate(total=Count('id'))
                .order_by('day')
                .filter(day__range=[inicio_fecha, fin_fecha]))
        reporte = {item['day'].strftime('%Y-%m-%d'): item['total'] for item in data}
        return Response(reporte)

def datos_articulos_por_deporte(request):
    inicio_fecha = request.GET.get('inicio_fecha')
    fin_fecha = request.GET.get('fin_fecha')

    # Filtrar préstamos por rango de fechas y agrupar por deporte
    data = (Prestamo.objects.filter(fecha_prestamo__range=[inicio_fecha, fin_fecha])
            .values('articulo_deportivo__deporte')
            .annotate(total_prestados=Count('articulo_deportivo')))

    deportes = [item['articulo_deportivo__deporte'] for item in data]
    prestados = [item['total_prestados'] for item in data]

    return JsonResponse({'deportes': deportes, 'prestados': prestados})


def reportes_view(request):
    articulos = ArticuloDeportivo.objects.all()
    context = {
        'articulos': articulos,
    }
    return render(request, 'reportes.html', context)

def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())
    


def multas_por_dia(request):
    inicio_fecha = request.GET.get('inicio_fecha')
    fin_fecha = request.GET.get('fin_fecha')
    
    multas = Multa.objects.filter(fecha_generada__range=[inicio_fecha, fin_fecha])
    total_por_dia = multas.values('fecha_generada').annotate(total=Sum('valor_multa')) 

    return render(request, 'multas_por_dia.html', {'total_por_dia': total_por_dia})
