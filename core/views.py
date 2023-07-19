from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.core.paginator import Paginator
import pyrebase, random

config={
  "apiKey": "AIzaSyCT4aK9h9pG8Uh7S__Br2Nm8Oq04XK4bOQ",
  "authDomain": "bdinfonegocio.firebaseapp.com",
  "databaseURL": "https://bdinfonegocio-default-rtdb.firebaseio.com/",
  "projectId": "bdinfonegocio",
  "storageBucket": "bdinfonegocio.appspot.com",
  "messagingSenderId": "1087803435559",
  "appId": "1:1087803435559:web:4b7aceb2daf11800dc3c02",
}
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

def home (request):
    return render(request,'core/home.html')

def perfil (request):
    if request.session['email']:
      clave=request.session['email']
      valores=database.child("Tiendas").order_by_child("email").equal_to(clave).get()
      datos=[]
      for valor in valores.each():
        datos.append(valor.val())
      return render(request, 'core/perfil.html', {'datos':datos})

def productos (request):
  clave=request.session['email']
  valores=database.child("Productos").order_by_child("email").equal_to(clave).get()
  datos=[]
  keys=[]
  for valor in valores.each():
    datos.append(valor.val())
    keys.append(valor.key())
  for i in range(len(datos)):
    datos[i]['Codigo']=keys[i]

  print(datos)

  paginator=Paginator(datos, 2)
  page_number=request.GET.get('page')
  datosp=paginator.get_page(page_number) 
  return render(request,'core/Productos.html', {'datosp':datosp})

def buscar (request):
  busqueda=request.POST['busqueda']
  clave=request.session['email']
  valores=database.child("Productos").order_by_child("email").equal_to(clave).get()
  datos=[]
  keys=[]
  for valor in valores.each():
    nombre=valor.val()['nombre']
    if busqueda.lower() in nombre.lower():
      datos.append(valor.val())
      keys.append(valor.key())
  for i in range(len(datos)):
    datos[i]['Codigo']=keys[i]

  print(datos)
  
  return render(request,'core/Productos.html', {'datos':datos})


def reportes (request):

  #Obtener el produto más visitado
  clave=request.session['email']
  valores=database.child("Productos").order_by_child("email").equal_to(clave).get()
  visitas=[]
  for valor in valores.each():
    visita=valor.val()['visitas']
    visitas.append(visita)
  maximaVisita=max(visitas)
  masvistos=database.child("Productos").order_by_child("email").equal_to(clave).get()
  datosVisitas=[]
  for valor in masvistos.each():
    compararVisita=valor.val()['visitas']
    if compararVisita==maximaVisita:
      datosVisitas.append(valor.val())

  #Obtener las visitas totales
  totales=sum(visitas)
  return render(request,'core/Reportes.html', {'datosVisitas':datosVisitas,'totales':totales})


def soporte (request):
    return render(request,'core/Soporte.html')

def FAQ (request):
    return render(request,'core/FAQ.html')

def loguear(request):
  email=request.POST.get('emailform')
  password=request.POST.get('passform')
  
  try:
    user=authe.sign_in_with_email_and_password(email,password)
  except:
    messages.add_message(request=request, level=messages.WARNING, message="Credenciales inválidas")
    return render(request, "core/home.html")

  session_email=user['email']
  request.session['email']=session_email
  registro=database.child("Tiendas").order_by_child("email").equal_to(request.session['email']).get()
  datos=[]
  for i in registro.each():
    datos.append(i.key())
  session_codigo=datos[0]
  request.session['codigo']=session_codigo
  return redirect('perfil')

def logout(request):
  del request.session['email']
  auth.logout(request)
  return render(request, "core/home.html")

def editarperfil(request):
  clave=request.session['email']
  valores=database.child("Tiendas").order_by_child("email").equal_to(clave).get()
  print(valores)
  datos=[]
  for valor in valores.each():
    datos.append(valor.val())
  print(datos)
  return render(request, 'core/edición.html', {'datos':datos})



def interfazagregar(request):
  return render(request, "core/interfazagregar.html")

def agregar(request):
  clave=request.session['email']
  codigo=request.POST['codigoform']
  existec=database.child("Productos").child(codigo).shallow().get().val()
  while existec==codigo:
    codigo=random.randint(0,999)
    existec=database.child("Productos").child(codigo).shallow().get().val()

  
  nombre=request.POST['nombreform']
  existep=database.child("Productos").order_by_child("nombre").equal_to(nombre).get().val()
  if existep!=[]:
    datos=list(existep.values())
    datos2=datos[0]
    if datos2['email']!=clave:
      descripcion=request.POST['descripcionform']
      stock=request.POST['stockform']
      visitas=0
      email=request.session['email']
      data={"nombre":nombre,"descripción":descripcion,"stock":stock, "email":email, "visitas":visitas}
      database.child("Productos").child(codigo).set(data)
      messages.add_message(request=request, level=messages.SUCCESS, message="Producto añadido satisfactoriamente")
      return redirect('productos')
    else:
      messages.add_message(request=request, level=messages.WARNING, message="Ya existe el nombre del producto, ingrese otro nombre para hacerlos distinguibles")
      return redirect('productos')
  else:
    descripcion=request.POST['descripcionform']
    stock=request.POST['stockform']
    visitas=0
    email=request.session['email']
    data={"nombre":nombre,"descripción":descripcion,"stock":stock, "email":email, "visitas":visitas}
    database.child("Productos").child(codigo).set(data)
    messages.add_message(request=request, level=messages.SUCCESS, message="Producto añadido satisfactoriamente")
    return redirect('productos')

def editar1(request, codigo):
  cod=codigo
  valores=database.child("Productos").child(cod).get()
  print(valores)
  val=[]
  for valor in valores.each():
    val.append(valor.val())
  print(val)
  datos={}
  datos['descripcion']=val[0]
  datos['nombre']=val[2]
  datos['stock']=val[3]
  datos1=[]
  datos1.append(datos)
  return render(request, 'core/edición.html', {'datos1':datos1, 'cod':cod})

def confirmarEdit(request):
  codigo=request.session['codigo']
  nombre=request.POST['nombreform']
  direccion=request.POST['direcciónform']
  telefono=request.POST['teléfonoform']
  giro=request.POST['giroform']
  database.child("Tiendas").child(codigo).update({"nombre":nombre,"dirección":direccion,"teléfono":telefono,"dirección":direccion,"giro":giro})
  return redirect('perfil')

def confirmarEdit1(request, codigo):
  cod=codigo
  nombre=request.POST['nombreform']
  descripcion=request.POST['descripciónform']
  stock=request.POST['stockform']
  database.child("Productos").child(cod).update({"nombre":nombre,"descripción":descripcion,"stock":stock})
  messages.add_message(request=request, level=messages.SUCCESS, message="Producto editado satisfactoriamente")
  return redirect('productos')

def eliminar(request, codigo):
  cod=codigo
  database.child("Productos").child(cod).remove()
  messages.add_message(request=request, level=messages.SUCCESS, message="Producto eliminado satisfactoriamente")
  return redirect('productos')

def enviarReporte(request):
  titulo=request.POST['tituloform']
  categoria=request.POST['categoriaform']
  descripcion=request.POST['descripcionform']
  email=request.session['email']
  data={"titulo":titulo,"categoria":categoria,"descripcion":descripcion, "email":email}
  database.child("Reportes").push(data)
  messages.add_message(request=request, level=messages.SUCCESS, message="Reporte enviado satisfactoriamente")
  return redirect('soporte')