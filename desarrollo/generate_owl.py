# -*- coding: utf-8 -*-
import re

def obtener_etiqueta(cadena):
   caracterEsp = '[A-Za-zÁÉÍÓÚÜÑáéíóúñü\s]'
   m = re.search('(?<=\\emph{)('+caracterEsp + ')+}', cadena)
   return m

def obtener_etiquetas(cadena):
   etiquetas=[]
   m=obtener_etiqueta(cadena)
   etiquetas.append(m.group(0)[:-1])
   cadena = cadena[m.end():]
   fin = m==None
   while not fin:
       m=obtener_etiqueta(cadena)
       fin = m==None
       if not fin: 
          etiquetas.append(m.group(0)[:-1])
          cadena = cadena[m.end():]
   return etiquetas

with open('glosario.tex') as f:
    read_data = f.read()
    f.closed

with open('prueba.txt', 'w') as g:
    etiquetas = obtener_etiquetas(read_data);
    for etiqueta in etiquetas:
       g.write(etiqueta + " ")
    g.closed

#print obtener_etiquetas(read_data)
