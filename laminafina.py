#coding: utf-8


import math as m
import numpy as np

#La representación se realiza en Bokeh
from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider, Label
from bokeh.plotting import figure, output_file, show, ColumnDataSource

'''
dibuja el patrón de difracción tras múltiples refelxiones en una lámina fina.
Construye un html que puede ejecutarse desde cualquier navegador
'''


r=0.9			#reflectividad (entre 0 y 1)
n=1.5			#índice de refracción
l=500 			#lambda, nm
t=500			#espesor, micras
p=2				#orden del máximo que queremos ver (orden 0 -> y=0 en la pantalla)
I0=1			#la intensidad inicial, aporta generalidad pero no es relevante

#---------------------------------
#se trata de representar la intensidad transmitida frente al ángulo de incidencia y frente a delta
#habrá un máximo para cada orden de p


t=t*1e3

Ai=np.linspace(0, 7, 20000)			#lista con los ángulos de incidencia para representar
Ai=np.deg2rad(Ai)

At=np.arcsin(np.sin(Ai)/n)

def Intens(Ai, t, n, l):
	At=np.arcsin(np.sin(Ai)/n)
	F=4*r**2/(1-r**2)**2
	d=2*m.pi/l*2*t*n*np.cos(At)				#el desfase delta
	I=1/(1+F*(np.sin(d/2)**2))				#intensidad en funcion de Ai
	return I


I=Intens(Ai, t, n, l)


#........................................
#representación en Bokeh
#........................................

x=Ai
y=Intens(Ai, t, n, l)

source=ColumnDataSource(data=dict(x=x, y=y))

plot = figure(plot_height=500, plot_width=500, title="REFLEXIONES MÚLTIPLES EN UNA LÁMINA FINA")
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
plot.xaxis.axis_label = 'Angulo de incidencia (rad)'
plot.yaxis.axis_label = 'Intensidad'

callback = CustomJS(args=dict(source=source), code="""
	var data=source.data;
	var l=lamba.value;
	var n=indic.value;
	var t=espesor.value*1000;
	var r=reflec.value;
	x=data['x']
	y=data['y']
	F=4*r**2/(1-r**2)**2;
	for (i = 0; i < x.length; i++) {
		At=Math.asin((Math.sin(x[i]))/n);
		d=Math.PI/l*4*t*n*Math.cos(At);
		I=1/(1+F*((Math.sin(d/2))**2));
        y[i] =I;
        }
	source.change.emit();
""")


#parámetros

lamba_slider=Slider(title="longitud de onda (nm)", value=633, start=630, end=636, step=0.001, callback=callback,format = "0[.]0")
callback.args["lamba"]=lamba_slider

indic_slider=Slider(title="índice de refracción", value=1.500, start=1.495, end=1.505, step=0.00001, callback=callback, format = "0[.]0000")
callback.args["indic"]=indic_slider

espesor_slider=Slider(title="espesor de la lámina (micras)", value=500.5, start=500, end=501, step=0.001, callback=callback)
callback.args["espesor"]=espesor_slider

reflec_slider=Slider(title="reflectividad", value=0.8, start=0.5, end=0.99, step=0.001, callback=callback)
callback.args["reflec"]=reflec_slider

layout = row(
	plot, 
	widgetbox(lamba_slider, indic_slider, espesor_slider, reflec_slider),
	)


#-------------------------------------------------------------------------------------
citation = Label(x=0.07, y=0.07, x_units='screen', y_units='screen',
                 text='Collected by Luke C. 2016-04-01', render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)	
#-------------------------------------------------------------------------------------	
	
	
#salida en html
output_file("simulacion.html", title="simulacion")
show(layout)
