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

def G(S,P,O):
    g.add((S,P,O))

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
    relevance=user[20]
    insp_count=user[30]
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
    g.add((uri,ocd.relevance,r.Literal(relevance)))
    if insp_count:
        g.add((uri,ocd.inspirationCount,r.Literal(insp_count)))
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
    G(uri,ocd.topic,dp[tid])
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
    G(uri,ocd.name,r.Literal(title))
    G(uri,ocd.longDescription,r.Literal(ldesc))
    G(uri,ocd.authorDescription,r.Literal(adesc))
    G(uri,ocd.regulation,r.Literal(reg))
    G(uri,ocd.awards,r.Literal(aw))
    G(uri,ocd.partners,r.Literal(part))
for prize in d["competition_prizes"]:
    pid=prize[0] # ok.
    name=prize[1] # ok.
    description=prize[2] # ok.
    competition_id=prize[3] # ok.
    offerer_id=prize[4] # ok.
    tid=winning_topic_id=prize[5] # ok.
    created_at=prize[6] # ok.
    updated_at=prize[7] # ok.

    uri=ocd.Prize+"#"+pid
    G(uri,rdf.type,ocd.Prize)
    G(uri,ocd.name,r.Literal(name))
    G(uri,ocd.description,r.Literal(desc))
    uri_=ocd.Competition+"#"+coid
    G(uri,ocd.competition,uri_)
    G(uri,ocd.topic,dp[tid])
    G(uri,ocd.offerer,ocd.User+"#"+offerer_id)

    

    G(uri,ocd.created,r.Literal(parse(created)))
    if updated!=created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
    
# Tags
for tag in d["tags"]:
    tid=tag[0] # Ok.
    tag_=tag[1] # Ok.
    relevancia=tag[2] # ok.

    uri=ocd.Tag+"#"+tid
    G(uri,rdf.type,ocd.Tag)
    G(uri,ocd.text,r.Literal(tag_))
    G(uri,ocd.relevance,r.Literal(relevancia))

# e taggings
for tagging in d["taggings"]:
    tid_=tagging[0] #tagging Ok.
    tid=tagging[1] #tag Ok.
    toid=tagging[2] #topic Ok.
    uid=tagging[3] #user Ok.
    utype=tagging[4] # ok.
    ttype=tagging[5] # ok.
    created=tagging[7] # ok.

    uri=ocd.Tagging+"#"+tid_
    G(uri,rdf.type,ocd.Tagging)
    G(uri,ocd.tag,ocd.Tag+"#"+tid)
    if utype:
        G(uri,ocd.tagger,ocdp+"#"+uid)
    if ttype=="Topico":
        G(uri,ocd.tagged,dp[toid])
    else:
        G(uri,ocd.tagged,ocd.Macrotag+"#"+toid)
    G(uri,ocd.created,r.Literal(parse(created)))

de={}
for estado in d["estados"]:
    eid=estado[0]
    nome=estado[1] # ok
    abr=estado[2] # ok
    created=estado[3] # ok.
    updated=estado[4] # ok.
    relevance=estado[5] # ok.

    uri=ocd.State+"#"+abr
    de[eid]=uri
    G(uri,rdf.type,ocd.State)
    G(uri,ocd.abreviation,r.Literal(abr))
    G(uri,ocd.name,r.Literal(name))
    G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
    G(uri,ocd.relevance,r.Literal(relevance))

dc={}
for cidade in d["cidades"]:
    cid=cidade[0]
    nome=cidade[1] # ok.
    eid=cidade[2] # estado ok.
    slug=cidade[3] # ok.
    created=cidade[4] # ok.
    updated=cidade[5] # ok.
    relevance=cidade[6] # ok.

    uri=ocd.City+"#"+slug
    dc[cid]=uri
    G(uri,rdf.type,ocd.City)
    G(uri,ocd.state,de[eid])
    G(uri,ocd.name,r.Literal(nome))
    G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
    G(uri,ocd.relevance,r.Literal(relevance))

for bairro in d["bairros"]:
    bid=bairro[0] # ok.
    nome=bairro[1] # ok.
    cid=bairro[2] # ok.
    created=bairro[3] # ok.
    updated=bairro[4] # ok.
    relevance=bairro[5] # ok.

    uri=ocd.Neighborhood+"#"+bid
    G(uri,rdf.type,ocd.Neighborhood)
    if nome:
        G(uri,ocd.name,r.Literal(nome))
    G(uri,ocd.city,dc[cid])

    G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
    G(uri,ocd.relevance,r.Literal(relevance))

