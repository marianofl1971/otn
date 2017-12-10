#!/usr/bin/env python3.4

import re
import unicodedata
from collections import namedtuple

EntradaBibTex = namedtuple("EntradaBibTex", "identificador titulo uri")

#:%s@]{leyUniversidades}@ del Real Decreto 898/1985, sobre régimen del profesorado universitario 00https://www.boe.es/buscar/pdf/1985/BOE-A-1985-11578-consolidado.pdf00]@g

def extraer_referencias():
    """
        A partir de un fichero bibtex transformado, genera una lista de tuplas del tipo EntradaBibTex.
        Véase el fichero 'diccionario_bib.dic' para ver el formato esperado. Tal y como se puede
        comprobar, se han eliminado los símbolos '\' del fichero bibTex original, se ha añadido la
        secuencia ',,,' al final de cada referencia, y se han cambiado todos los tipos de documento
        por 'inicio'

        :return: lista de entradas de tuplas del tipo EntradaBibTex. 
    """
    with open('diccionario_bib.dic') as f:
         referencias = f.read()
         f.closed
    ebs=[]
    m=extraer_referencia(referencias) #Se extrae la primera referencia
    fin = m==None
    while not fin:
       string_referencia = m.group()[:-4] #Se elimina la secuencia ',,,}' del final de la cadena
       eb = transformar_string_entrada_bibtex(string_referencia) #Se transforma la referencia en una tupla del tipo EntradaBibTex
       ebs.append(eb) #Se añade la tupla a la lista
       referencias = referencias[m.end():] #Se avanza el puntero que recorre la cadena leída del fichero.
       m=extraer_referencia(referencias) #Se extrae la siguiente referencia
       fin = m==None
    return ebs

def extraer_referencia(cadena):
    """
       A partir de una cadena de caracteres según el formato que se puede apreciar en diccionario_bib.dic,
       se obtiene la primera referencia. Para ver el uso de este método, se puede examinar extraer_referencias()

       :param cadena: Cadena de caracteres según el formato que se puede apreciar en diccionario_bib.dic.
       :return: un match
    """
    #m = re.search('(?<=@inicio{).+?,,,}', cadena) # La última interrogación se utiliza para indicare que es non-greedy
    m = re.search('(?<=@).+?,,,}', cadena) # La última interrogación se utiliza para indicare que es non-greedy
    return m

def explotar_referencias_en_definicion(definicion, ebs):
    l_string = []
    l_string.append(definicion)
    for eb in ebs:
       l_string.append(explotar_referencia_en_definicion(l_string[len(l_string)-1], eb))
    return l_string[len(l_string)-1]

def explotar_referencia_en_definicion(definicion, entrada_bibtex):
    """
       Toma como entrada una definición de un término de una ontología según el formato de glosario_mod_1.tex, y de una
       tupla del tipo EntradaBibTex, y transforma la definición en otra con las referencias en un formato natural para
       leídas por las personas.

       :param definicion: definición de un término de una ontología según el formato de glosario_mod_1.tex.
       :param entrada_bibtex: tupla del tipo EntradaBibTex.
       :return definición transformada de tal forma que sus referencias están en un formato natural.
    """
    linea = definicion
    m = re.search(']{'+entrada_bibtex.identificador+'}', definicion)
    if m!=None: #Sólo hay que hacer las transformación si la entrada de bibtex está presente en la definición.
       linea = re.sub('\[', '[véase el ', linea)
       linea = re.sub(']{'+entrada_bibtex.identificador+'}', ' del ' + entrada_bibtex.titulo + ' 00(' + entrada_bibtex.uri + ')00', linea)
       linea = re.sub('\[','(', linea)
       linea = re.sub('\]',')', linea)
       linea = re.sub('00\(','[', linea)
       linea = re.sub('\)00', '])', linea)
    return linea

def obtener_uri_de_latex(instruccion_url):
    """
       Obtiene una uri a partir de una instrucción url de LaTex (obsérvese que a la url recibida se le ha quitado el símbolo '\')

       :param instruccion_url: instrucción de LaTex, pero sin el símbolo '\'.
       :return: la uri en formato estándar de la Web.
    """
    return re.search('(?<=url{).+?}', instruccion_url).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy

