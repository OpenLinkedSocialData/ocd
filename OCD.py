#!/usr/bin/python
#-*- coding: utf-8 -*-
import rdflib as r, time
from SPARQLWrapper import SPARQLWrapper, JSON

T=time.time()
#g = r.Graph()
#g.load("cdTriplestore.rdf")
#print time.time()-T

# mais de 4 minutos para carregar
#ss=set([s for s in g.subjects()])
#len(ss)
#oo=set([s for s in g.objects()])
#len(ss)
#len(oo)
#pp=set([s for s in g.predicates()])

#classes=g.objects(predicate=r.RDF.type)
# classes que apareceram na triplificacao dos dados
#classes_=set([cc for cc in classes])
#properties=set([s for s in g.predicates()])

propriedades=[r.term.URIRef(u'http://purl.org/socialparticipation/ocd/commentCount'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/cep'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/commentBody'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/supporter'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/contact'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/start'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/tagger'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/partners'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/mbox'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/tagged'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/relatedOntology'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/inspirationCount'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/commentType'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/abreviation'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/state'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/text'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/author'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/neighborhood'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/image'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/relevance'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/description'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/contentType'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/size'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/authorDescription'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/ip'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/supportCount'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/longDescription'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/offerer'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/birthday'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/emailTrigger'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/city'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/competition'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/height'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/user'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/userDescription'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/updated'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/phone'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/followersCount'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/status'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/filename'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/regulation'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/tag'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/width'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/created'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/shortDescription'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/name'),
     r.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/caption'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/software'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/type'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/fax'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/url'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/awards'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/deleted'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/responsible'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/gender'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/title'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/site'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/articleBody'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/topic')]
classes=[r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Login'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Problem'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Triplestore'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Image'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Inspiration'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Neighborhood'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Tag'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Post'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Observatory'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Comment'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Competition'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/State'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Proposal'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Tagging'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/MacroTag'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Place'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Support'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/City'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Prize'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/Link'),
     r.term.URIRef(u'http://purl.org/socialparticipation/ocd/User')]
print time.time()-T

####
# Roteiro de métodos para construção da ontologia baseada nos dados
# data driven ontology

# 0) Triplifica conforme triplificaCD.py
# usa nomes mínimos para propriedades e classes como :body ou :name, classes como
# commentBody ou userName devem ser evitadas
# na triplificação. Podendo ser observadas e adicionadas
# no levantamento da ontologia.

# FEITO

# 0.5) Coloca dados triplificados num endpoint sparql para fazer as queries necessárias
# para o levantamento da ontologia.

# FEITO

# 1) Obtencao de todas as classes
# ?o where { ?s rdf:type ?o }
# com algumas excessoes
PREFIX="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ops: <http://purl.org/socialparticipation/ops#>
PREFIX opa: <http://purl.org/socialparticipation/opa#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcty: <http://purl.org/dc/dcmitype/>
PREFIX tsioc: <http://rdfs.org/sioc/types#>
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX schema: <http://schema.org/>
PREFIX aa: <http://purl.org/socialparticipation/aa/>
PREFIX ocd: <http://purl.org/socialparticipation/ocd/>"""

q="SELECT DISTINCT ?o WHERE {?s rdf:type ?o}"
NOW=time.time()
#sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query")
sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
sparql.setQuery(PREFIX+q)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("%.2f segundos para puxar todas as classes"%
      (time.time()-NOW,))
classes=[i["o"]["value"] for i in results["results"]["bindings"] if "w3.org" not in i["o"]["value"]]

# 2) Obtem todas as propriedades
# ?p where { ?s ?p ?o. }
# com algumas excessoes
q="SELECT DISTINCT ?p WHERE {?s ?p ?o}"
NOW=time.time()
#sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query")
sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
sparql.setQuery(PREFIX+q)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("%.2f segundos para puxar todas as propriedades"%
      (time.time()-NOW,))
#props_=[i["p"]["value"] for i in results["results"]["bindings"]]
props=[i["p"]["value"] for i in results["results"]["bindings"] if "w3.org" not in i["p"]["value"]]

# 3) Faz estrutura para cada classe e uma figura:
# classe no meio, dados à esquerda, classes à direita
# para cada classe, para cada individuo da classe,
# ver as relacoes estabelecidas com o individuo como
# sujeito e como objeto. Anotar a propriedade e o tipo de dado
# na ponta
# guarda a estrutura de relacionamento da classe.

# buscar todas as distintas propriedades 
#foo={}
#for classe in classes:
#    q=("SELECT DISTINCT ?p WHERE { ?i a <%s> . ?i ?p ?o }"%(classe,))
#    NOW=time.time()
#    #sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query")
#    sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
#    sparql.setQuery(PREFIX+q)
#    sparql.setReturnFormat(JSON)
#    results = sparql.query().convert()
#    propsc=[i["p"]["value"] for i in results["results"]["bindings"]]
#    print("%.2f segundos para puxar as propriedades consequentes"%(time.time()-NOW,))
#    q=("SELECT DISTINCT ?p WHERE { ?i a <%s> . ?s ?p ?i }"%(classe,))
#    NOW=time.time()
#    sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
#    sparql.setQuery(PREFIX+q)
#    sparql.setReturnFormat(JSON)
#    results = sparql.query().convert()
#    propsa=[i["p"]["value"] for i in results["results"]["bindings"]]
#    print("%.2f segundos para puxar as propriedades antecedentes"%(time.time()-NOW,))
#    foo[classe]=[propsa,propsc]
## faz figuras
def fazQuery(query):
    NOW=time.time()
    #sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query")
    sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
    sparql.setQuery(PREFIX+query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print time.time()-NOW
    return results["results"]["bindings"]

vizinhanca={}
for classe in classes[:3]:
    #res=fazQuery("SELECT DISTINCT ?p (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?p ?o }"%(classe,))
    NOW=time.time()
    print "\nant:"
    ant=fazQuery("SELECT DISTINCT ?p ?co (datatype(?o) as ?do) WHERE { ?i a <%s> . ?s ?p ?i . OPTIONAL { ?s a ?co . } }"%(classe,))
    print "cons:"
    cons=fazQuery("SELECT DISTINCT ?p ?co (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?p ?o . OPTIONAL { ?o a ?co . } }"%(classe,))
    vizinhanca[classe]=(ant,cons)
    #sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query")
    #sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
    #sparql.setQuery(PREFIX+q)
    #sparql.setReturnFormat(JSON)
    #results = sparql.query().convert()


# 4) Faz estrutura geral e figura geral

# 5) Observando as triplas, observar conceitos especificos do namespace,
# como commentBody e userName. Esta parte pode ser pulada para deixar
# a inferência mais leve e o namespace menos populoso.

# 6) As propriedades são qualificadas e as restrições de classe aplicadas.
# Enriquece figura

# 7) O namespace é relacionado com namespaces externos através de: super classes e propriedades, e equivalentes classes e propriedades.
# enriquece figura

# 8) Escreve OWL, TTL e PNG

# 9) Sobe no endpoint para mais testes

