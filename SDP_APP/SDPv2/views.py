from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings

from SDPv2.forms import login, signin, upload
from rest_framework import viewsets
from .serializer import docSerializer
from .models import documento, docHTML, userAuth,TesisDetalle
from .forms import login
from django.utils import timezone
from django.contrib import messages

import os
import subprocess

import msal
import requests


from .Scripts.pdf import obtener_pregunta, obtener_objetivo, crearResumen, generarSinStopWords
from sklearn.feature_extraction.text import TfidfVectorizer


from fuzzywuzzy import process


# Views

# ----------------------------------------------------
# Login view
def login_view(request):
    if request.method == 'POST':
        form = login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']

            # Validar credenciales
            try:
                user_auth = userAuth.objects.get(user=username, password=password)

                # Si se encuentran las credenciales, redirigir a la página de admin o dashboard
                return redirect('home')  # Redirige a la página de administrador (o alguna otra)

            except userAuth.DoesNotExist:
                # Si las credenciales no son correctas, mostrar un mensaje de error
                messages.error(request, 'Usuario o contraseña incorrectos.')
                return redirect('login')

    else:
        form = login()

    return render(request, 'login.html', {'form': form})




def signin_view(request):
    if request.method == 'POST':
        form = signin(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario en la base de datos
            return redirect('login')  # Redirige a una página de éxito
    else:
        form = signin()

    return render(request, 'signin.html', {'form': form})



def showDocView(request, document_id):
    # Obtenemos el detalle del documento recién subido
    tesis_detalle = TesisDetalle.objects.get(documento_id=document_id)
    # Pasamos el path al template
    context = {
        'document_path': tesis_detalle.documento.documento_pdf.url,
        'document_name': tesis_detalle.documento.nombreDoc,  # Nombre de la tesis
        'author': tesis_detalle.sede,  # Autor si está disponible
        'vector': tesis_detalle.vector_palabras, 
        'resumen': tesis_detalle.resumen,
        'pregunta': tesis_detalle.pregunta_investigacion,
        'objetivo': tesis_detalle.objetivo_general
    }
    print(f"Ruta del documento: {tesis_detalle.documento.documento_pdf.url}")

    # Renderiza la plantilla y pasa la variable al contexto
    return render(request, 'docview.html', context)
  

def homeView(request):
    return render(request, 'home.html')


def obtener_vector_palabras(texto_documento):
    vectorizer = TfidfVectorizer(max_features=20, stop_words=None)  # Limita a 20 palabras clave
    tfidf_matrix = vectorizer.fit_transform([texto_documento])
    palabras = vectorizer.get_feature_names_out()
    return list(palabras)


#Vista para subir un documento
def upload_document(request):
    if request.method == 'POST':
        thesis_name = request.POST.get('thesis_name')
        author_name = request.POST.get('author')
        approved_date = request.POST.get('approved_date')
        document_file = request.FILES['document']

        # Crear el nuevo documento y guardarlo en la base de datos
        new_document = documento(
            nombreDoc=thesis_name,
            estado='Vigenge',  # Se personalizará en la bdd
            fechaAprobado=approved_date,
            #enlaceDOI=None,  # Este campo aún no está disponible
            fechaPublicado=timezone.now(),  # Fecha automática
            #autor=author,
            documento_pdf=document_file
        )
        new_document.save()
         # Ruta completa después de guardar (desde el campo FileField)
        saved_file_path = new_document.documento_pdf.path
        print(f"Archivo guardado en: {saved_file_path}")
        pregunta = obtener_pregunta(saved_file_path)
        objetivo = obtener_objetivo(saved_file_path)
        resumen = crearResumen(saved_file_path)
        # Generar vector de palabras clave
        vector_palabras = obtener_vector_palabras(generarSinStopWords(saved_file_path))

        print(pregunta + "\n\n" + objetivo + "\n\n" + resumen)

        # Crear y guardar el modelo TesisDetalle
        tesis_detalle = TesisDetalle(
            documento=new_document,  # Relacionar con el documento recién guardado
            pregunta_investigacion=pregunta,
            objetivo_general=objetivo,
            resumen=resumen,
            sede=author_name,  
            path=saved_file_path,  # Guardar el path completo del documento
            doi=None,  # Aún no es necesario
            vector_palabras=vector_palabras  # Guardar el vector de palabras
        )
        tesis_detalle.save()


        # Redirigir a la vista docview pasando el document_id
        return redirect('docview', document_id=new_document.id)
    


    return render(request, 'upload.html')



#Vista de la lista entera de documentos
def lista_documentos(request):
    documentos = documento.objects.all()  # Obtiene todos los documentos de la base de datos
    return render(request, 'searchI.html', {'documentos': documentos})


#Crear un nuevo curso vista
def createCourseView(request):
    return render(request, 'createCourse.html')


#Buscar documentos
def buscar(request):
    # Obtener los parámetros de búsqueda desde el formulario
    nombre = request.GET.get('nombre', '').lower()  # Captura el parámetro 'nombre'
    fecha = request.GET.get('fecha', '')  # Captura el parámetro 'fecha'
    sede = request.GET.get('sede', '').lower()  # Captura el parámetro 'sede'
    estado = request.GET.get('estado', '').lower()  # Captura el parámetro 'estado'

    print(f"nombre: {nombre}, fecha: {fecha}, sede: {sede}, estado: {estado}")

    # Obtener todos los documentos
    documentos = TesisDetalle.objects.all()
    maindocs = documento.objects.all()

    resultados = set()  # Usamos un set para evitar duplicados

    # Búsqueda por palabras clave en vector_palabras
    if nombre:
        for doc in documentos:
            palabras_clave = doc.vector_palabras  # Asume que es una lista de palabras clave
            if palabras_clave:  # Asegúrate de que no sea None
                coincidencia = process.extractOne(nombre, palabras_clave)
                if coincidencia and coincidencia[1] > 80:  # Si la similitud es mayor al 80%
                    resultados.add(doc)  # Añadimos a resultados usando un set para evitar duplicados

    # Búsqueda por nombre de tesis (nombreDoc)
    if nombre:  # Si el parámetro nombre está presente
        for maind in maindocs:
            palabras_clave2 = maind.nombreDoc  # Extrae el nombre de la tesis
            if palabras_clave2:  # Asegúrate de que no sea None o vacío
                palabras_clave2 = palabras_clave2.lower()  # Convierte el nombre a minúsculas para comparación uniforme
                
                # Usamos fuzzywuzzy para buscar coincidencias difusas
                similitud = process.extractOne(nombre, [palabras_clave2])
                if similitud and similitud[1] > 80:  # Si la similitud es mayor al 80%
                    resultados.add(maind)  # Añadimos a resultados el nombre de la tesis encontrada

    # Búsqueda por fecha de publicación (si tienes un campo de fecha)
    if fecha:
        documentos_fecha = maindocs.filter(fechaAprobado=fecha)  # Suponiendo que hay un campo fecha_publicacion
        for doc in documentos_fecha:
            resultados.add(doc)

    # Búsqueda por sede
    if sede:
        documentos_sede = documentos.filter(sede=sede)  # Filtrado parcial por sede
        for doc in documentos_sede:
            resultados.add(doc)

    # Búsqueda por estado
    if estado:
        documentos_estado = maindocs.filter(estado=estado)  # Filtrado parcial por estado
        for doc in documentos_estado:
            resultados.add(doc)

    # Convertimos el set a lista para evitar duplicados
    documentos = list(resultados)

    return render(request, 'searchI.html', {'documentos': documentos})



def detalle_documento(request, documento_id):
    # Obtener el documento o retornar un 404 si no existe
    documento = get_object_or_404(TesisDetalle, pk=documento_id)
    return render(request, 'docview.html', {'documento': documento})

