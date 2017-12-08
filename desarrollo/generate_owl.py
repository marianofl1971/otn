#!/usr/bin/env python3.4

import re
import unicodedata

def eliminar_instruccion_url(instruccion_url):
    return re.search('(?<=url{).+?}', instruccion_url).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy

def obtener_seeAlso_una_entidad(entrada_bibtex):
    titulo = re.search('(?<=title = {).+?}', entrada_bibtex).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy
    nota = re.search('(?<=note = {).+?}', entrada_bibtex).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy
    return titulo + nota  

#def obtener_seeAlso_ontologia():

def elimina_tildes(cadena): #función inspirada en https://gist.github.com/victorono/7633010
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s

def generar_uri(etiqueta):
    etiqueta_sin_tildes = elimina_tildes(etiqueta)
    lista_palabras = etiqueta_sin_tildes.split()
    palabra_en_mayuscula = ''
    for palabra in lista_palabras:
        palabra_en_mayuscula = palabra_en_mayuscula+''.join((palabra[0].upper(),palabra[1:]))
    return 'http://w3id.org/education/otn#' + palabra_en_mayuscula 

def generar_ontologia(datos_leidos):
    with open('cabecera.owl') as f:
         cabecera = f.read()
         f.closed
    with open('ontologia.owl', 'w') as g:
         g.write(cabecera)
         etiquetas = obtener_anotaciones(datos_leidos, obtener_etiqueta, -1)
         itEt = iter(etiquetas)
         definiciones = obtener_anotaciones(datos_leidos, obtener_definicion, -3)
         itDef = iter(definiciones)
         print('Número de etiquetas generadas: ' + str(len(etiquetas)))
         print('Número de definiciones generadas: ' + str(len(definiciones)))
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
         g.write('</rdf:RDF>')
         g.closed

def obtener_anotaciones(cadena, obtener_anotacion, recorte):
    etiquetas=[]
    m=obtener_anotacion(cadena)
    etiquetas.append(m.group()[:recorte])
    cadena = cadena[m.end():]
    fin = m==None
    while not fin:
       m=obtener_anotacion(cadena)
       fin = m==None
       if not fin: 
          etiquetas.append(m.group()[:recorte])
          cadena = cadena[m.end():]
    return etiquetas

def obtener_etiqueta(cadena):
    m = re.search('(?<=\\emph{).+?}', cadena) # La última interrogación se utiliza para indicare que es non-greedy
    return m

def obtener_definicion(cadena):
    m = re.search('(?<=<<<).+?>>>', cadena)
    return m

with open('glosario_2.tex') as f:
    datos_leidos = f.read()
    f.closed
#print(eliminar_instruccion_url('url{https://www.boe.es/buscar/pdf/1985/BOE-A-1985-11578-consolidado.pdf}'))
generar_ontologia(datos_leidos)
