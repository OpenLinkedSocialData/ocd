#!/usr/bin/python
#-*- coding: utf-8 -*-
import rdflib as r
import _mysql
import time
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

# O número de logins não nulos é igual ao número de logins
# que são iguais ao email. Portanto, é usado somente o email.
print len([i[1] for i in d["users"] if i[1]]) == sum([i[1]==i[3]  for i in d["users"]])

print "tipos"
aa=[i[14] for i in d["users"] if i[14]]
print [(i,aa.count(i)) for i in set(aa)]
