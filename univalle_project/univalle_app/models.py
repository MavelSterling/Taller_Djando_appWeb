from django.db import models

class Univalluno(models.Model):
    ESTUDIANTE = 'Estudiante'
    FUNCIONARIO = 'Funcionario'
    TIPOS = [
        (ESTUDIANTE, 'Estudiante'),
        (FUNCIONARIO, 'Funcionario')
    ]
    
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo = models.CharField(choices=TIPOS, max_length=20)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=50, unique=True)
    codigo_estudiante = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ArticuloDeportivo(models.Model):
    nombre = models.CharField(max_length=100)
    deporte = models.CharField(max_length=50)
    descripcion = models.TextField()
    valor = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    univalluno = models.ForeignKey(Univalluno, on_delete=models.CASCADE)
    articulo_deportivo = models.ForeignKey(ArticuloDeportivo, on_delete=models.SET_NULL, null=True)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField()

    def __str__(self):
        return f"Prestamo {self.id} - {self.univalluno} - {self.articulo_deportivo}"

class Multa(models.Model):
    prestamo = models.OneToOneField(Prestamo, on_delete=models.CASCADE)
    valor_multa = models.PositiveIntegerField()
    pagada = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Multa {self.id} - Prestamo {self.prestamo.id}"
