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


#sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query") # com reasoner