def transformar_string_entrada_bibtex(string_entrada_bibtex):
    """
       Transforma una entrada del estilo de las que se pueden encontrar en el fichero diccionario_bib.dic en una
       tupla del tipo EntradaBibTex. Para ver su uso, puede consultarse la función extraer_referencias().

       :param: string_entrada_bibtex: entrada del estilo de las que se pueden encontrar en el fichero diccionario_bib.dic.
       :return tupla del tipo EntradaBibTex.
    """
    identificador = re.search('(?<=inicio{).+?,', string_entrada_bibtex).group()[:-1]
    titulo = re.search('(?<=title = {).+?}', string_entrada_bibtex).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy
    nota = re.search('(?<=note = ").+?"', string_entrada_bibtex).group()[:-1] # La última interrogación se utiliza para indicare que es non-greedy
    uri = obtener_uri_de_latex(nota)
    ebt = EntradaBibTex(identificador, titulo, uri)
    return ebt 

def elimina_tildes(cadena): #función inspirada en https://gist.github.com/victorono/7633010
    """
       Elimina tildes de una cadena de caracteres. Se utiliza para generar la URI de una entidad a partir de su etiqueta.

       :param: cadena: Cadena de caracteres que puede tener tildes.
       :return: Cadena de caracteres sin tildes.
    """
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s

def generar_uri(etiqueta):
    """
       Genera la URI de la entidad a partir de su etiqueta.

       :param: etiqueta: la etiqueta de la entidad.
       :return: la URI de la entidad.
    """
    etiqueta_sin_tildes = elimina_tildes(etiqueta)
    lista_palabras = etiqueta_sin_tildes.split()
    palabra_en_mayuscula = ''
    for palabra in lista_palabras:
        palabra_en_mayuscula = palabra_en_mayuscula+''.join((palabra[0].upper(),palabra[1:]))
    return 'http://w3id.org/education/otn#' + palabra_en_mayuscula 

def generar_ontologia(datos_leidos):
    """
       A partir de una cadena de caractares leída de un glosario que sigue el formato de glosario_mod_1.tex,
       genera una ontología en OWL. El resultado lo escribe en el fichero ontologia.owl.

       :param: datos_leidos: cadena de caractares leída de un glosario que sigue el formato de glosario_mod_1.tex.
    """
    ebs = extraer_referencias()
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
                 definicion = next(itDef)
                 definicion_con_referencias = explotar_referencias_en_definicion(definicion, ebs)
                 g.write('   <rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">'+definicion_con_referencias+'</rdfs:comment>\n')
                 g.write('   <rdfs:label xml:lang="es">'+etiqueta+'</rdfs:label>\n')
                 g.write('</owl:Class>\n\n')
         except StopIteration:
              pass
         g.write('</rdf:RDF>')
         g.closed

def obtener_anotaciones(cadena, obtener_anotacion, recorte):
    """
       Obtiene, a partir de una cadena leída de un fichero con un formato similar al de glosario_mod_1.tex,
       utilizando la función obtener_anotacion, bien sea una etiqueta, bien sea una definición. Si se trata de una
       etiqueta, obtener_anotacion será obtener_etiqueta y, si se trata de una definición, obtener_anotacion
       será obtener_definicion. El recorte indica cuántos caracteres sobran del final de la cadena. En el caso de
       las etiquetas, hay que quitar un carácter y, en el caso de las definciones, hay que quitar tres caracteres.

       param: cadena: cadena leída de un fichero con un formato similar al de glosario_mod_1.tex.
       param: cadena: obtener_anotacion: función para obtener la etiqueta o la definición, según el caso.
       return: la anotación, que puede ser una etiqueta o una definición.
    """
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
    """
       Obtiene una etiqueta a partir de una definición de un término de la ontología en LaTeX. Se puede consultar
       el fichero glosario_mod_1.tex para comprobar el formato.

       param: cadena: definición de un término de la ontología en LaTeX.
       return: la etiqueta del término.
    """
    m = re.search('(?<=\\emph{).+?}', cadena) # La última interrogación se utiliza para indicare que es non-greedy
    return m

def obtener_definicion(cadena):
    """
       Obtiene una definición a partir de una definición de un término de la ontología en LaTeX. Se puede consultar
       el fichero glosario_mod_1.tex para comprobar el formato.

       param: cadena: definición de un término de la ontología en LaTeX.
       return: la etiqueta del término.
    """
    m = re.search('(?<=<<<).+?>>>', cadena)
    return m

with open('glosario_mod_1.tex') as f:
    datos_leidos = f.read()
    f.closed
generar_ontologia(datos_leidos)
