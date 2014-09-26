#!/usr/bin/python
#-*- coding: utf-8 -*-
import rdflib as r
import _mysql
import time
from dateutil.parser import parse
T=time.time()
db=_mysql.connect(user="root",passwd="foobar",db="cd")
db.query("SET NAMES 'utf8'")
db.query('SET character_set_connection=utf8')
db.query('SET character_set_client=utf8')
db.query('SET character_set_results=utf8')

db.query("show tables;")
res=db.store_result()
tables=[res.fetch_row()[0][0] for i in xrange(res.num_rows())]

d={}
for tt in tables:
    db.query("select column_name from information_schema.columns where table_name='%s';"%(tt,))
    res=db.store_result()
    d["h"+tt]=[res.fetch_row()[0][0] for i in xrange(res.num_rows())]
    db.query("select * from %s;"%(tt,))
    res=db.store_result()
    d[tt]=[res.fetch_row()[0] for i in xrange(res.num_rows())]

g = r.Graph()
g.namespace_manager.bind("xsd", r.namespace.XSD)    
g.namespace_manager.bind("ocd", "http://purl.org/socialparticipation/ocd/")    
rdf = r.namespace.RDF
ocd = r.Namespace("http://purl.org/socialparticipation/ocd/")
xsd = r.namespace.XSD

# triplifica users
ocdp=ocd.User
du={}
for user in d["users"]:
    uid=user[0]
    email=user[3]
    created=user[6]
    updated=user[7]
    state=user[12]
    deleted=user[13]
    ttype=user[14]
    du[uid]=(email,created,updated)

    uri=ocdp+"#"+uid
    g.add((uri,rdf.type,ocdp))
    g.add((uri,ocd.mbox,r.URIRef("mailto:%s"%(email,))))
    g.add((uri,ocd.created,r.Literal(parse(created))))
    if updated != created:
        g.add((uri,ocd.updated,r.Literal(parse(updated))))
    g.add((uri,ocd.status,r.Literal(state)))
    if deleted:
        g.add((uri,ocd.deleted,r.Literal(parse(deleted))))
    g.add((uri,ocd.type,r.Literal(ttype)))
foo=[]
contac=0
contau=0
for userd in d["user_dados"]:
    uid=userd[1]
    nome=userd[2]
    fone=userd[3]
    # email=userd[4] priorizado o email da tabela users
    site=userd[5]
    desc=userd[6]
    gen=userd[7]
    ani=userd[8]
    fax=userd[9]
    created=userd[10]
    updated=userd[11]

    uri=ocdp+"#"+uid
    g.add((uri,ocd.name,r.Literal(nome)))
    g.add((uri,ocd.phone,r.Literal(fone)))
#    try:
#        if du[uid][0]!=email:
#            print "diferente"
#            print "1: %s, 2: %s"%(du[uid][0],email)
#    except:
#        print "usuario existe no user_dados mas nao no users"
#        foo.append(uid)
    g.add((uri,ocd.site,r.Literal(site)))
    g.add((uri,ocd.userDescription,r.Literal(desc)))
    g.add((uri,ocd.gender,r.Literal(gen)))
    if ani:
        g.add((uri,ocd.birthday,r.Literal(parse(ani))))
    g.add((uri,ocd.fax,r.Literal(fax)))
    try:
        if created==du[uid][1]:
            print "criado certin"
        else:
            contac+=1
            print "criacao n bate"
        if updated==du[uid][2]:
            print "updated certin"
        else:
            contau+=1
            print "update n bate"
    except:
        print uid

# posts
def G(S,P,O):
    g.add((S,P,O))
dp={}
for topico in d["topicos"]:
    # ttype,uid,titulo,desc,slug,created,updated,ccomment, cadesoes,relevancia,cseguidores,competition_id=topico[1:5]+topico[7:14]+topico[15:]
    ttype=topico[1] # ["Proposta" ou "Problema"] # OK
    # Criadas classes para Proposta e problema TTM
    # Para os especialistas qualificarem
    uid=topico[2] # co+2 'user_id', parecemments
    titulo=topico[3] # OK
    desc=topico[4] # OK
    slug=topico[7]  # OK
    created=topico[8] # OK
    updated=topico[9] # OK
    ccomments=topico[10] # OK
    cadesoes=topico[11] # OK
    relevancia=topico[12] # OK
    cseguidores=topico[13] # OK
    competition_id=topico[15] # OK

    uri=ocd.Post+"#"+slug.decode("utf-8")
    dp[topico[0]]=uri
    G(uri,rdf.type,ocd.Post)
    if ttype=="Proposta":
        G(uri,rdf.type,ocd.Proposal)
    elif ttype=="Problema":
        G(uri,rdf.type,ocd.Problem)
    else:
        print u"tipo de postagem não identificada"
    G(uri,ocd.title,r.Literal(titulo))
    G(uri,ocd.articleBody,r.Literal(desc))
    G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
    G(uri,ocd.commentCount, r.Literal(ccomments))
    G(uri,ocd.supportCount,r.Literal(cadesoes))
    G(uri,ocd.relevance,r.Literal(relevancia))
    G(uri,ocd.followersCount,r.Literal(cseguidores))
    if competition_id: # Vínculo com Competition
        uri_=ocd.Competition+"#"+competition_id
        G(uri,ocd.competition,uri_)
    
# Tabela Comments
for comment in d["comments"]:
    cid=comment[0] # Ok.
    tid=comment[1] # opis eh tudo topic
    body=comment[3] # OK.
    uid=comment[4] # OK.
    ttype=comment[8] # Ok.
    created=comment[9] # OK.
    updated=comment[10] # Ok.
    uri=ocd.Comment+"#"+cid
    G(uri,rdf.type,ocd.Comment)
    if body:
        G(uri,ocd.commentBody,r.Literal(body))
    uri_u=ocdp+"#"+uid
    G(uri,ocd.author,uri_u)
    G(uri,ocd.commentType,r.Literal(ttype))
    G(uri,ocd.created,r.Literal(parse(created)))
    if updated!=created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
    
# Tabela Competitions    
for competition in d["competitions"]:
    coid=competition[0] # OK.
    sdesc=competition[1] # OK.
    created=competition[3] # Ok.
    updated=competition[4] # Ok.
    start=competition[5]   # Ok.
    title=competition[11] # Ok.
    ldesc=competition[14] # Ok.
    adesc=competition[15] # Ok.
    reg=competition[16] # Ok.
    aw=competition[17] # Ok.
    part=competition[18] # Ok.

    uri=ocd.Competition+"#"+coid
    G(uri,rdf.type,ocd.Competition)
    G(uri,ocd.shortDescription,r.Literal(sdesc))
    G(uri,ocd.created,r.Literal(parse(created)))
    if created != updated:
        G(uri,ocd.created,r.Literal(parse(created)))
    if start:
        G(uri,ocd.start,r.Literal(parse(start)))
    G(uri,ocd.competitionName,r.Literal(title))
    G(uri,ocd.longDescription,r.Literal(ldesc))
    G(uri,ocd.authorDescription,r.Literal(adesc))
    G(uri,ocd.regulation,r.Literal(reg))
    G(uri,ocd.awards,r.Literal(aw))
    G(uri,ocd.partners,r.Literal(part))
    
# taggings
for tag in d["tags"]:
    

# triplificar as relevâncias
print time.time()-T
