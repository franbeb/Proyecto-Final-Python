#codigo de la sopa de letras
#el boton para elegir color deberia ser del color seleccionado
#opcion de mas ayuda que seleciona algunas casillas al comienzo

import PySimpleGUI as sg
from modulos.constantes import *
import random as rand
import string

def letra_random(may):
	letra = rand.choice(string.ascii_lowercase)
	if may:
		letra=letra.upper()
	return letra
def rotate_matrix( m, cant_veces=3):
	new=m
	for x in range(cant_veces):
		new=[[new[j][i] for j in range(len(new))] for i in range(len(new[0])-1,-1,-1)]
	return new
	
def elegir_de_tipo(cant,lista,tipo,mayus=False):
	lista_copia=lista.copy()
	maxim=0
	elegidos=[]
	todas_pal=[]
	for i in range(cant):
		el=rand.choice(lista_copia)
		lista_copia.remove(el)
		if mayus:
			el[0]=el[0].upper()
		else:
			el[0]=el[0].lower()
		elegidos.append(el)
		todas_pal.append([el[0],tipo,el[1]])
		maxim=max(maxim,len(el[0]))
	return (elegidos,maxim,todas_pal)

def elegir_palabras(config,pal):  #parece que las claves ADJ,SUS y VER estan al pedo
	elegido={}
	todas_pal=[]
	maxim=0
	aux=elegir_de_tipo(config[CANT_VER],pal[VER],VER,config[CONF_MAY])
	elegido[VER]=aux[0]  #palabras elegidas #esto no se usa
	maxim=max(maxim,aux[1]) #actualizae maximos
	todas_pal=todas_pal+aux[2]
	
	aux=elegir_de_tipo(config[CANT_SUS],pal[SUS],SUS,config[CONF_MAY])
	elegido[SUS]=aux[0]	#palabras elegidas #esto no se usa
	maxim=max(maxim,aux[1]) #actualizae maximos
	todas_pal=todas_pal+aux[2]
	
	aux=elegir_de_tipo(config[CANT_ADJ],pal[ADJ],ADJ,config[CONF_MAY])
	elegido[ADJ]=aux[0]	#palabras elegidas #esto no se usa
	maxim=max(maxim,aux[1]) #actualizae maximos
	todas_pal=todas_pal+aux[2]
	
	
	#elegido[CANT_PAL]=config[CANT_VER]+config[CANT_SUS]+config[CANT_ADJ]
	elegido[MAX_LONG]= maxim
	rand.shuffle(todas_pal)
	elegido[CANT_PAL]=len(todas_pal)
	elegido[TODAS_PAL]=todas_pal
	return elegido

def matriz_crear(elegido,config):
	w, h = elegido[MAX_LONG]+EXTRA_LONG, elegido[CANT_PAL];#hay que ver si deberian quedar filas vacias
	matriz = [[0 for x in range(w)] for y in range(h)]
	matriz_respuestas=[[None for x in range(w)] for y in range(h)]
	matriz_input=[[None for x in range(w)] for y in range(h)]
	matriz_output=[[None for x in range(w)] for y in range(h)]
	palabras=elegido[TODAS_PAL]
	x=0
	y=0   #matriz[y][x]
	for datospal in palabras:
		x=0
		pal=datospal[0]
		margen=w-len(pal)
		
		tipo=datospal[1]

		r=rand.randrange(margen+1) #agrego 1 xq por alguna razon nunca quedaban sin margen derecho
		for i in range(r): #me parece que  no pueden quedar sin margen derecho
			margen-=1
			matriz[y][x]=letra_random(config[CONF_MAY])#caracter al alazar
			x+=1
		for letra in pal:
			matriz[y][x]=letra
			matriz_respuestas[y][x]=tipo
			x+=1
		for i in range(margen):
			matriz[y][x]=letra_random(config[CONF_MAY])#caracter al alazar
			x+=1
		y+=1
	if config[CONF_ORIENTACION]== CONF_VERT:
		matriz=rotate_matrix(matriz)
		matriz_respuestas=rotate_matrix(matriz_respuestas)
		matriz_input=rotate_matrix(matriz_input)
		matriz_output=rotate_matrix(matriz_output)
	
	return(matriz,matriz_respuestas,matriz_input,matriz_output)
	
	
	
	
