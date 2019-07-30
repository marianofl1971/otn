cp implementacion/otn.rdf implementacion/otn_sp.rdf
sed -i s@https://w3id.org/def/dul-dolce-zero-en-espannol@https://w3id.org/def/dul-es@g implementacion/otn_sp.rdf
sed -i s@http://www.ontologydesignpatterns.org/ont/dul/DUL.owl@https://w3id.org/def/dul-es@g implementacion/otn_sp.rdf
sed -i '/<\/rdf:RDF>/d' implementacion/otn_sp.rdf
cat implementacion/otn_sp.rdf implementacion/dul-nnapa.rdf > implementacion/otn_sp2.rdf
mv implementacion/otn_sp2.rdf implementacion/otn_sp.rdf
echo "</rdf:RDF>" >> implementacion/otn_sp.rdf
java -jar /home/mariano/investigacion/herramientas/widoco/widoco-1.4.1-jar-with-dependencies.jar -ontFile implementacion/otn_sp.rdf -outFolder documentacion -lang es
