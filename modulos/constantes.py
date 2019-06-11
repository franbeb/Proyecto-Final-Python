#constantes?
import json

DIR_PAL = "../datos/palabras.json" #Guarda la direccion donde se encuentra el json con la palabras de la sopa de letras
DIR_CONFIG = "../datos/configuracion.json" #Guarda la direccion donde se encuentra la configuracion a usar en la sopa de letra


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


#Juego

MAX_LONG = 'PalabraMasLarga' #Palabra mas larga de nuestra sopa
CANT_PAL = 'Cantidad_Palabras' #Cantidad de palabras en nuestra sopa
EXTRA_LONG = 3
TODAS_PAL = 'Todas_Palabras' #Lista con las palabras de todas la categorias

#Procesos 

def import_json(dir):
    with open(dir,'r') as arch:
        reader = json.load(arch) 
    return(reader)

def escribir_json(dir , palabras):
    with open(dir , 'w') as new:
        new.write(json.dumps(palabras))
	