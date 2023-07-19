from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('perfil/',views.perfil,name='perfil'),
    path('productos',views.productos,name='productos'),
    path('peportes',views.reportes,name='reportes'),
    path('soporte',views.soporte,name='soporte'),
    path('FAQ',views.FAQ,name='FAQ'),
    path('loguear/', views.loguear,name="loguear"),
    path('logout/', views.logout,name="logout"),
    path('editarperfil/', views.editarperfil,name="editarperfil"),
    path('buscar/', views.buscar),
    path('interfazagregar/', views.interfazagregar,name="interfazagregar"),
    path('agregar/', views.agregar),
    path('editar1/<codigo>', views.editar1),
    path('confirmarEdit/', views.confirmarEdit),
    path('confirmarEdit1/<codigo>', views.confirmarEdit1),
    path('eliminar/<codigo>', views.eliminar),
    path('enviarReporte/', views.enviarReporte),
    path('admin/', admin.site.urls),
]
