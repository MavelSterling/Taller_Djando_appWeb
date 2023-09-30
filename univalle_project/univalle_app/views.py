from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, time

from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count

from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa
from .serializers import UnivallunoSerializer, ArticuloDeportivoSerializer, PrestamoSerializer, MultaSerializer
from django.shortcuts import render


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
    vencimiento = datetime.combine(now.date(), time(20, 0))
    if now > vencimiento:
        prestamos_sin_devolver = Prestamo.objects.filter(fecha_vencimiento__lte=now, articulo_deportivo__isnull=False)
        for prestamo in prestamos_sin_devolver:
            valor_multa = prestamo.articulo_deportivo.valor * 0.15  # 15% del valor del artículo
            Multa.objects.create(prestamo=prestamo, valor_multa=valor_multa)

class ReporteArticulosPorDeporte(views.APIView):
    def get(self, request, *args, **kwargs):
        inicio_fecha = self.request.query_params.get('inicio_fecha', None)
        fin_fecha = self.request.query_params.get('fin_fecha', None)
        prestamos = Prestamo.objects.filter(fecha_prestamo__range=[inicio_fecha, fin_fecha])
        reporte = {}
        for prestamo in prestamos:
            deporte = prestamo.articulo_deportivo.deporte
            if deporte in reporte:
                reporte[deporte] += 1
            else:
                reporte[deporte] = 1
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
    return render(request, 'reportes.html')