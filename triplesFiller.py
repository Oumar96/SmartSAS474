'''Python programs that can transform the dataset into RDF triples. '''

import sqlite3

conn = sqlite3.connect('courses.sqlite')

#base='';
#ConcordiaHomepage="https://www.concordia.ca/"
#dbr: Concordia_University

#read URIs annotations
#ex:'URI': 'http://dbpedia.org/resource/Presidency_of_Barack_Obama',

Prefixes = {'owl':'<https://www.w3.org/2002/07/owl#>', 'foaf':'<http://xmlns.com/foaf/0.1/>', 'rdfs':'<https://www.w3.org/2000/01/rdf-schema#>', 'rdf':'<https://www.w3.org/1999/02/22-rdf-syntax-ns#>', 'focu':'<http://focu.io/schema#>', 'xsd':'<http://www.w3.org/2001/XMLSchema#>'}

#classes
classes=['focu:Course','focu:Grade','focu:courseTopics']
subclasses={'focu:University':'foaf:Organization','focu:Student':'foaf:Person'}
props=['foaf:name', 'foaf:schoolHomepage','foaf:familyName','foaf:givenName','foaf:mbox','focu:IDNumber', 'focu:courseName', 'focu:courseSubject', 'focu:courseNumber','focus:courseDescription']
propsDomRange = {'focu:isEnrolledAt': ['focu:Student','focu:University'], 'focu:completedCourseGrade':['focu:Student','focu:Grade'] ,'focu:takesCourse':['focu:Student','focu:Course'],'focu:hasTopics':['focu:courseDescription','focu:courseTopics']}

triples='BASE <http://example.org/>\n'

for key, value in Prefixes.items():
    triples += ("@prefix {}: {} .\n".format(key, value))

triples +='\n'

for c in classes:
    triples += c + ' a rdfs:Class .\n'

for c,sbc in subclasses.items():
    triples += (c + ' a rdfs:Class ;\n'
                + '\t rdfs:subClassOf {} .\n'.format(sbc))
triples +='\n'

for prop in props:
    triples += prop + ' a rdf:Property .\n'

triples +='\n'

for prop, domran in propsDomRange.items():
    triples += (prop + ' a rdf:Property ;\n'
                + '\t rdfs:domain {} ;\n\t rdfs:range {} .\n'.format(domran[0], domran[1]))
triples +='\n'



cursor = conn.execute("SELECT * from courses")
course=''
for row in cursor:
   #print (row[0],row[1],row[2])
    course=row[0].split()
    triples+=('<{}> a focu:Course;\n'.format(row[0])
            + '\t focu:courseSubject {} ;\n'.format(course[0])
            + '\t focu:courseNumber {} ;\n'.format(course[1])
            + '\t focu:courseName {} ;\n'.format(row[2])
            +'\t focu:courseDescription {} .\n'.format(row[3]))
           # +hasTopics

print(triples);
conn.close()

'''with open('triples.txt', 'wb') as file:
    file.write(triples)'''

