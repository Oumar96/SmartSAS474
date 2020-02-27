'''Python programs that can transform the dataset into RDF triples. '''

import sqlite3
import spotlight
import requests
import json
from collections import defaultdict
conn = sqlite3.connect('courses.sqlite')


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

for c, sbc in subclasses.items():
    triples += (c + ' a rdfs:Class ;\n'
                + '\t rdfs:subClassOf {} .\n'.format(sbc))
triples +='\n'

for prop in props:
    triples += prop + ' a rdf:Property .\n'

triples += '\n'

for prop, domran in propsDomRange.items():
    triples += (prop + ' a rdf:Property ;\n'
                + '\t rdfs:domain {} ;\n\t rdfs:range {} .\n'.format(domran[0], domran[1]))
triples +='\n'


apiPrefix = "https://api.dbpedia-spotlight.org/en/annotate?text="
headers = {'accept': 'application/json'}
cursor = conn.execute("SELECT * from courses")

for row in cursor:
    course = row[0].split()
    description = row[3]

    ''' response bugs in this section
    URL = apiPrefix + description
    try:
        response = requests.get(url=URL, headers=headers)
        responseDict = response.json()
        annotations = []
        for resources in responseDict['Resources']:
            annotations.append(resources['@URI'])
    except KeyError: #requests.exceptions.RequestException:
        print('skipped3', responseDict)
        pass'''

    triples+=('<{}> a focu:Course;\n'.format(row[0])
            + '\t focu:courseSubject {} ;\n'.format(course[0])
            + '\t focu:courseNumber {} ;\n'.format(course[1])
            + '\t focu:courseName {} ;\n'.format(row[2])
            +'\t focu:courseDescription {} ;\n'.format(row[3]))

    ''' formating for topics
    try:
        for a in range(len(annotations)-1):
            triples +='\t focu:hasTopics {} ;\n'.format(a)
            triples += '\t focu:hasTopics {} .\n'.format(annotations[len(annotations) - 1])
    except IndexError:
        pass'''

print(triples)

conn.close()



'''************ working test with last description ************'''
URL = apiPrefix + description
response = requests.get(url=URL,headers=headers)
responseDict = response.json()
annotations = []

#print nested dictionnary of resources and storing them into annotations
for resources in responseDict['Resources']:
    try:
        annotations.append(resources['@URI'])
    except KeyError:
        pass
print('annotation test\n',annotations)
'''*******************************************'''


'''with open('triples.txt', 'wb') as file:
    file.write(triples)'''


''' ********* failed exception handling ********** 
 try:
        response = requests.get(url=URL, headers=headers)
        responseDict = response.json()
        annotations = []
        try:
            for resources in responseDict['Resources']:
                try:
                    annotations.append(resources['@URI'])
                except KeyError:
                    print('skipped1',resources['@URI'])
                    pass
        except KeyError:
            print('skipped2',responseDict['Resources'])
            pass
    except: #requests.exceptions.RequestException:
        print('skipped3', responseDict)
        pass
__________________________________________________________'''

''' prints annotations and other data in Resources dict key
    try:
        print(responseDict['Resources'])
    except KeyError:
        pass
    '''



'''using spotlight package but request fails
URL = apiPrefix + description
r = requests.get(url=URL, headers=headers)
annotations = spotlight.annotate(apiPrefix, description, confidence=0.4, support=20)'''