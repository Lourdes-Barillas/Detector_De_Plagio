from django.db import models
from django.utils import timezone
import os

# Create your models here.
class user(models.Model):
    correo = models.EmailField(unique=True, verbose_name='Correo')
    Cod_identif = models.CharField(max_length=15, null=False, unique=True, verbose_name='Carne')

    def __str__(self) -> str:
        return self.Cod_identif

    class Meta:
        db_table = 'UserSystem'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']




#Modelo otro usuario
#-------------------------------------------------------------------------------------
class otherUser(models.Model):
    id_user = models.OneToOneField(user, on_delete=models.CASCADE)
    nombresO = models.CharField(max_length=150,null=False)
    apellidosO = models.CharField(max_length=150,null=False)

    class Meta:
            db_table = 'OtherUser'
            verbose_name = 'OtherUser'
            verbose_name_plural = 'Other_Users'
            ordering = ['id']



#Modelo para los casos para crear otros usuarios
#-------------------------------------------------------------------------------------
class caseCreateUser(models.Model):
    id_Otheruser = models.ForeignKey(otherUser, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=250,null=False)
    estado = models.CharField(max_length=50,null=False)
    fecha_creado = models.DateTimeField(auto_now_add=True, verbose_name='fechaCaso')

    class Meta:
        db_table = 'Case'
        verbose_name = 'Case'
        verbose_name_plural = 'Cases'
        ordering = ['id']



#Modelo autenticación de usuario
#-------------------------------------------------------------------------------------
class userAuth(models.Model):
    id_user = models.OneToOneField(user, on_delete=models.CASCADE)
    user = models.CharField(max_length=30,null=False)
    password = models.CharField(max_length=30,null=False)

    class Meta:
        db_table = 'userAuth'
        verbose_name = 'userAuth'
        verbose_name_plural = 'Users_Authorization'
        ordering = ['id']



#Modelo sede de la universidad
#-------------------------------------------------------------------------------------
class sede(models.Model):
    codigoSede = models.CharField(max_length=15, null= False, unique=True,verbose_name='CodigoSede')
    municipio = models.CharField(max_length=60,null=False)
    departamento = models.CharField(max_length=60,null=False)
    direccion = models.CharField(max_length=200,null=False)

    class Meta:
        db_table = 'sede'
        verbose_name = 'sede'
        verbose_name_plural = 'Sedes_Universidad'
        ordering = ['id']


#Modelo docente
#-------------------------------------------------------------------------------------
class proffessor(models.Model):
    id_user = models.OneToOneField(user, on_delete=models.CASCADE)
    nombresP = models.CharField(max_length=150,null=False)
    apellidosP = models.CharField(max_length=150,null=False)

    class Meta:
        db_table = 'Proffessor'
        verbose_name = 'Proffessor'
        verbose_name_plural = 'Docentes'
        ordering = ['id']



#Modelo del curso PG2
#-------------------------------------------------------------------------------------
class curso(models.Model):
    codigoCurso = models.CharField(max_length=15, null= False, unique=True,verbose_name='CodigoSede')
    idSede = models.OneToOneField(sede, on_delete=models.CASCADE)
    idProffessor = models.OneToOneField(proffessor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Curso'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['id']



#Modelo estudiante
#-------------------------------------------------------------------------------------
class student(models.Model):
    id_user = models.OneToOneField(user, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=150,null=False)
    apellidos = models.CharField(max_length=150,null=False)
    cursoId = models.ForeignKey(curso,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Estudiante'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['id']


#Subir un documento a su carpeta
def upload_to(instance, filename):
    #Crear la carpeta basado en el nombre de la tesis
    folder_name = instance.nombreDoc.replace(" ", "_")
    return f'Documentos_prueba/{folder_name}/{filename}'

#Modelo del objeto documento
#-------------------------------------------------------------------------------------
class documento(models.Model):
    nombreDoc = models.CharField(max_length=300, null=False, unique=True, verbose_name='NombreTesis')
    estado = models.CharField(max_length=60, null=False)
    fechaAprobado = models.DateField(null=False)
    enlaceDOI = models.URLField(null=True, blank=True)
    fechaPublicado = models.DateField(null=False, default=timezone.now)
    autor = models.TextField(null=True, blank=True)#models.OneToOneField(user, on_delete=models.CASCADE)
    documento_pdf = models.FileField(upload_to=upload_to, null=False, verbose_name='Documento PDF')

    class Meta:
        db_table = 'documento'
        verbose_name = 'documento'
        verbose_name_plural = 'documentos'
        ordering = ['id']


#Modelo del objeto documento HTML
#-------------------------------------------------------------------------------------
class docHTML(models.Model):
    doc_id = models.ForeignKey(documento,on_delete=models.CASCADE)
    ruta_html_original = models.CharField(max_length=200,null=False)
    html_sistema = models.TextField(null=False)

    class Meta:
        db_table = 'docHTML'
        verbose_name = 'docHTML'
        verbose_name_plural = 'docsHTML'
        ordering = ['id']
    


#Ver documentos
def lista_documentos(request):
    documentos = documento.objects.all()  # Obtiene todos los documentos de la base de datos
    return render(request, 'searchI.html', {'documentos': documentos})



# Modelo extendido con información adicional sobre la tesis
class TesisDetalle(models.Model):
    # Relación con el modelo 'documento'
    documento = models.ForeignKey(documento, on_delete=models.CASCADE, related_name='detalles')

    # Campos adicionales
    pregunta_investigacion = models.TextField(null=False, verbose_name="Pregunta de investigación")
    objetivo_general = models.TextField(null=False, verbose_name="Objetivo general")
    resumen = models.TextField(null=False, verbose_name="Resumen de la tesis")
    sede = models.CharField(max_length=150, null=False, verbose_name="Sede")
    doi = models.URLField(null=True, blank=True, verbose_name="DOI (Enlace)")
    path = models.TextField(null=False, verbose_name="Path")
    vector_palabras = models.JSONField(null=True, blank=True, verbose_name="Vector de palabras clave")  # Almacena las palabras clave

    class Meta:
        db_table = 'tesis_detalle'
        verbose_name = 'Tesis Detalle'
        verbose_name_plural = 'Tesis Detalles'
        ordering = ['documento']

    def __str__(self):
        return f'{self.documento.nombreDoc} - Detalles'