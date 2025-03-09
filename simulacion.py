import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Input
#tiempos
print("Cuantas entradas de tiempo va a introducir?")
numtime = int(input())
tiempos = np.empty((0,numtime))
times = np.empty((0,numtime))

for x in range(numtime):  
    print(f"Introduzca la hora {x+1} en el formato HH.MM")
    l = float(input())
    times = np.append(times,l)
    i = x*5
    tiempos = np.append(tiempos,i)
    

#temperaturas
print("Cuantas entradas de temperatura va a introducir?")
numtemp = int(input())
temperaturas = np.empty((0,numtemp))
for x in range(numtemp):
    print(f"Introduzca la temperatura {x+1}")
    j = float(input())
    temperaturas = np.append(temperaturas,j)

#variables conocidas
T0 = 8
Tm = 40

#ecuacion de enfriamiento
def ecuacion(t,k,t0):
    return Tm+(T0-Tm)*np.exp(-k*(t+t0))

#Procedimiento
params, inc = curve_fit(ecuacion, tiempos, temperaturas, p0=[0.01,20]) 
#valores iniciales cercanos a los calculados hardcoded, as much as i tried, if i calculated them
# here curve_fit refused to work
k, t0 = params

#Calculo de incertidumbre
incertidumbre = np.sqrt(np.diag(inc))
k_inc, t0_inc = incertidumbre

# Calcular hora de introducción
horas = int(times[0]//1)
minutos = int((times[0]%1)*100)
hora_introduccion =  (horas*60) + minutos - t0  # Convertir primer tiempo a minutos y restar t0
hora = int(hora_introduccion // 60)
minuto = int(hora_introduccion % 60)

print("--RESULTADOS--")
print(f"Hora de introducción: {hora}:{minuto:02d}")
print(f"Constante de enfriamiento (k): {k:.5f}± {k_inc:.5f} min⁻¹")
print(f"Tiempo de introducción (t0): {t0:.2f}± {t0_inc:.5f} minutos")

# Graficar los datos y el modelo ajustado
rangetime = np.linspace(-t0, 25, 100)  # Rango de tiempo para la curva ajustada
rangetemp = ecuacion(rangetime, k, t0)
plt.scatter(tiempos, temperaturas, label="Datos observados", color="violet")
plt.plot(rangetime, rangetemp, label="Modelo de enfriamiento", color="blue")
plt.axvline(x=0, color="black", linestyle="--", label=f"{horas}:{minutos:02d}")
plt.xlabel(f"Tiempo (minutos desde {horas}:{minutos:02d}")
plt.ylabel("Temperatura (°C)")
plt.title("Enfriamiento de la lata")
plt.legend()
plt.grid()
plt.show()