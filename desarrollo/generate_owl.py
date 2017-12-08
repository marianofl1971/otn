#!/usr/bin/env python3.4

import re
import unicodedata
import sys

'''
def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()
'''

def generar_uri(etiqueta):
    etiqueta_sin_tildes = etiqueta
    lista_palabras = etiqueta_sin_tildes.split()
    palabra_en_mayuscula = ''
    for palabra in lista_palabras:
        #palabra_en_mayuscula = ''.join((palabra[0].upper(),palabra[1:]))
        palabra_en_mayuscula = palabra_en_mayuscula+''.join((palabra[0].upper(),palabra[1:]))
    return 'http://w3id.org/education/otn#' + palabra_en_mayuscula 

def generar_ontologia(datos_leidos):
    with open('cabecera.owl') as f:
         cabecera = f.read()
         f.closed
    with open('ontologia.owl', 'w') as g:
         g.write(cabecera)
         etiquetas = obtener_anotaciones(datos_leidos, obtener_etiqueta)
         itEt = iter(etiquetas)
         definiciones = obtener_anotaciones(datos_leidos, obtener_definicion)
         itDef = iter(definiciones)
         print(len(etiquetas))
         print(len(definiciones))
         try:
             for i in range(len(etiquetas)):
                 etiqueta = next(itEt)
                 termino = generar_uri(etiqueta)
                 g.write('<!--' +  termino + '-->\n')
                 g.write('<owl:Class rdf:about="'+termino+'">\n')
                 g.write('   <rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">'+next(itDef)+'</rdfs:comment>\n')
                 g.write('   <rdfs:label xml:lang="es">'+etiqueta+'</rdfs:label>\n')
                 g.write('</owl:Class>\n\n')
         except StopIteration:
              pass
         g.write('</owl:Ontology>')
         g.closed

def obtener_anotaciones(cadena, obtener_anotacion):
    etiquetas=[]
    m=obtener_anotacion(cadena)
    etiquetas.append(m.group()[:-1])
    cadena = cadena[m.end():]
    fin = m==None
    while not fin:
       m=obtener_anotacion(cadena)
       fin = m==None
       if not fin: 
          etiquetas.append(m.group()[:-1])
          cadena = cadena[m.end():]
    return etiquetas

def obtener_etiqueta(cadena):
    #caracterEsp = '[A-Za-zÁÉÍÓÚÜÑáéíóúñü\s]'
    m = re.search('(?<=\\emph{).+?}', cadena) # La última interrogación se utiliza para indicare que es non-greedy
    #m = re.search('(?<=<<<).+>>>', cadena)
    return m

def obtener_definicion(cadena):
    #caracterEsp = '[\\\A-Za-zÁÉÍÓÚÜÑáéíóúñü0-9,\s\{\}\[\]\_\.]'
    m = re.search('(?<=<<<).+?>>>', cadena)
    return m

with open('glosario_2.tex') as f:
    datos_leidos = f.read()
    f.closed
#print generar_uri("plan de estudios")
generar_ontologia(datos_leidos)
'''
    m = obtener_definicion(datos_leidos)
    print m.group(0)
'''
#print obtener_etiquetas(datos_leidos)
