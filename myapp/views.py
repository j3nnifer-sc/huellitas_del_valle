import os
from django.shortcuts import render, redirect

def catalogo_mascotas(request):
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'data', 'mascotas.txt')
    #creación de lista que guardará todos los diccionarios de cada mascota
    lista_mascotas = []
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for info_mascota in archivo:
            # Se elimina algún salto de linea que esté en el txt 
            info_mascota = info_mascota.strip()
            
            #si no hay información en alguna linea o una linea comienza con #, el sistema debe de ir a la siguiente linea
            if not info_mascota or info_mascota.startswith('#'):
                continue
            # Hace que se separe la información que está en cada linea cuando encuentra un |
            partes = info_mascota.split('|')
            
            # analiza si hay por lo menos 5 fragmentos de información por mascotas
            if len(partes) >= 5:
                # Se crea un diccionario por cada mascota, se usa strip para los espacios sobrantes
                mascota = {
                    'nombre': partes[0].strip(),
                    'especie': partes[1].strip(),
                    'peso': partes[2].strip(),
                    'edad': partes[3].strip(),
                    'descripcion': partes[4].strip(),
                }
                lista_mascotas.append(mascota)
                
                
    filtro_edad = request.GET.get('edad', '').strip()
    filtro_especie = request.GET.get('especie', '').strip()
            
    lista_filtrada = []
    for mascota in lista_mascotas:
        # Verificamos si cumple con el filtro de especie
        cumple_especie = True
        if filtro_especie not in ["Todas las especies","",]:
            if filtro_especie != mascota["especie"]:
                cumple_especie = False
                
        # Verifica si cumple con el filtro de edad        
        cumple_edad = True
        if filtro_edad not in ["Todas las edades", ""]:
            if filtro_edad != mascota["edad"]:
                cumple_edad = False

        # Si cumple con ambos criterios, se añade a la lista que se va a mostrar
        if cumple_especie and cumple_edad:
            lista_filtrada.append(mascota)

    edades_unicas = sorted(list(set(m['edad'].strip().lower() for m in lista_mascotas)))

    contexto = {
        'mascotas': lista_filtrada,
        'edades_unicas' : edades_unicas,
        'pagina': 'catalogo',
        }
    return render(request, 'index.html', contexto)
                           
def ingresar_solicitud(request):
    # se toma las mascotas del txt para que sea dinámico
    ruta_mascotas = os.path.join(os.path.dirname(__file__), 'data', 'mascotas.txt')
    nombres_mascotas = []
    
    with open(ruta_mascotas, 'r', encoding='utf-8') as archivo:
        for info_mascota in archivo:
            #quita espacios en blanco que haya en la información de la mascota
            info_mascota = info_mascota.strip()
            #ignora lineas en blanco  del  txt o que comiencen con #
            if not info_mascota or info_mascota.startswith('#'):
                continue
        
            partes = info_mascota.split('|')
            if len(partes) >= 1:
                # se guarda el nombre de la mascota
                nombres_mascotas.append(partes[0].strip())

    # se crean las variables por defecto para cuando se carga el formulario limpio
    nombre = ''
    telefono = ''
    correo = ''
    mascota_seleccionada = ''

    if request.method == 'POST':
        # toma los datos ingresados por el usuario, si aún no hay nada, también lo toma para que no haya error 
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        mascota_seleccionada = request.POST.get('mascota', '').strip()
        
        # verifica si los campos del formulario están llenos
        if nombre and telefono and correo and mascota_seleccionada:
    
            error_nombre = None
            error_telefono = None
            #para cada caracter del nombre si es un digito, salta mensaje de error
            if any(c.isdigit() for c in nombre):
                error_nombre = 'El nombre no puede tener numeros.'

            if any(c.isalpha() for c in telefono):
                error_telefono = 'El teléfono no puede tener letras.'

            if error_nombre or error_telefono:
                # si hay un error, volvemos a renderizar pasando los datos y la lista de mascotas
                contexto = {
                    'error_nombre': error_nombre,
                    'error_telefono': error_telefono,
                    'pagina': 'formulario',
                    'nombre': nombre,
                    'telefono': telefono,
                    'correo': correo,
                    'mascota_seleccionada': mascota_seleccionada,
                    'nombres_mascotas': nombres_mascotas,
                    'campos_formulario': obtener_campos_dinamicos(nombre, telefono, correo)
                }
                return render(request, 'index.html', contexto)

            # Se define la ruta hacia el txt de solicitudes
            ruta_solicitudes = os.path.join(os.path.dirname(__file__), 'data', 'solicitudes.txt')
            #se ordena la información para guardarla en el txt
            info_solicitud = f"{nombre} | {telefono} | {correo} | {mascota_seleccionada}\n"
            
            #se escribe en el txt la nueva solicitud
            with open(ruta_solicitudes, 'a', encoding='utf-8') as archivo:
                archivo.write(info_solicitud)
                
            contexto = {
                "mensaje_confirmacion": "¡Su solicitud ha sido guardada exitosamente!",
                "pagina": "formulario",
                "redireccionar": True,
                'nombres_mascotas': nombres_mascotas,
                'campos_formulario': obtener_campos_dinamicos('', '', '')
            }
            return render(request, 'index.html', contexto)

    # si el usuario entra por primera vez o faltaron campos por rellenar, se usa este diccionario
    contexto = {
        'pagina': 'formulario',
        'nombres_mascotas': nombres_mascotas,
        'campos_formulario': obtener_campos_dinamicos(nombre, telefono, correo)
    }
    return render(request, 'index.html', contexto)


# función que arma los inputs dinámicamente
def obtener_campos_dinamicos(nombre, telefono, correo):
    return [
        {
            'id': 'nombre', 
            'label': 'Nombre completo *', 
            'type': 'text', 
            'placeholder': 'Escribe tu nombre completo', 
            'pattern': '[A-Za-zñÑáéíóúÁÉÍÓÚ\\s]+', 
            'title': 'El nombre no puede tener números.', 
            'value': nombre
        },
        {
            'id': 'telefono', 
            'label': 'Teléfono de contacto *', 
            'type': 'tel', 
            'placeholder': 'Ej. 310 000 0000', 
            'pattern': '[0-9]+', 
            'title': 'El Teléfono no puede tener letras', 
            'value': telefono
        },
        {
            'id': 'correo', 
            'label': 'Correo electrónico *', 
            'type': 'email', 
            'placeholder': 'correo@ejemplo.com', 
            'pattern': '', 
            'title': '', 
            'value': correo
        },
    ]
        