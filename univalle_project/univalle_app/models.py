from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, time

class Univalluno(models.Model):
    ESTUDIANTE = 'Estudiante'
    FUNCIONARIO = 'Funcionario'
    TIPOS = [
        (ESTUDIANTE, 'Estudiante'),
        (FUNCIONARIO, 'Funcionario')
    ]
    TIPO_DOCUMENTO_CHOICES = (
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
    )
    
    
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo = models.CharField(choices=TIPOS, max_length=20)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=50)
    codigo_estudiante = models.CharField(max_length=50, null=True)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    class Meta:
        unique_together = ['tipo_documento', 'numero_documento']

class ArticuloDeportivo(models.Model):
    nombre = models.CharField(max_length=100)
    deporte = models.CharField(max_length=50)
    descripcion = models.TextField()
    valor = models.IntegerField(null=True, blank=True)
    prestado = models.BooleanField(default=False)  # por defecto, el artículo no está prestado

    def esta_disponible(self):
        return not self.prestado

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    univalluno = models.ForeignKey(Univalluno, on_delete=models.CASCADE)
    articulo_deportivo = models.ForeignKey(ArticuloDeportivo, on_delete=models.SET_NULL, null=True)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)  # Se establece automáticamente al crear un nuevo registro
    fecha_vencimiento = models.DateTimeField()

    def clean(self):
        # Verificar si el Univalluno ya tiene un artículo en préstamo
        prestamo_existente = Prestamo.objects.filter(univalluno=self.univalluno, articulo_deportivo__prestado=True).exclude(pk=self.pk)
        if prestamo_existente.exists():
            raise ValidationError("El Univalluno ya tiene un artículo en préstamo.")

        # Verificar si el Univalluno tiene multas pendientes
        multas_pendientes = Multa.objects.filter(prestamo__univalluno=self.univalluno, pagada=False)
        if multas_pendientes.exists():
            raise ValidationError("El Univalluno tiene multas pendientes. Debe pagarlas antes de solicitar otro préstamo.")

    def save(self, *args, **kwargs):
        # Si es una nueva instancia, establece la fecha_vencimiento a las 8:00 pm del día actual
        if not self.pk:
            ahora = datetime.now()
            self.fecha_vencimiento = datetime.combine(ahora.date(), time(20, 0))

        self.clean()
        super(Prestamo, self).save(*args, **kwargs)

    def __str__(self):
        return f"Prestamo {self.id} - {self.univalluno} - {self.articulo_deportivo}"



class Multa(models.Model):
    fecha_generada = models.DateField(null=True)
    prestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE)
    valor_multa = models.PositiveIntegerField()
    pagada = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def pagar(self):
        # Marca la multa como pagada, registra la fecha de pago y libera el artículo deportivo.
        self.pagada = True
        self.fecha_pago = timezone.now()
        # Liberar el artículo deportivo
        articulo = self.prestamo.articulo_deportivo
        articulo.prestado = False
        articulo.save()
        self.save()
        
    def generar_multas():
        # Obten todos los préstamos que no han sido devueltos antes de las 8:10 pm
        ahora = timezone.now()
        prestamos_pendientes = Prestamo.objects.filter(fecha_vencimiento__lt=ahora, articulo_deportivo__prestado=True)
    
        for prestamo in prestamos_pendientes:
            # Aquí puedes calcular el valor de la multa basado en tus reglas de negocio
            valor_multa = calcular_valor_multa(prestamo)
        
            Multa.objects.create(prestamo=prestamo, valor_multa=valor_multa)


    def __str__(self):
        return f"Multa {self.id} - Prestamo {self.prestamo.id}"
