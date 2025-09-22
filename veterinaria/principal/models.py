from django.db import models
from django.contrib.auth.models import User

ROLES = [
    ('asistente', 'Asistente'),
    ('veterinario', 'Veterinario'),
]

class Profesional(models.Model):
    idprofesional = models.IntegerField(primary_key=True)
    run = models.CharField(max_length=13, unique=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    fono = models.CharField(max_length=45)

    class Meta:
        verbose_name_plural = "Profesionales"
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Asistente(models.Model):
    idasistente = models.OneToOneField(Profesional, on_delete=models.CASCADE, primary_key=True)
    tipo_acceso = models.CharField(max_length=45, choices=ROLES, default='asistente')

    def __str__(self):
        return self.idasistente.nombre

class Veterinario(models.Model):
    idveterinario = models.OneToOneField(Profesional, on_delete=models.CASCADE, primary_key=True)
    tipo_acceso = models.CharField(max_length=45, choices=ROLES, default='asistente')

    def __str__(self):
        return self.idveterinario.nombre

class Dueno(models.Model):
    id = models.AutoField(primary_key=True, db_column='iddueño')
    run = models.CharField(max_length=45, unique=True)
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    fono_contacto1 = models.CharField(max_length=45)
    fono_contacto2 = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
    
SEXO_CHOICES = [
    ('M', 'Macho'),
    ('H', 'Hembra'),
]    

class FichaMascota(models.Model):
    idficha_mascota = models.AutoField(primary_key=True, db_column='idficha_mascota')
    nombre = models.CharField(max_length=45)
    num_chip = models.CharField(max_length=45, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    raza = models.CharField(max_length=45)
    dueño = models.ForeignKey(Dueno, on_delete=models.CASCADE)
    asistente = models.ForeignKey(Asistente, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

class Atencion(models.Model):
    idatencion = models.AutoField(primary_key=True, db_column='idatencion')
    fecha_atencion = models.DateField()
    diagnostico = models.CharField(max_length=45)
    tratamiento = models.CharField(max_length=45)
    observaciones = models.CharField(max_length=45, blank=True, null=True)
    ficha_mascota = models.ForeignKey(FichaMascota, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Atención de {self.ficha_mascota.nombre}'

class Servicios(models.Model):
    idservicios = models.IntegerField(primary_key=True)
    descripcion_servicio = models.CharField(max_length=45)
    costo_servicio = models.IntegerField()
    servicioscol = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.descripcion_servicio

class Detalle(models.Model):
    iddetalle = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    costo = models.IntegerField()
    detallecol = models.CharField(max_length=45, blank=True, null=True)
    servicios = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    atencion = models.ForeignKey(Atencion, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profesional = models.OneToOneField('principal.Profesional', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

