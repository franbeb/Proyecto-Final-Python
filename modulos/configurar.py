#desde aca podes configurar las opciones
import PySimpleGUI as sg
from constantes import *
from pattern.web import Wiktionary

#la config se guarde en un jason que es un dicionario como clave el nombre de la config

# Colores: se podrá configurar los colores con los que se representarán los
# sustantivos, adjetivos y verbos. 

def crear_interfaz(pal):
    
    layout =[   
		    [sg.InputText(), sg.Button(button_text = 'AGREGAR' , key = 'Agregar') , sg.Button(button_text = 'ELIMINAR' , key = 'Eliminar')],
            [sg.Text(ADJ) , sg.Slider(range=(0 , len(pal[ADJ])), default_value = len(pal[ADJ])/2 , orientation='horizontal', font=('Helvetica', 12)) , sg.Button(button_text=COL_ADJ, button_type=sg.BUTTON_TYPE_COLOR_CHOOSER)],
            [sg.Text(VER) , sg.Slider(range=(0 , len(pal[VER])), default_value = len(pal[VER])/2 , orientation='horizontal', font=('Helvetica', 12)) , sg.Button(button_text=COL_VER, button_type=sg.BUTTON_TYPE_COLOR_CHOOSER)],
            [sg.Text(SUS) , sg.Slider(range=(0 , len(pal[SUS])), default_value = len(pal[SUS])/2 , orientation='horizontal', font=('Helvetica', 12)) , sg.Button(button_text=COL_SUS, button_type=sg.BUTTON_TYPE_COLOR_CHOOSER)],
		    [sg.Checkbox('Ayuda' , default = False)],
            [sg.Checkbox('Mayusculas' , default = False)],
            [sg.Radio('Vertical' ,'Radio1', default = True),sg.Radio('Horizontal','Radio1')],
            [sg.Submit(),sg.Cancel()]	        
            ]

    window = sg.Window('Configuracion').Layout(layout)
    return window

def buscar_palabra(pal):
    w = Wiktionary(language = 'es')
    art = w.search(pal)

    tipo = 'Nada'
    for elem in art.sections :
        if 'adjetivo' in elem.title.lower():
            tipo = 'Adjetivo'
        elif 'verbo' in elem.title.lower():
            tipo = 'Verbo'
        elif 'sustantivo' in elem.title.lower():
            tipo = 'Sustantivo'

    #Falta implementacion tipos pattern y Definicion
    return tipo , 'Definicion '


def buscar_cat(pal):
    w = Wiktionary(language = 'es')
    art = w.search(pal)

    tipo = 'Nada'
    for elem in art.sections :
        if 'adjetivo' in elem.title.lower():
            tipo = 'Adjetivo'
        elif 'verbo' in elem.title.lower():
            tipo = 'Verbo'
        elif 'sustantivo' in elem.title.lower():
            tipo = 'Sustantivo'

    #Falta implementacion tipos pattern y Definicion
    return tipo

def agregar_palabra(pal , palabras):
    cat , definicion = buscar_palabra(pal)
    print(cat)
    palabras[cat].append([pal , definicion])


def borrar_palabra(pal , palabras):
    cat = buscar_cat(pal)
    buscando = True
    for pa in palabras[cat]:
        if(pa[0] == pal) :
            palabras[cat].remove(pa)

def checkear_sliders(config , valores):
    if valores[1] != '':
        config[ADJ]  = valores[1]
    if valores[2] != '':
        config[VER] = valores[2]
    if valores[3] != '':
        config[SUS] = valores[3]

def checkear_colores(config, valores):
    if valores[COL_ADJ] != '':
        config[COL_ADJ] = valores[COL_ADJ]
    if valores[COL_VER] != '':
        config[COL_VER] = valores[COL_VER]
    if valores[COL_SUS] != '':
        config[COL_SUS] = valores[COL_SUS]

def checkear_config(config, valores):
    
    config[CONF_AYUDA] = valores[4]
    config[CONF_MAY] = valores[5]
    if valores[5]:
        config[CONF_ORIENTACION] = CONF_VERT
    else:
        config[CONF_ORIENTACION] = 'Horizontal'
#Main

config = {}        #Diccionario que se cargara en el configuracion.json
palabras = import_json(DIR_PAL)
config = import_json(DIR_CONFIG)
window = crear_interfaz(palabras)
print(config)
seguir = True
while seguir :
    boton, valores=window.Read()
    print(boton , valores)
    if boton==None or boton=='Cancel':
        boo=False
        break
    if boton == 'Submit':
       checkear_sliders(config, valores)
       checkear_colores(config, valores)
       checkear_config(config , valores)
    elif(boton == 'Agregar'):
        agregar_palabra(valores[0] , palabras)
    elif(boton == 'Eliminar'):
        borrar_palabra(valores[0],palabras)

escribir_json(DIR_PAL , palabras)    
escribir_json(DIR_CONFIG , config)    


#Formato del json config. Diccionario con claves sobre la opciones, cant_ver , cant_sus , cant_adj, 