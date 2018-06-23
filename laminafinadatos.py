#coding: utf-8
import math as m
import numpy as np
import matplotlib.pyplot as plt






while True:
	try:
		r=raw_input('reflectividad de la superficie (menor que uno): \n')
		r=float(r)
		break
	except ValueError:
		print("Vaya! No te entiendo... Prueba otra vez!")	
while True:
	try:
		n=raw_input('índice de refracción del sustrato \n')
		n=float(n)
		break
	except ValueError:
		print("Vaya! No te entiendo... Prueba otra vez! (introduce un número real)")
while True:
	try:
		l=raw_input('longitud de onda en nm \n')
		l=float(l)
		break
	except ValueError:
		print("Vaya! No te entiendo... Prueba otra vez!")	
while True:
	try:
		t=raw_input('espesor de la lámina en micras\n')
		t=float(t)
		break
	except ValueError:
		print("Vaya! No te entiendo... Prueba otra vez!")	
while True:
	try:
		Smax=raw_input('¿Cuántos órdenes quieres calcular?\n')
		Smax=int(Smax)
		break
	except ValueError:
		print("Vaya! No te entiendo... Prueba otra vez!")


#---------------------------------
#se trata de representar la intensidad transmitida frente al ángulo de incidencia y frente a delta
#habrá un máximo para cada orden de p

t=t*1e3

Ai=np.linspace(0, 7, 2000)			#lista con los ángulos de incidencia para representar
Ai=np.deg2rad(Ai)

At=np.arcsin(np.sin(Ai)/n)

F=4*r**2/(1-r**2)**2
C=F/(1+F)

def Intens(Ai, t, n, l):
	At=np.arcsin(np.sin(Ai)/n)
	d=2*m.pi/l*2*t*n*np.cos(At)				#el desfase delta
	I=1/(1+F*(np.sin(d/2)**2))				#intensidad en funcion de Ai
	return I



M=2*t*n/l
Angmax=(2*1/M)**0.5
angmax=m.asin(n*Angmax)
Lc=l*m.pi*M*(F)**0.5*1e-7
Ancho=l*4/(F**0.5)/(2*m.pi*M)
print("\n \n \n")

print("Contraste				%1.4f\n" % C)
print("Longitud de coherencia			%1.2f  cm\n" % Lc)
print("Máximo orden de interferencia	       %5d\n" % m.floor(M))
print("Ancho espectral				%1.3f nm\n" % Ancho)
s=1
print("P	  Ai		err(Ai)\n")
while s<=Smax:
	Angmax=(2*s/M)**0.5
	angmax=m.asin(n*Angmax)
	Dtentret=1/(m.pi*(s)*F**0.5)
	print("%d	%1.4f		%1.4f" % (s, angmax, Dtentret))
	s+=1


I=Intens(Ai, t, n, l)


fig=plt.figure()
ax = fig.add_subplot(111, aspect='auto', facecolor='aliceblue')

ax.set_title("Reflexion en una lamina fina")
ax.grid(1,'major', 'x')
ax.set_xlabel("Angulo de incidencia (radianes)")
ax.set_ylabel("Intensidad normalizada")
ax.plot(Ai, I, '-')
plt.show()


