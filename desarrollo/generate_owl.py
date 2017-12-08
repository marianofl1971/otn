# -*- coding: utf-8 -*-
import re
from collections import deque

def convertir_caracter_esp_a_ingles(caracter):
    conv_caracteres = {'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ü':'U','Ñ':'NN',
                      'á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'nn','ü':'u'}
    if caracter in conv_caracteres:
        return conv_caracteres[caracter]
    else:
        return caracter

def convertir_caracteres_esp_a_ingles(palabra):
    cola_caracteres = deque([])
    for i in range(len(palabra)):
        cola_caracteres.append(palabra[i])
    return ''.join(map(convertir_caracter_esp_a_ingles, cola_caracteres))
    #return ''.join(cola_caracteres)

def generar_uri(etiqueta):
    lista_palabras = etiqueta.split()
    palabra_en_mayuscula = ''
    for palabra in lista_palabras:
        #palabra_en_mayuscula = ''.join((palabra[0].upper(),palabra[1:]))
        palabra_en_mayuscula = palabra_en_mayuscula+''.join((convertir_caracteres_esp_a_ingles(palabra[0]).upper(),palabra[1:]))
    return 'http://w3id.org/education/otn#' + palabra_en_mayuscula 

def generar_ontologia():
    with open('cabecera.owl') as f:
         cabecera = f.read()
         f.closed
    with open('ontologia.owl', 'w') as g:
         g.write(cabecera)
         etiquetas = obtener_anotaciones(read_data, obtener_etiqueta)
         itEt = iter(etiquetas)
         definiciones = obtener_anotaciones(read_data, obtener_definicion)
         itDef = iter(definiciones)
         try:
             while True:
                 etiqueta = itEt.next()
                 termino = generar_uri(etiqueta)
                 g.write('<!--' +  termino + '-->\n')
                 g.write('<owl:Class rdf:about="'+termino+'">\n')
                 g.write('   <rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">'+itDef.next()+'</rdfs:comment>\n')
                 g.write('   <rdfs:label xml:lang="es">'+etiqueta+'</rdfs:label>\n')
                 g.write('</owl:Class>\n\n')
         except StopIteration:
              pass
         g.write('</owl:Ontology>')
         g.closed

def obtener_etiqueta(cadena):
    caracterEsp = '[A-Za-zÁÉÍÓÚÜÑáéíóúñü\s]'
    m = re.search('(?<=\\emph{)('+caracterEsp + ')+}', cadena)
    return m

def obtener_anotaciones(cadena, obtener_anotacion):
    etiquetas=[]
    m=obtener_anotacion(cadena)
    etiquetas.append(m.group(0)[:-1])
    cadena = cadena[m.end():]
    fin = m==None
    while not fin:
       m=obtener_anotacion(cadena)
       fin = m==None
       if not fin: 
          etiquetas.append(m.group(0)[:-1])
          cadena = cadena[m.end():]
    return etiquetas

def obtener_definicion(cadena):
    caracterEsp = '[\\\A-Za-zÁÉÍÓÚÜÑáéíóúñü0-9,\s\{\}\[\]\_\.]'
    m = re.search('(?<=<<<)('+caracterEsp + ')+', cadena)
    return m

with open('glosario_2.tex') as f:
    read_data = f.read()
    f.closed
print generar_uri("plan de estudios")
generar_ontologia()
'''
    m = obtener_definicion(read_data)
    print m.group(0)
'''
#print obtener_etiquetas(read_data)
