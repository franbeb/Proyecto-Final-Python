#constantes?
import json

DIR_PAL = "datos/palabras.json" #Guarda la direccion donde se encuentra el json con la palabras de la sopa de letras
DIR_CONFIG = "datos/configuracion.json" #Guarda la direccion donde se encuentra la configuracion a usar en la sopa de letra
DIR_OFI = "datos/datos-oficinas.json"
LOOK = 'Look'

#Palabras.json
ADJ = 'Adjetivo' #String que representa la clave en Palabras de los adjetivos
VER = 'Verbo'   #String que representa la clave en Palabras de los verbos
SUS = 'Sustantivo' #String que representa la clave en Palabras de los sustantivos

#Configuracion.json
CANT_VER ='Cantidad_Verbos' 
CANT_ADJ = 'Cantidad_Adjetivos'
CANT_SUS = 'Cantidad_Sustantivos'
COL_ADJ = 'Color_Adjetivo'
COL_VER = 'Color_Verbo'
COL_SUS = 'Color_Sustantivo'
CONF_ORIENTACION = 'Tipo_Orientacion'
CONF_VERT = 'Vertical'
CONF_MAY = 'Mayuscula'
CONF_AYUDA = 'Ayuda'


#COLORES
COL_INCORRECTO = "#fb3338"
COL_MALCLASIFICADO = "#da716d"
COL_DEFAULT = "#77cac1"
COL_CORRECTO = "#34e238"
COL_NOSELEC = "#fcae45"
COL_NEU = 'lightblue'

#Juego

MAX_LONG = 'PalabraMasLarga' #Palabra mas larga de nuestra sopa
CANT_PAL = 'Cantidad_Palabras' #Cantidad de palabras en nuestra sopa
EXTRA_LONG = 3
TODAS_PAL = 'Todas_Palabras' #Lista con las palabras de todas la categorias

#Procesos 

def import_json(dir):
    '''Abre un archivo JSON '''
    with open(dir,'r') as arch:
        reader = json.load(arch) 
    return(reader)

def escribir_json(dir , palabras):
    '''Escribe un archivo JSON '''
    with open(dir , 'w') as new:
        new.write(json.dumps(palabras))
	