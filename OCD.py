#!/usr/bin/python
#-*- coding: utf-8 -*-
import cPickle as pickle, time
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib as r, pygraphviz as gv

# variaveis principais:
# classes (kk), props,
# vizinhanca_ (de classes)

T=time.time()
def fazQuery(query):
    NOW=time.time()
    #sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query")
    sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
    sparql.setQuery(PREFIX+query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print time.time()-NOW
    return results["results"]["bindings"]

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
sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
sparql.setQuery(PREFIX+q)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("%.2f segundos para puxar todas as propriedades"%
      (time.time()-NOW,))
props=[i["p"]["value"] for i in results["results"]["bindings"] if "w3.org" not in i["p"]["value"]]
props_=[i.split("/")[-1] for i in props]

# 3) Faz estrutura para cada classe e uma figura:
# classe no meio, dados à esquerda, classes à direita
# para cada classe, para cada individuo da classe,
# ver as relacoes estabelecidas com o individuo como
# sujeito e como objeto. Anotar a propriedade e o tipo de dado
# na ponta
# guarda a estrutura de relacionamento da classe.

# buscar todas as distintas propriedades 
classes_=foo={}
for classe in classes:
    q=("SELECT DISTINCT ?p WHERE { ?i a <%s> . ?i ?p ?o }"%(classe,))
    NOW=time.time()
    sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    propsc=[i["p"]["value"] for i in results["results"]["bindings"]]
    print("%.2f segundos para puxar as propriedades consequentes"%(time.time()-NOW,))
    q=("SELECT DISTINCT ?p WHERE { ?i a <%s> . ?s ?p ?i }"%(classe,))
    NOW=time.time()
    sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
    sparql.setQuery(PREFIX+q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    propsa=[i["p"]["value"] for i in results["results"]["bindings"]]
    print("%.2f segundos para puxar as propriedades antecedentes"%(time.time()-NOW,))
    classes_[classe]=foo[classe]=[propsa,propsc]
# faz figuras
vizinhanca={}
vizinhanca_={}
for classe in classes:
    #res=fazQuery("SELECT DISTINCT ?p (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?p ?o }"%(classe,))
    NOW=time.time()
    print("\n%s antecedente, consequente: "%(classe.split("/")[-1],))
    ant=fazQuery("SELECT DISTINCT ?p ?cs (datatype(?s) as ?ds) WHERE { ?i a <%s> . ?s ?p ?i . OPTIONAL { ?s a ?cs . } }"%(classe,))
    ant_=[]
    for aa in ant:
        if "cs" in aa.keys():
            tobj=aa["cs"]["value"]
            ant_.append((tobj,aa["p"]["value"]))
        elif (("ds" in aa.keys()) and ("w3.org" not in aa["p"]["value"])):
            tobj=aa["ds"]["value"]
            ant_.append((tobj,aa["p"]["value"]))
    cons=fazQuery("SELECT DISTINCT ?p ?co (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?p ?o . OPTIONAL { ?o a ?co . } }"%(classe,))
    cons_=[]
    for cc in cons:
        if "co" in cc.keys():
            tobj=cc["co"]["value"]
            cons_.append((cc["p"]["value"],tobj))
        elif (("do" in cc.keys()) and ("w3.org" not in cc["p"]["value"])):
            tobj=cc["do"]["value"]
            cons_.append((cc["p"]["value"],tobj))
        elif "/mbox" in cc["p"]["value"]:
            tobj="XMLSchema#anyURI"
            cons_.append((cc["p"]["value"],tobj))
    vizinhanca[classe]=(ant,cons)
    vizinhanca_[classe]=(ant_,cons_)
f=open("dumpVV.pickle","wb")
vv=(vizinhanca,vizinhanca_)
pickle.dump(vv,f)
f.close()
fo=open("dumpVV.pickle","rb")
vv_=pickle.load(fo)
fo.close()
kk=vv_[1].keys()
for tkey in kk:
    cl=tkey
    cl_=cl.split("/")[-1]
    print cl_
    ex=vv_[1][cl]
    A=gv.AGraph(directed=True)
    A.graph_attr["label"]=("classe: %s, no namespace interno: http://purl.org/socialparticipation/ocd/"%(cl_,))
    for i in xrange(len(ex[0])): # antecedentes
        label=ex[0][i][0].split("/")[-1]
        elabel=ex[0][i][1].split("/")[-1]
        print label, elabel
        A.add_node(label,style="filled")
        A.add_edge(label,cl_)
        e=A.get_edge(label,cl_)
        e.attr["label"]=elabel
        n=A.get_node(label)
        n.attr['color']="#A2F3D1"
    print("\n\n")
    for i in xrange(len(ex[1])): # consequentes
        label=ex[1][i][1].split("/")[-1]
        elabel=ex[1][i][0].split("/")[-1]
        print elabel, label
        if "XMLS" in label:
            label_=i
        else:
            label_=label
        A.add_node(label_,style="filled")
        A.add_edge(cl_,label_)
        e=A.get_edge(cl_,label_)
        e.attr["label"]=elabel
        n=A.get_node(label_)
        n.attr['label']=label
        if "XMLS" in label:
            n.attr['color']="#FFE4AA"
        else:
            n.attr['color']="#A2F3D1"
    n=A.get_node(cl_)
    n.attr['style']="filled"
    n.attr['color']="#6EAA91"
    nome=("imgs/classes/%s.png"%(cl_,))
    A.draw(nome,prog="dot") # draw to png using circo
    print("Wrote %s"%(nome,))

# 4) Faz estrutura geral e figura geral
A=gv.AGraph(directed=True)
A.graph_attr["label"]="Diagrama geral da OCD no namespace interno: http://purl.org/socialparticipation/ocd/"
ii=1
for tkey in kk:
    cl_=tkey.split("/")[-1]
    if cl_ not in A.nodes():
        A.add_node(cl_,style="filled")
        n=A.get_node(cl_)
        n.attr['color']="#A2F3D1"
    ex=vv_[1][tkey]
    for i in xrange(len(ex[0])):
        label=ex[0][i][0].split("/")[-1]
        elabel=ex[0][i][1].split("/")[-1]
        print elabel
        if label not in A.nodes():
            A.add_node(label,style="filled")
            n=A.get_node(label)
            n.attr['color']="#A2F3D1"
        A.add_edge(label,cl_)
        e=A.get_edge(label,cl_)
        e.attr["label"]=elabel
    print("\n\n")
    for i in xrange(len(ex[1])):
        label=ex[1][i][1].split("/")[-1]
        elabel=ex[1][i][0].split("/")[-1]
        print elabel, label
        if "XMLS" in label:
            label_=ii; ii+=1
            color="#FFE4AA"
        else:
            label_=label
            color="#A2F3D1"
        if label_ not in A.nodes():
            A.add_node(label_,style="filled")
            n=A.get_node(label_)
            n.attr['label']=label.split("#")[-1]
            n.attr['color']=color
        A.add_edge(cl_,label_)
        e=A.get_edge(cl_,label_)
        e.attr["label"]=elabel
        e.attr["color"]=color
        e.attr["penwidth"]=2
A.draw("OCD.png",prog="twopi",args="-Granksep=4")
A.draw("OCD2.png",prog="dot",args="-Granksep=.4 -Gsize='1000,1000'")
print("Wrote %s"%(nome,))

# 4.5) qualificar literais
## ok.

# 5) Observando as triplas, observar hierarquias e conceitos especificos do namespace,
# como commentBody e userName. Ver README.md.
owl = r.namespace.OWL
rdf = r.namespace.RDF
rdfs = r.namespace.RDFS
ocd = r.Namespace("http://purl.org/socialparticipation/ocd/")
xsd = r.namespace.XSD
g=r.Graph()
def G(S,P,O):
    global g
    g.add((S,P,O))
G(ocd.Problem, rdfs.subClassOf,ocd.Post)
G(ocd.Proposal, rdfs.subClassOf,ocd.Post)

G(ocd.supportCount, rdfs.subPropertyOf    ,ocd.counting)
G(ocd.inspirationCount, rdfs.subPropertyOf,ocd.counting)
G(ocd.commentCount, rdfs.subPropertyOf    ,ocd.counting)
G(ocd.followersCount, rdfs.subPropertyOf  ,ocd.counting)

# 6) As propriedades são qualificadas e as restrições de classe aplicadas.
# para cada propriedade, ver o que incide no domínio e no âmbito.
# Ao mesmo tempo, fazer os axiomas de classe

# 6.1) estrutura básica e figuras:
P={}
P_={}
import string
for prop in props:
    # observar todos os subjeitos com q ela ocorre
    # observar todos os objetos com que ela ocorre
    # fazer estrutura, plotar cada uma
    prop_=prop.split("/")[-1]
    suj=fazQuery("SELECT DISTINCT ?cs WHERE { ?s <%s> ?o . ?s a ?cs . }"%(prop,))
    obj=fazQuery("SELECT DISTINCT ?co (datatype(?o) as ?do) WHERE { ?s <%s> ?o . OPTIONAL { ?o a ?co . } }"%(prop,))
    P[prop_]=(suj,obj)
    A=gv.AGraph(directed=True)
    A.graph_attr["label"]=("propriedade: %s, no namespace interno: http://purl.org/socialparticipation/ocd/"%(prop_,))
#    A.add_node(1,style="filled")
#    A.add_node(2,style="filled")
    A.add_edge(1,2)
    e=A.get_edge(1,2)
    e.attr["label"]=prop_
    n1=A.get_node(1)
    n2=A.get_node(2)
    n1.attr['style']="filled"
    n2.attr['style']="filled"
    n1.attr['color']="blue"
    n2.attr['color']="red"
    # Agiliza tags dos sujeitos
    ts=[i["cs"]["value"].split("/")[-1] for i in suj]
    ls=string.join(ts,"<br />")
    print "ls: "+ls
    #n1.attr['label']=ls
    n1.attr['label']=("<%s>"%(ls,))
    # Agiliza tags dos objetos 
    if "mbox" in prop_:
        lo="XMLSchema#anyURI"
        to=[lo]
    else:
        to1=[i["co"]["value"].split("/")[-1] for i in obj if "co" in i.keys()]
        to2=[i["do"]["value"].split("/")[-1] for i in obj if "do" in i.keys()]
        to=to1+to2
        lo=string.join(to,"<br />")
    P_[prop_]=(ts,to)
    print "lo:"+lo
    n2.attr['label']=("<%s>"%(lo,))
    nome=("imgs/properties/%s.png"%(prop_,))
    A.draw(nome,prog="dot") # draw to png using circo
    print("Wrote %s"%(nome,))

# 6.2) qualificação das propriedades: range, domain e axioma de propriedade
# owl:ObjectProperty, owl:DatatypeProperty or owl:AnnotationProperty
propsD={}
for prop in props: propsD[prop]=0 # 1 quando propriedade estiver ok.
G(ocd.abbreviation, rdf.type, owl.DatatypeProperty)
G(ocd.abbreviation, rdf.type, owl.functionalProperty)
G(ocd.abbreviation, rdfs.range, xsd.string)
G(ocd.abbreviation, rdfs.domain, ocd.State)
propsD[ocd.abbreviation]=1


G(ocd.accountable, rdf.type, owl.ObjectProperty)
G(ocd.accountable, rdf.type, owl.functionalProperty)
B=r.BNode()
G(ocd.accountable, rdfs.range, B)
G(B, owl.unionOf, ocd.User)
G(B, owl.unionOf, ocd.Post)
G(B, owl.unionOf, ocd.Proposal)
G(B, owl.unionOf, ocd.Observatory)
G(B, owl.unionOf, ocd.Problem)
G(B, owl.unionOf, ocd.Competition)
B2=r.BNode()
G(ocd.accountable, rdfs.domain, B2)
G(B2, owl.unionOf, ocd.Place)
G(B2, owl.unionOf, ocd.Image)
propsD[ocd.accountable]=1

G(ocd.author, rdf.type, owl.ObjectProperty)
G(ocd.author, rdf.type, owl.functionalProperty)
G(ocd.author, rdfs.range, ocd.User)
B=r.BNode()
G(ocd.author, rdfs.domain, B)
G(B, owl.unionOf, ocd.Proposal)
G(B, owl.unionOf, ocd.Post)
G(B, owl.unionOf, ocd.Problem)
G(B, owl.unionOf, ocd.Comment)
G(B, owl.unionOf, ocd.Inspiration)
propsD[ocd.author]=1

G(ocd.authorDescription, rdf.type, owl.DatatypeProperty)
G(ocd.authorDescription, rdf.type, owl.functionalProperty)
G(ocd.authorDescription, rdfs.range, xsd.string)
G(ocd.authorDescription, rdfs.domain, ocd.Competition)

G(ocd.autoDescription, rdf.type, owl.DatatypeProperty)
G(ocd.autoDescription, rdf.type, owl.functionalProperty)
G(ocd.autoDescription, rdfs.range, xsd.string)
G(ocd.autoDescription, rdfs.domain, ocd.User)
for prop in props:
    if prop not in functionalBlackList:
        G(prop,rdf.type,owl.functionalProperty)
    ant,cons=P_[prop.split("/")[-1]]
    if len(cons) and ("XMLS" in cons[0]):
        G(prop, rdf.type, owl.DatatypeProperty)
    else:
        G(prop, rdf.type, owl.ObjectProperty)
    if len(ant)>1:
        B=r.BNode()
        G(prop, rdfs.domain, B)
        for ant_ in ant:
            G(B, owl.unionOf, ocd+ant_)
    elif ant:
        G(prop, rdfs.domain, ocd+ant[0])
        
    if len(cons)>1:
        B=r.BNode()
        G(prop, rdfs.range, B)
        for cons_ in cons:
            G(B, owl.unionOf, ocd+cons_)
    elif cons:
        G(prop, rdfs.domain, ocd+cons[0])
# restrições de classe

G(ocd.counting, rdfs.range,xsd.integer)
# 6.1) Enriquece figura

# Também pode ser pulada esta etapa para simplificar ontologia e evitar incompatibilidades com bancos de dados atualizados e maiores detalhes dados pelos especialitas.

# 7) O namespace é relacionado com namespaces externos através de: super classes e propriedades, e equivalentes classes e propriedades.
# enriquece figura

# 8) Escreve OWL, TTL e PNG

# 9) Sobe no endpoint para mais testes

# EXTRA: faz figura centrada na propriedade,
# Como foi feita para cada classe, mas centrada na propriedade
# Fazer também para cada literal.
print "total time: ", time.time()-T
