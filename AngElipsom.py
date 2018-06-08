#coding: utf - 8

import math as m  
import cmath as cm  
import numpy as np  
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import Button


'''

Este programa interactivo representa en un gráfico el comportamiento de los ángulos elipsométricos
en función del ángulo de incidencia. r_s y r_p son respectivamente los coeficientes de reflexión
perpendicular y paralelo al plano de incidencia. La definición de los ángulos elipsométricos se muestra
sobre el gráfico. Devuelve además el ánculo de polarización para los índices real y complejo elegidos
con los sliders, sobre el mismo gráfico.


"facecolor" puede no funcionar en algunas versiones de Python. Si fuera el caso, elimínese sin mayor
problema. Su función es meramente estética.

'''

#funciones necesarias
def Gat(n, ai):						#ángulo de transmisión (complejo)
	return cm.asin(cm.sin(ai)/n)


def Grs(n, ai, fit):				#rs (complejo)
	return (m.cos(ai)-n*cm.cos(fit))/(m.cos(ai)+n*cm.cos(fit))

def Grp(n, ai, fit):				#rp (complejo)
	return (n*m.cos(ai)-cm.cos(fit))/(n*m.cos(ai)+cm.cos(fit))

def GRr(rs, rp, ri):				#Rr(array complejo)
	return np.array([rs*Ri[0], rp*Ri[1]])


Ri=np.array([1, 1j])     			#polarización inicial (circular levógira por defecto)

ailist=np.linspace(0, 90, 500)		#mallado del ángulo de incidencia
ailistrad=ailist*m.pi/180

nr0=1.5; nc0=0						#parte real y compleja de los índices de refracción (iniciales)

nr=nr0; nc=nc0
n=nr+nc*1j

Dlist=np.zeros(len(ailist))			#lista conteniendo los desfases entre las componentes r y s
Plist=np.zeros(len(ailist))			#lista conteniendo la relación entre sus módulos

if nc==0:							#dieléctrico

	for s in range(len(ailist)):

		atransm=Gat(n, ailistrad[s])
		rs=Grs(n, ailistrad[s], atransm)    
		rp=Grp(n, ailistrad[s], atransm)
		Delta=cm.phase(rs)-cm.phase(rp)
		Dlist[s]=Delta
else:								#metal

	for s in range(len(ailist)):

		atransm=Gat(n, ailistrad[s])
		rs=Grs(n, ailistrad[s], atransm)    
		rp=Grp(n, ailistrad[s], atransm)
		Delta=cm.phase(rs)-cm.phase(rp)+2*m.pi
		if Delta > 2*m.pi: Delta=Delta-2*m.pi
		Dlist[s]=Delta

for s in range(len(ailist)):
	
	atransm=Gat(n, ailistrad[s])
	rs=Grs(n, ailistrad[s], atransm)    
	rp=Grp(n, ailistrad[s], atransm)
	Rr=GRr(rs, rp, Ri)
	Rr=np.array([cm.polar(Rr[0]), cm.polar(Rr[1])])
	Plist[s]=abs(Rr[1][0]/Rr[0][0])*4 


#creamos el plot. l es el eje para Dlist y l2 el eje para Plist.
fig, ax= plt.subplots(figsize=(16, 8))
plt.subplots_adjust(left=0.25, bottom=0.25)
l, = plt.plot(ailist, Dlist, lw=2, color='red')
l2, = plt.plot(ailist, Plist, lw=2, color='blue')

#propiedades del gráfico
ax.axis([0, 90, 0, 3.5])
ax.set_yticks([0., .5*np.pi, np.pi, 4])
ax.set_yticklabels(["$0$", r"$\frac{1}{2}\pi$",r"$\pi$"])
axcolor = 'lightgoldenrodyellow'
axnr = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axnc = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)

#se definen los sliders para las componentes real y compleja del índice
snr = Slider(axnr, 'Indice de refraccion real', 1.01, 8, valinit=nr0)
snc = Slider(axnc, 'Coeficiente de extincion', 0, 10.0, valinit=nc0)

