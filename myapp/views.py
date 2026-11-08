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
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'data', 'mascotas.txt')
    lista_mascotas = []
    
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for info_mascota in archivo:
                info_mascota = info_mascota.strip()
                if not info_mascota or info_mascota.startswith('#'):
                    continue
                partes = info_mascota.split('|')
                if len(partes) >= 5:
                    lista_mascotas.append({
                        'nombre': partes[0].strip(),
                        'especie': partes[1].strip(),
                        'peso': partes[2].strip(),
                        'edad': partes[3].strip(),
                        'descripcion': partes[4].strip(),
                    })

    if request.method == 'POST':
        # Toma los datos ingresados por el usuario en el formulario
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        mascota = request.POST.get('mascota', '').strip()
        # Verifica si los campos del formulario están llenos
        if nombre and telefono and correo and mascota:
    
            error_nombre = None
            error_telefono = None

            if any(c.isdigit() for c in nombre):
                error_nombre = 'El nombre no puede tener numeros.'

            if any(c.isalpha() for c in telefono):
                error_telefono = 'El teléfono no puede tener letras.'

            if error_nombre or error_telefono:
                contexto = {
                    'error_nombre' : error_nombre,
                    'error_telefono' : error_telefono,
                    'pagina' : 'formulario',
                    'nombre' : nombre,
                    'telefono' : telefono,
                    'correo' : correo,
                    'mascota' : mascota,
                    'mascotas' : lista_mascotas  # <--- Corregido (en plural)
                }
                return render(request, 'index.html', contexto)

            # Se define la ruta hacia el txt
            ruta_solicitudes = os.path.join( os.path.dirname(__file__), 'data', 'solicitudes.txt')

            #crea una variable la cual va a guardar en una sola linea la información del usuario, usando como separador el caracter |
            info_solicitud = f"{nombre} | {telefono} | {correo} | {mascota}\n"
            
            with open(ruta_solicitudes, 'a', encoding='utf-8') as archivo:
                archivo.write(info_solicitud)
                
            contexto = {
                "mensaje_confirmacion": "¡Su solicitud ha sido guardada exitosamente!",
                "pagina" : "formulario",
                "redireccionar" : True,
                "mascotas" : lista_mascotas
            }
            return render(request, 'index.html', contexto)
            
        # Corregido: se añade 'mascotas': lista_mascotas
        return render(request, 'index.html', {'pagina' : 'formulario', 'mascotas': lista_mascotas})
        
    # Corregido: se añade 'mascotas': lista_mascotas
    return render(request, 'index.html', {'pagina' : 'formulario', 'mascotas': lista_mascotas})