import csv #Importamos el módulo
datos=[] #Lista que contendrá diccionarios
with open("synergy_logistics_database.csv","r") as archivo_csv: #Cargamos archivo
  lector=csv.DictReader(archivo_csv) #Creamos el objeto como diccionario
  for linea in lector:
    datos.append(linea) #Apendamos cada diccionario en la Lista

#Después de cerrar el archivo 
lista_1=[] #Contendrá: [origen,destino,$$ total,[$$ importaciones, $$ exportaciones]]
for i in datos: #Iteramos sobre cada diccionario
  ori=i["origin"] #Origen del movimiento
  dest=i["destination"] #Destinatario del movimiento
  if not([ori,dest] in lista_1): #Para evitar rutas repetidas
    lista_1.append([ori,dest]) #Apendamos solo [origen,destino]

for j in lista_1: #iteramos sobre la lista de rutas
  cnt1=0 #Contador para ir sumando $$ valor de movimientos de importaciones
  cnt2=0 #Contador para ir sumando $$ valor de movimientos de exportaciones
  tot=0 #Suma de ambos contadores
  for i in datos: #Iteramos sobre cada diccionario
    if (j[0]==i["origin"])and(j[1]==i["destination"]): #Si coinciden origen y destino
      tot+=int(i["total_value"])
      if i["direction"]=="Imports": #Si corresponde a importación
        cnt1+=int(i["total_value"]) #Previamente era tipo string asi que convertimos
      elif i["direction"]=="Exports": #Si corresponde a exportación
        cnt2+=int(i["total_value"])
  j.append(tot) #Como tercer elemento el dinero total que se movió en esa ruta
  j.append([cnt1,cnt2]) #Como cuarto elemento de cada ruta ira el $$ total

# Utilizaré la función integrada sort para ordenar de mayor a menor las rutas de acuerdo al $$ que mueven, dado que mi lista_1 es de la forma [origen,destino,$$ total,[$$ importaciones, $$ exportaciones]] para utilizar la función sort también necesitaré el parametro key que ordena de acuerdo a la devolución de alguna función, para ello crée la siguiente función que devuelve el valor del elemento número 2 de cada lista, el cual en mi caso corresponde a $$ total
def devo(lista):
  return lista[2] #Devuelve el valor en la posición 2 de la lista sobre la que se itera

lista_1.sort(key=devo,reverse=True) #Ordenará de mayor a menor $$ total, de cada ruta

suma=0 #Aquí se obtendrá el valor total de $$$
for i in lista_1: #Iteramos sobre toda la lista de [origen,destino,$$ valor,...]
  suma+=i[2] #Vamos sumando el $$ valor, de cada ruta

print("Las 10 rutas más demandadas son:")
print("")
conta=0 #Para almacenar la suma total de ingresos
for i in range(0,10):
  print(i+1,'.-  Origen:',lista_1[i][0],' Destino:',lista_1[i][1],'  $$ Total:',lista_1[i][2])
  print('           ','$$ de importaciones:',lista_1[i][3][0],'   ','$$ de exportaciones:',lista_1[i][3][1])
  conta+=lista_1[i][2] #Incrementamos su valor
print("")
print("Ingresos totales:",conta," Porcentaje del total:",(conta/suma)*100)
print("")
lista_2=[] #Aquí iran: [medio de transporte, $$ total, [$import,$export]]
for i in datos: #Iteramos sobre cada diccionario
  if not([i["transport_mode"]] in lista_2): #Si el medio de transporte no esta
    lista_2.append([i["transport_mode"]]) #Entonces lo apendamos

for j in lista_2: #Iteramos sobre los medios de transporte
  cnt1=0 #Contador para ir sumando $$ valor de importaciones
  cnt2=0 #Contador para ir sumando $$ valor de exportaciones
  tot=0 #Suma de ambos contadores
  for i in datos: #Iteramos sobre cada diccionario
    if i["transport_mode"]==j[0]: #Cuando coincidan los medios de transporte
      tot+=int(i["total_value"])
      if i["direction"]=="Imports": #Si corresponde a importación
        cnt1+=int(i["total_value"])
      if i["direction"]=="Exports": #Si corresponde a exportación
        cnt2+=int(i["total_value"])
  j.append(tot) #El segundo elemento serán los ingresos por ese medio de transporte 
  j.append([cnt1,cnt2]) #El tercer elemento será [$$importaciones,$$exportaciones]

#Explicación análoga a lo que hice en las lineas 30 a 34
def devo2(lista):
  return lista[1] #Devuelve el valor en la posición 1 de la lista sobre la que se itera
  #En este caso es el total de ingresos de cada medio de tranpsorte
lista_2.sort(key=devo2,reverse=True) #Ordenará de mayor a menor $$ total, de cada ruta

print("")
print("Los medios de transporte de mayor a menor importancia son:")
print("")
for i in range(0,len(lista_2)):
  print(i+1,'.-',lista_2[i][0],' $$ Imports:',lista_2[i][2][0],' $$ Exports:',lista_2[i][2][1],' $$ Total:',lista_2[i][1])
print("")
lista_3=[] #Aquí irá [país,[$$ importaciones,$$ exportaciones]]
for i in datos: #Iteramos sobre los diccionarios
  if not([i["origin"]] in lista_3): #Si el país de origen no está
    lista_3.append([i["origin"]]) #Entonces lo apendamos

for j in lista_3: #Iteramos sobre la lista de paises
  cnt1=0 #Contador para ir sumando $$ valor de importaciones
  cnt2=0 #Contador para ir sumando $$ valor de exportaciones
  tot=0 #Suma de ambos contadores
  for i in datos: #Iteramos sobre los diccionarios
    if j[0]==i["origin"]: #Si coinciden los paises de origen
      tot+=int(i["total_value"])
      if i["direction"]=="Imports": #Si corresponde a importación
        cnt1+=int(i["total_value"])
      if i["direction"]=="Exports": #Si corresponde a exportación
        cnt2+=int(i["total_value"])
  j.append(tot) #El segundo elemento será el $$ valor total
  j.append([cnt1,cnt2]) #El tercer elemento será [$$import,$$export]

lista_3.sort(key=devo2,reverse=True) #Ordenará de mayor a menor $$ total, los paises

acumulador=0 #Porcentaje acumulativo
porcentaje=0.8*suma # 80% del valor de exportaciones e importaciones
ind=0 #Para ir iterando sobre la lista_1

print("")
print("Valor total de importaciones y exportaciones: $",suma)
print("Por lo que el 80 % corresponde a:",'$',porcentaje)
print("Los países que contribuyen a esos ingresos son:")
print("")
while acumulador<=80.00: #Para llegar solo al 80%
  por=(lista_3[ind][1]/suma)*100 #Porcentaje del $$ total
  acumulador+=por #Para ir acumulando porcentajes
  print(ind+1,'.-',lista_3[ind][0],'    Valor total: $',lista_3[ind][1],'   Porcentaje:',por,'%')
  ind+=1 #Para cambiar de sublista en lista_1
  
