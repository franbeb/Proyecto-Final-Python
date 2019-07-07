# desde aca podes configurar las opciones
import PySimpleGUI as sg
from modulos.constantes import *
from pattern.web import Wiktionary
from pattern.es import parse
# la config se guarde en un jason que es un dicionario como clave el nombre de la config

# Colores: se podrá configurar los colores con los que se representarán los
# sustantivos, adjetivos y verbos.


def crear_interfaz(pal, config, palabras_lista):

    ori = config[CONF_ORIENTACION] == CONF_VERT

    layout = [
            [sg.InputText(), sg.Button(button_text='AGREGAR', key='Agregar'),
                          sg.Button(button_text='ELIMINAR', key='Eliminar')],
            [sg.Text('Palabras \n Agregadas'), sg.Listbox(
                palabras_lista, size=(None, 5), key='Agregadas')],
            [sg.Text(ADJ), sg.Slider(range=(0, len(pal[ADJ])), default_value=config[CANT_ADJ], orientation='horizontal', font=('Helvetica', 12), key = 'ADJ'), sg.Button(
                button_text=COL_ADJ, button_type=sg.BUTTON_TYPE_COLOR_CHOOSER, button_color=('#000000', config[COL_ADJ]), key=COL_ADJ)],
            [sg.Text(VER), sg.Slider(range=(0, len(pal[VER])), default_value=config[CANT_VER], orientation='horizontal', font=('Helvetica', 12), key = 'VER'), sg.Button(
                button_text=COL_VER, button_type=sg.BUTTON_TYPE_COLOR_CHOOSER, button_color=('#000000', config[COL_VER]), key=COL_VER)],
            [sg.Text(SUS), sg.Slider(range=(0, len(pal[SUS])), default_value=config[CANT_SUS], orientation='horizontal', font=('Helvetica', 12), key = 'SUS'), sg.Button(
                button_text=COL_SUS, button_type=sg.BUTTON_TYPE_COLOR_CHOOSER, button_color=('#000000', config[COL_SUS]), key=COL_SUS)],
            [sg.Checkbox('Ayuda', default=config[CONF_AYUDA])],
            [sg.Text('Tipografia de texto'),sg.InputCombo(values= ['Helvetica', 'Arial', 'Calibri'], readonly= True, key = 'tipografia')],
            [sg.Checkbox('Mayusculas', default=config[CONF_MAY])],
            [sg.Radio('Vertical', 'Radio1', default=ori), sg.Radio(
                'Horizontal', 'Radio1', default=not ori)],
            [sg.Button('Guardar', key='Submit'), sg.Button(
                'Volver', key='Cancel'), sg.Button('Mostrar Reporte', key='Reporte')]
            ]

    window = sg.Window('Configuracion').Layout(layout)
    return window


def analizar_seccion(elem, tipo):
    tip = tipo
    part = elem.content.split('\n')
    defi = 'Nada'
    for p in part:
        if(p.startswith('1')):
            defi = p
    return tip, defi


def buscar_palabra(pal , reporte):
    w = Wiktionary(language='es')
    art = w.search(pal)

    tipo = 'Nada'
    tipo_wiki = 'Nada'
    tipo_pat = 'Nada'
    defi = 'Nada'
    if art != None:
        for elem in art.sections:
            if 'adjetivo' in elem.title.lower():
                tipo_wiki, defi = analizar_seccion(elem, ADJ)
            elif 'verbo' in elem.title.lower():
                tipo_wiki, defi = analizar_seccion(elem, VER)
            elif 'sustantivo' in elem.title.lower():
                tipo_wiki, defi = analizar_seccion(elem, SUS)


    tip = parse(pal)
    tip = tip.split('/')[1]
    if tip == 'NN':
       tipo_pat = SUS
    elif tip == 'VB':
        tipo_pat = VER
    elif tip == 'JJ':
         tipo_pat = ADJ
            
    if tipo_wiki == 'Nada':
        if 'Nada' != tipo_pat :

            reporte.write('No se encontro tipo en Wiktionary , se utilizo la categoria encontrada en Pattern para la palabra {} \n'.format(pal))
            tipo = tipo_pat
        else :
             sg.Popup("No tiene categoria")
             reporte.write('No se encontro tipo en Wiktionary ,ni en Pattern para la palabra {} \n'.format(pal))
    else:
        if tipo_wiki != tipo_pat and tipo_pat != 'Nada':
            reporte.write('Conflicto entre tipos de Wiktionary y Pattern , se tomara la categoria de Wiktionary para la palabra{} \n'.format(pal))
        tipo = tipo_wiki        
        
    if (defi == 'Nada') and (tipo != "Nada"):
        reporte.write('Se ingreso definicion , ya que no se pudo encontrar una en Wiktionary para la palabra {} \n'.format(pal))
        defi = sg.PopupGetText('Ingrese definicion , ya que no se pudo encontrar una en la Web')
        
     # Falta implementacion tipos pattern y Definicion
    return tipo , defi


def buscar_cat(pal) :
    
    w = Wiktionary(language = 'es')
    art = w.search(pal)

    tipo = 'Nada'
    try :
        for elem in art.sections :
            if 'adjetivo' in elem.title.lower():
                tipo = ADJ
            elif 'verbo' in elem.title.lower():
                tipo = VER
            elif 'sustantivo' in elem.title.lower():
                tipo = SUS
    except:
        sg.Popup("No se encontro en Wiki")
        
    if tipo == 'Nada':
        tip = parse(pal).split('/')[1]
        if tip == 'NN':
           tipo = SUS
        elif tip == 'VB':
            tipo = VER
        elif tip == 'JJ':
            tipo = ADJ
    # Falta implementacion tipos pattern y Definicion
    return tipo

