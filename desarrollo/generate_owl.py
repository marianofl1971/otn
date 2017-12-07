# -*- coding: utf-8 -*-
import re

def generar_uri(etiqueta):
    listaPalabras = etiqueta.split()
    palabraEnMayuscula = ''
    for palabra in listaPalabras:
        #palabraEnMayuscula = ''.join((palabra[0].upper(),palabra[1:]))
        palabraEnMayuscula = palabraEnMayuscula+''.join((palabra[0].upper(),palabra[1:]))
    return 'http://w3id.org/education/otn#' + palabraEnMayuscula 

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