#anotaciones sobre el gráfico
plt.text(-3.1, 27.5, "Comportamiento de los angulos elipsometricos frente al angulo de incidencia"  , fontsize=21)
plt.text(-3.1, -1, r'Se define el el angulo elipsometrico $\Psi$ como $\Psi=atan\mid r_s$ $/$ $ r_p\mid$'  , fontsize=11, color='blue')
plt.text(-3.1, -2, r'Se define el el angulo elipsometrico $\Delta$ como $\Delta=ang(r_s)-ang(r_p)$'  , fontsize=11, color='red')

#títulos de los ejes
ax.set_xlabel(r'Angulo de incidencia')
ax.set_ylabel(r'$\gamma$ (desfase s-p)', color='red',fontsize=11)

#definición y título del eje derecho
ax2 = ax.twinx()
ax2.axis([0, 90, 0, 1])
ax2.set_ylabel(r'$r_{p}$  $/$  $r_{s}$', color='blue',fontsize=11)


def data1 (nr, nc):
#Esta función actualiza los valores del eje izquierdo

	n=nr+nc*1j
	if nc==0:
		for s in range(len(ailist)):
			atransm=Gat(n, ailistrad[s])
			rs=Grs(n, ailistrad[s], atransm)    
			rp=Grp(n, ailistrad[s], atransm)
			Delta=cm.phase(rs)-cm.phase(rp)
			Dlist[s]=Delta
	else:
		for s in range(len(ailist)):
			atransm=Gat(n, ailistrad[s])
			rs=Grs(n, ailistrad[s], atransm)    
			rp=Grp(n, ailistrad[s], atransm)
			Delta=cm.phase(rs)-cm.phase(rp)+2*m.pi
			if Delta > 2*m.pi: Delta=Delta-2*m.pi
			Dlist[s]=Delta
			Dlist[-1]=0
	return Dlist
	
def dataR (nr, nc):
#Equivalente a la anterior, actualiza los valores del eje derecho

	n=nr+nc*1j
	Plist=np.zeros(len(ailist))
	for s in range(len(ailist)):
		atransm=Gat(n, ailistrad[s])
		rs=Grs(n, ailistrad[s], atransm)    
		rp=Grp(n, ailistrad[s], atransm)
		Rr=GRr(rs, rp, Ri)
		Rr=np.array([cm.polar(Rr[0]), cm.polar(Rr[1])])
		Plist[s]=abs(Rr[1][0]/Rr[0][0])*4
	return Plist
	
def update(val):
#se ejecuta cada vez que movamos un slider. Llama a las dos anteriores y actualiza el gráfico.

    nrd = snr.val
    ncd = snc.val
    a=(cm.atan(nrd+ncd*1j).real*180/m.pi)
    plt.title("Angulo de polarizacion  "+"%.2f grados" % a, loc='right')
    l.set_ydata(data1(nrd, ncd))
    l2.set_ydata(dataR(nrd, ncd))
    fig.canvas.draw_idle()

snr.on_changed(update)
snc.on_changed(update)

#se construye el botón reset
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reiniciar', color=axcolor, hovercolor='0.975')

def reset(event):
    snr.reset()
    snc.reset()
button.on_clicked(reset)


#más anotaciones
plt.text(-7.5, 21, "ALGUNOS EJEMPLOS"  , fontsize=10, color='blue')
plt.text(-7.5, 19, "material     real(N)     imag(N)"  , fontsize=10, color='magenta')
plt.text(-7.5, 18, "Aluminio      1.34         7.62"  , fontsize=10)
plt.text(-7.5, 17,  "Boro             2.35        1.50"  , fontsize=10)
plt.text(-7.5, 16,  "Carbono       3.15        0.04"  , fontsize=10)
plt.text(-7.5, 15,  "NaCl             1.78        0.00"  , fontsize=10)
plt.text(-7.5, 14,  "Cobre           1.21        1.78"  , fontsize=10)
plt.text(-7.5, 13,  "fuente: refractiveindex.info"  , fontsize=10, color='green')


#cuestiones estéticas
rect = fig.patch
rect.set_facecolor('aliceblue')
ax.grid(linestyle='dotted')

plt.show()
