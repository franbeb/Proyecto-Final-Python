#desde aca podes podes acceder a la configuracion y empezar a jugar
import PySimpleGUI as sg
import modulos.juego as juego
import modulos.configurar as configurar
from modulos.constantes import *

layout = [
			[sg.Text('SOPA DE LETRA')],
			[sg.Button('Jugar'),sg.Button('Configurar')]

		 ]
boo=True
config = import_json(DIR_CONFIG)
sg.ChangeLookAndFeel(config[LOOK])
window = sg.Window('sopa de letras').Layout(layout)
while (boo):
	boton, valores=window.Read()
	if boton==None:
		boo=False
		break
	elif boton=='Jugar':
		juego.main()
	elif boton=='Configurar':
		configurar.main()
		
	print(boton)