"""
URL configuration for SDP_APP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

from django.contrib.auth.views import LogoutView
from SDPv2.views import login_view, signin_view, showDocView, homeView, upload_document, lista_documentos,createCourseView, buscar,detalle_documento

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin')
    ,path('login/', login_view, name='login')
    ,path('signin/', signin_view, name='signin')
    ,path('upload/', upload_document, name='upload')
    ,path('docview/<int:document_id>/', showDocView, name='docview')
    ,path('search/', lista_documentos, name='search')
    ,path('home/', homeView, name='home')
    ,path('createCourse/', createCourseView, name='createCourseView')
    ,path('buscar/', buscar, name='buscar')
    ,path('documento/<int:documento_id>/', detalle_documento, name='detalle_documento')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


