from django.shortcuts import render

from datetime import datetime, time
from django.utils import timezone
from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa
from .serializers import UnivallunoSerializer, ArticuloDeportivoSerializer, PrestamoSerializer, MultaSerializer

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

# Vistas especiales
class GenerarMultasView(views.APIView):
    def post(self, request, *args, **kwargs):
        # Suponiendo que hay una función 'generar_multas()' que se encarga de la lógica de multas
        generar_multas()
        return Response({"detail": "Multas generadas con éxito"}, status=status.HTTP_200_OK)

# función generar_multas 
def generar_multas():
    now = timezone.now()
    vencimiento = datetime.combine(now.date(), time(20, 0))
    if now > vencimiento:
        prestamos_sin_devolver = Prestamo.objects.filter(fecha_vencimiento__lte=now, articulo_deportivo__isnull=False)
        for prestamo in prestamos_sin_devolver:
            valor_multa = prestamo.articulo_deportivo.valor * 0.15  # 15% del valor del artículo
            Multa.objects.create(prestamo=prestamo, valor_multa=valor_multa)


class MultaList(generics.ListCreateAPIView):
    queryset = Multa.objects.all()
    serializer_class = MultaSerializer
    
class MultaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Multa.objects.all()
    serializer_class = MultaSerializer
    
    
class ReporteArticulosPorDeporte(APIView):
    def get(self, request, *args, **kwargs):
        inicio_fecha = self.request.query_params.get('inicio_fecha', None)
        fin_fecha = self.request.query_params.get('fin_fecha', None)

        # Filtrar préstamos por rango de fechas
        prestamos = Prestamo.objects.filter(fecha_prestamo__range=[inicio_fecha, fin_fecha])

        # Agrupar préstamos por deporte
        reporte = {}
        for prestamo in prestamos:
            deporte = prestamo.articulo_deportivo.deporte
            if deporte in reporte:
                reporte[deporte] += 1
            else:
                reporte[deporte] = 1

        return Response(reporte)

class ReporteArticulosPorDia(APIView):
    def get(self, request, *args, **kwargs):
        inicio_fecha = self.request.query_params.get('inicio_fecha', None)
        fin_fecha = self.request.query_params.get('fin_fecha', None)

        # Agrupar préstamos por fecha y contarlos
        data = (Prestamo.objects
                .annotate(day=TruncDate('fecha_prestamo'))
                .values('day')
                .annotate(total=Count('id'))
                .order_by('day')
                .filter(day__range=[inicio_fecha, fin_fecha]))

        reporte = {item['day'].strftime('%Y-%m-%d'): item['total'] for item in data}

        return Response(reporte)





