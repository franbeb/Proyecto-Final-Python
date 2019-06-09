#codigo de la sopa de letras
import PySimpleGUI as sg
from constantes import *
import random as rand


def elegir_de_tipo(cant,lista,tipo):
	lista_copia=lista.copy()
	maxim=0
	elegidos=[]
	todas_pal=[]
	for i in range(cant):
		el=rand.choice(lista_copia)
		lista_copia.remove(el)
		elegidos.append(el)
		todas_pal.append([el[0],tipo])
		maxim=max(maxim,len(el[0]))
	return (elegidos,maxim,todas_pal)

def elegir_palabras(config,pal):  #parece que las claves ADJ,SUS y VER estan al pedo
	elegido={}
	todas_pal=[]
	maxim=0
	aux=elegir_de_tipo(config[CANT_VER],pal[VER],VER)
	elegido[VER]=aux[0]  #palabras elegidas
	maxim=max(maxim,aux[1]) #actualizae maximos
	todas_pal=todas_pal+aux[2]
	
	aux=elegir_de_tipo(config[CANT_SUS],pal[SUS],SUS)
	elegido[SUS]=aux[0]	#palabras elegidas
	maxim=max(maxim,aux[1]) #actualizae maximos
	todas_pal=todas_pal+aux[2]
	
	aux=elegir_de_tipo(config[CANT_ADJ],pal[ADJ],ADJ)
	elegido[ADJ]=aux[0]	#palabras elegidas
	maxim=max(maxim,aux[1]) #actualizae maximos
	todas_pal=todas_pal+aux[2]
	
	
	#elegido[CANT_PAL]=config[CANT_VER]+config[CANT_SUS]+config[CANT_ADJ]
	elegido[MAX_LONG]= maxim
	rand.shuffle(todas_pal)
	elegido[CANT_PAL]=len(todas_pal)
	elegido[TODAS_PAL]=todas_pal
	return elegido

def matriz_crear(elegido):
	w, h = elegido[MAX_LONG]+EXTRA_LONG, elegido[CANT_PAL];#hay que ver si deberian quedar filas vacias
	matriz = [[0 for x in range(w)] for y in range(h)]
	matriz_respuestas=[[0 for x in range(w)] for y in range(h)]
	palabras=elegido[TODAS_PAL]
	x=0
	y=0   #matriz[y][x]
	for datospal in palabras:
		x=0
		pal=datospal[0]
		margen=w-len(pal)
		
		tipo=datospal[1]

		r=rand.randrange(margen)
		for i in range(r):
			margen-=1
			matriz[y][x]='x'#caracter al alazar
			x+=1
		for letra in pal:
			matriz[y][x]=letra
			matriz_respuestas[y][x]=tipo
			x+=1
		for i in range(margen):
			matriz[y][x]='x'#caracter al alazar
			x+=1
		y+=1
	#antes de devolverla habria que ver si hay que rotralas
	return(matriz,matriz_respuestas)
		
	
# def click():
# def selcionar_tipodepal():#verbo/sustantivo/adjetivo
# def checkear():
# def generar_tablero():

def main(): #empieza a jugar
	config=import_json(DIR_CONFIG)
	todas_pal=import_json(DIR_PAL)
	print(config)
	print(todas_pal)
	elegido=elegir_palabras(config,todas_pal)
	print('sdasds: ',elegido)
	matriz,matriz_respuestas=matriz_crear(elegido)
	for lista in matriz:
		print(lista)
	for lista in matriz_respuestas:
		print(lista)
main()