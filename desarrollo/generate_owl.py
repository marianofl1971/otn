#!/usr/bin/env python3.4

import re
import unicodedata
from collections import namedtuple

EntradaBibTex = namedtuple("EntradaBibTex", "identificador titulo uri")

#:%s@]{leyUniversidades}@ del Real Decreto 898/1985, sobre régimen del profesorado universitario 00https://www.boe.es/buscar/pdf/1985/BOE-A-1985-11578-consolidado.pdf00]@g

'''
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
'''

def generar_referencia(definicion, entrada_bibtex):
    #entrada_bibtex = leer_string_entrada_bibtex(string_entrada_bibtex)
    linea = definicion
    linea = re.sub('\[', '[véase el ', linea)
    linea = re.sub(']{'+entrada_bibtex.identificador+'}', ' del ' + entrada_bibtex.titulo + ' 00(' + entrada_bibtex.uri + ')00', linea)
    #print(']{'+entrada_bibtex.identificador+'}')
    #linea = re.sub(']{'+entrada_bibtex.identificador+'}', ' xxx  ', linea)
    linea = re.sub('\[','(', linea)
    linea = re.sub('\]',')', linea)
    linea = re.sub('00\(','[', linea)
    linea = re.sub('\)00', '])', linea)
    print(linea)
    return linea

def obtener_uri_de_latex(instruccion_url):
    return re.search('(?<=url{).+?}', instruccion_url).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy

def leer_string_entrada_bibtex(string_entrada_bibtex):
    print(string_entrada_bibtex)
    identificador = re.search('(?<=@inicio{).+?,', string_entrada_bibtex).group()[:-1]
    titulo = re.search('(?<=title = {).+?}', string_entrada_bibtex).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy
    nota = re.search('(?<=note = ").+?"', string_entrada_bibtex).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy
    uri = obtener_uri_de_latex(nota)
    ebt = EntradaBibTex(identificador, titulo, uri)
    return ebt 

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

with open('glosario_mod_1.tex') as f:
    datos_leidos = f.read()
    f.closed
#generar_ontologia(datos_leidos)