def agregar_palabra(pal , palabras , window , palabras_lista , reporte):
    cat , definicion = buscar_palabra(pal , reporte)
    existe = cat != 'Nada'
    if(existe):
        check_repeticion = list(map(lambda x : x[0] , palabras[cat]))
        repe = not pal in check_repeticion
    else :
        repe = False
    if existe and repe: 
        palabras[cat].append([pal , definicion])
        Agregar = window.FindElement('Agregadas')
        palabras_lista.append(pal)
        Agregar.Update(values = palabras_lista )
        slider = window.FindElement(cat)
        slider.Update( range = ( 0 , len(palabras[cat])))
    else:
        if repe:
            sg.Popup('Ya se ingreso esa palabra previamente,si quiere cambiar la definicion intente eliminandola y agregandola de nuevo.')
        else:
            sg.Popup('No se encontro tipo en Wiktionary ,ni en Pattern para la palabra')

def borrar_palabra(pal , palabras , lista_palabra , window , config):
    cat = buscar_cat(pal)
    print(palabras[cat])
    for pa in palabras[cat]:
        if(pa[0] == pal):
            palabras[cat].remove(pa)
            eliminar = window.FindElement('Agregadas')
            lista_palabra.remove(pal)
            eliminar.Update(values=lista_palabra)
            #Actualizar sliders
            tipo = {SUS : CANT_SUS , ADJ : CANT_ADJ , VER : CANT_VER}
            slider = window.FindElement(cat)
            slider.Update( range = ( 0 , len(palabras[cat])))
            if(config[tipo[cat]] > len(palabras[cat])):
                config[tipo[cat]] = len(palabras[cat])
            

def checkear_sliders(config , valores):

    tipos = [None,CANT_ADJ,CANT_VER,CANT_SUS]
    ## Fijarse que no haya 0 palabras seleccionadas
    suma=0
    for i in range(1,4):
        if valores[i] == '':
            suma += config[tipos[i]]
        else:
            suma+=valores[i]
            
    if suma <= 0:
        sg.Popup("No esta permitido jugar con 0 palabras, Por favor vuelva a elegir cuantas palabras desea para jugar")
    else :
        if valores[1] != '':
            config[CANT_ADJ]  = int(valores[1])
        if valores[2] != '':
            config[CANT_VER] = int(valores[2])
        if valores[3] != '':
            config[CANT_SUS] = int(valores[3])

        
def checkear_colores(config, valores , window):
    if valores[COL_ADJ] != '':
        config[COL_ADJ] = valores[COL_ADJ]
        color_boton = window.FindElement(COL_ADJ)
        color_boton.Update(button_color = ('#000000',config[COL_ADJ]))
    if valores[COL_VER] != '':
        config[COL_VER] = valores[COL_VER]
        color_boton = window.FindElement(COL_VER)
        color_boton.Update(button_color = ('#000000',config[COL_VER]))
    if valores[COL_SUS] != '':
        config[COL_SUS] = valores[COL_SUS]
        color_boton = window.FindElement(COL_SUS)
        color_boton.Update(button_color = ('#000000',config[COL_SUS]))

def checkear_config(config, valores):
    
    config[CONF_AYUDA] = valores[4]
    config[CONF_MAY] = valores[5]
    config['tipografia'] = valores['tipografia']
    if valores[6]:
        config[CONF_ORIENTACION] = CONF_VERT
    else:
        config[CONF_ORIENTACION] = 'Horizontal'

def mostrar_reporte(reporte , fuente):
        layout = [
            [sg.Text("Reporte")],
            [sg.Listbox(reporte[0:], size=(70,10) , font = fuente)],
            [sg.Button('VOLVER')]
        ]
        window = sg.Window('Reporte', auto_size_text=True, default_element_size=(20, 1)).Layout(layout)

        while True:
            event = window.Read()
            if event[0] == 'VOLVER' or event[0] is None :
                window.Close()
                break


# Main
def main():

    reporte = open("reporte.txt","r+")
    config = {}        #Diccionario que se cargara en el configuracion.json
    palabras = import_json(DIR_PAL)
    config = import_json(DIR_CONFIG)

    
    l = list(map( lambda x : list(map(lambda y : y[0] , x)), palabras.values()))
    palabras_lista = []
    for pal in  l:
        palabras_lista = palabras_lista + pal
    window = crear_interfaz(palabras , config , palabras_lista)

    
    seguir = True
    while seguir :
        boton, valores=window.Read()
        print(boton , valores)
        if boton==None or boton=='Cancel':
            
            boo=False
            break
        if boton == 'Submit':
           checkear_sliders(config, valores)
           checkear_colores(config, valores , window)
           checkear_config(config , valores)
        elif(boton == 'Agregar'):
            agregar_palabra(valores[0] , palabras , window, palabras_lista ,reporte)
        elif(boton == 'Eliminar'):
            borrar_palabra(valores[0],palabras , palabras_lista , window , config)
        elif(boton == 'Reporte'):
            reporte.seek(0)
            mostrar_reporte(reporte.readlines() , config["tipografia"])

    window.Close()
    escribir_json(DIR_PAL , palabras)    
    escribir_json(DIR_CONFIG , config)    
    reporte.close()

# Formato del json config. Diccionario con claves sobre la opciones, cant_ver , cant_sus , cant_adj, 