# locais -
for local in d["locais"]:
    lid=local[0] # ok.
    rid=local[1]
    rtype=local[2]
    bid=local[3] # ok.
    cid=local[4] # ok.
    created=local[7] # ok.
    updated=local[8] # ok.
    cep=local[9] # ok.
    eid=local[10] # ok.

    uri=ocd.Place+"#"+lid
    G(uri,rdf.type,ocd.Place)
    if cep:
        G(uri,ocd.cep,r.Literal(cep))
    if eid:
        G(uri,ocd.state,de[eid])
    if cid:
        G(uri,ocd.city,dc[cid])
    if bid:
        G(uri,ocd.neighborhood,ocd.Neighborhood+"#"+bid)
    if rtype=="Topico":
        uri_=dp[rid]
    elif rtype=="User":
        uri_=ocd.User+"#"+rid
    elif rtype=="Competition":
        uri_=ocd.Competition+"#"+rid
    elif rtype=="Observatorio":
        uri_=ocd.Observatory+"#"+rid
    if rtype:
        G(uri,ocd.responsible,uri_)
    if created:
        G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
for adesao in d["adesoes"]:
    tid=adesao[0] # ok.
    uid=adesao[1] # ok.
    created=adesao[2]
    updated=adesao[3]
    aid=adesao[4] # ok.

    uri=ocd.Support+"#"+aid
    G(uri,rdf.type,ocd.Support)
    G(uri,ocd.topic,dp[tid])
    G(uri,ocd.supporter,ocd.User+"#"+rid)

    G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
for link in d['links']:
    lid=link[0]
    nome=link[1]
    url=link[2]
    tid=link[4]
    created=link[5]
    updated=link[6]

    uri=ocd.Link+"#"+lid
    G(uri,rdf.type,ocd.Link)
    G(uri,ocd.description,r.Literal(nome))
    G(uri,ocd.url,r.Literal(url))
    if tid:
        G(uri,ocd.topic,dp[tid])
    if created:
        G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
for observatorio in d["observatorios"]:
    oid=observatorio[0]
    uid=observatorio[1]
    recebe_email=observatorio[3]
    created=observatorio[4]
    updated=observatorio[5]

    uri=ocd.Observatory+"#"+oid
    G(uri,rdf.type,ocd.Observatory)
    G(uri,ocd.user,ocd.User+"#"+uid)
    G(uri,ocd.emailTrigger,r.Literal(recebe_email))
    G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))
for ot in d["observatorios_tem_tags"]:
    oid=ot[0]
    tid=ot[1]
    uri=ocd.Observatory+"#"+oid
    uri_=ocd.Tag+"#"+tid
    G(uri_,ocd.tagged,uri)
for login in d["historico_de_logins"]:
    lid=login[0] # ok.
    uid=login[1] # ok.
    created=login[2] # ok.
    ip=login[3] # ok.
    uri=ocd.Login+"#"+lid
    G(uri,rdf.type,ocd.Login)
    G(uri,ocd.user,ocd.User+"#"+uid)
    G(uri,ocd.created,r.Literal(parse(created)))
    G(uri,ocd.ip,r.Literal(ip))
for inspiration in d["inspirations"]:
    iid=inspiration[0] # ok.
    cid=inspiration[1] # ok.
    desc=inspiration[2]  # ok.
    created=inspiration[3] # ok.
    updated=inspiration[4] # ok.
    image=inspiration[5] # ok.
    uid=inspiration[6] # ok.
    title=inspiration[7] # ok.

    uri=ocd.Inspiration+"#"+iid
    G(uri,rdf.type,ocd.Inspiration)
    G(uri,ocd.competition,ocd.Competition+"#"+cid)
    G(uri,ocd.description,r.Literal(desc))
    G(uri,ocd.title,r.Literal(title))
    G(uri,ocd.user,ocd.User+"#"+uid)
    G(uri,ocd.image,r.Literal(image))
    G(uri,ocd.created,r.Literal(parse(created)))
    if updated!=created:
        G(uri,ocd.updated,r.Literal(parse(updated)))

for imagem in d["imagens"]:
    iid=imagem[0] # ok.
    rid=imagem[1] # ok.
    rtype=imagem[2] # ok.
    size=imagem[3]
    ctype=imagem[4]
    fname=imagem[5]
    height=imagem[6]
    width=imagem[7]
    legenda=imagem[11]
    created=imagem[12]
    updated=imagem[13]

    uri=ocd.Image+"#"+iid
    G(uri,rdf.type,pcd.Image)
    if rtype=="User":
        G(uri,ocd.responsible,ocd.User+"#"+rid)
    if rtype=="Topico":
        G(uri,ocd.responsible,ocd.Post+"#"+rid)
    if size:
        G(uri,ocd.size,r.Literal(size))
    if ctype:
        G(uri,ocd.contentType,r.Literal(ctype))
    if fname:
        G(uri,ocd.filename,r.Literal(fname))
    if height:
        G(uri,ocd.height,r.Literal(height))
    if width:
        G(uri,ocd.width,r.Literal(width))
    if legenda:
        G(uri,ocd.caption,r.Literal(legenda))

    G(uri,ocd.created,r.Literal(parse(created)))
    if updated != created:
        G(uri,ocd.updated,r.Literal(parse(updated)))



# macro_tags
# especificação de datai e demais informacoes da triplificacao
print time.time()-T