def crear_layout(matriz,config,palabras):#HACER CONTANTES PARA TAM,PAD Y COLORNEUTRAL!!!!
	layout = [    
         [sg.Text('sopa de letras: ')]
		 ]
	y=0
	for lista in matriz:
		l=[]
		x=0
		for elem in lista:
			l.append(sg.Text(elem,enable_events=True,background_color='lightblue',key=(y,x),size=(2,1),justification='center',pad=(0,0)))#sisze(4,2)?
			x+=1
		layout.append(l)
		y+=1
	layout.append([sg.Button(button_text=ADJ,button_color=('#000000',config[COL_ADJ]),key=(ADJ)),sg.Button(button_text=SUS,button_color=('#000000',config[COL_SUS]),key=(SUS)),sg.Button(button_text=VER,button_color=('#000000',config[COL_VER]),key=(VER))])
	
	
	if config[CONF_AYUDA]:
		for pal,tipo,defi in palabras:
			pal_secreta = '_ ' * len(pal)
			i=  rand.randrange(len(pal))
			pal_secreta = pal_secreta[:i*2] + pal[i]+' ' + pal_secreta[i*2+1:]
			layout.append([sg.Text(''.join([pal_secreta,' : ',defi]))]	)		
	else:
		if CANT_SUS!=0:
			layout.append([sg.Text(''.join(['Cantidad de sustantivos: ',str(config[CANT_SUS])]))])
		if CANT_ADJ!=0:
			layout.append([sg.Text(''.join(['Cantidad de adjetivos: ',str(config[CANT_ADJ])]))])
		if CANT_VER!=0:
			layout.append([sg.Text(''.join(['Cantidad de verbos: ',str(config[CANT_VER])]))])
		
	layout.append([sg.Button('Corregir',key='Submit'),sg.Button('Volver',key='Cancel')]	)
	return(layout)
	
def checkear(respuestas,input,output,config,matriz_letras):
	
	# correccion = [['N' for x in range(w)] for y in range(h)]
	# for x in range(w):
		# for y in range(h):
			# correccion[y][x]= 'C' if respuestas[y][x]==input[y][x] else 'I' #CONT PARA CORRECTO E INCORRECTO y sus respectivos colores
	layout = [    
         [sg.Text('correccion: ')],
		 [sg.Text('Color para las letras que marcaste bien!' , background_color = COL_CORRECTO)],
		 [sg.Text('Color las palabras que te olvidaste de seleccionar :(', background_color = COL_NOSELEC)],
		 [sg.Text('Color las palabras que clasificaste mal :/' , background_color = COL_MALCLASIFICADO)],
		 [sg.Text('Color para letras que marcaste muy mal >:(', background_color = COL_INCORRECTO)],
		 [sg.Text('Color para letras al azar', background_color = COL_DEFAULT)],
		 [sg.Text('')]
		 ]
	y=0
	for lista in output:
		l=[]
		x=0
		for elem in lista:
			if respuestas[y][x]==input[y][x]:
				output[y][x]= 'C'
				if respuestas[y][x]==None:
					color= COL_DEFAULT #letra al azar que no marcaste: bien!
				else:
					color= COL_CORRECTO #marcado bien de palabra
			else:
				output[y][x]= 'I'
				if input[y][x]==None: 
					color= COL_NOSELEC #no lo selecionaste!
				else:
					if respuestas[y][x]==None:
						color= COL_INCORRECTO	 #para el orto!
					else:
						color= COL_MALCLASIFICADO #mal clasificado
			l.append(sg.Text(matriz_letras[y][x],background_color=color,size=(2,1),justification='center',pad=(0,0)))
			x+=1
		layout.append(l)
		y+=1
	
	layout.append([sg.Button('Volver a jugar' , key = 'Repetir') , sg.Button('Volver a Menu' , key = 'Back')])
	window = sg.Window('sopa de letras').Layout(layout)
	boton, valores=window.Read()
	window.Close()
	return (boton)
			
# def click():
# def selcionar_tipodepal():#verbo/sustantivo/adjetivo

# def generar_tablero():

def main(): #empieza a jugar
	
	config=import_json(DIR_CONFIG)
	todas_pal=import_json(DIR_PAL)
	print(config)
	print(todas_pal)
	elegido=elegir_palabras(config,todas_pal)
	print('sdasds: ',elegido)
	matriz,matriz_respuestas,matriz_input,matriz_output=matriz_crear(elegido,config)
	# for lista in matriz:
		# print(lista)
	# for lista in matriz_respuestas:
		# print(lista)
	layout= crear_layout(matriz,config,elegido[TODAS_PAL])					
	window = sg.Window('sopa de letras').Layout(layout)
	
	dic_col={ADJ:config[COL_ADJ],SUS:config[COL_SUS],VER:config[COL_VER]}
	
	boo=True
	tipo_selecionado=ADJ

	
	#Para volver a jugar
	repetir = False
	
	while(boo):
		boton, valores=window.Read()
		if boton==None or boton=='Cancel':
			boo=False
			break
		elif boton==ADJ:
			tipo_selecionado=ADJ

		elif boton==SUS:
			tipo_selecionado=SUS
			
		elif boton==VER:
			tipo_selecionado=VER
			
		elif boton=='Submit': 
			respuesta = sg.PopupYesNo('Estas seguro que queres corregir tu sopa ?')
			if respuesta == 'Yes':
				opcion = checkear(matriz_respuestas,matriz_input,matriz_output,config,matriz)
				if opcion == 'Repetir':
					repetir = True
				boo=False
				
				
		else:
			selec=window.Element(boton)
			if matriz_input[boton[0]][boton[1]]==tipo_selecionado:
				matriz_input[boton[0]][boton[1]]=None
				selec.Update(background_color='lightblue')###color neutro
			else:
				matriz_input[boton[0]][boton[1]]=tipo_selecionado
				selec.Update(background_color=dic_col[tipo_selecionado])###color asociado con ese tipo
		print(tipo_selecionado, boton)
	window.Close()
		# for lista in matriz_input:
			# print(lista)
	if repetir:
		main()