'''Python programs that can transform the dataset into RDF triples. '''

import sqlite3
import spotlight
import requests
import json
from collections import defaultdict
from time import sleep
from itertools import islice

conn = sqlite3.connect('courses.sqlite')


Prefixes = {'owl':'<https://www.w3.org/2002/07/owl#>', 'foaf':'<http://xmlns.com/foaf/0.1/>', 'rdfs':'<https://www.w3.org/2000/01/rdf-schema#>', 'rdf':'<https://www.w3.org/1999/02/22-rdf-syntax-ns#>', 'focu':'<http://focu.io/schema#>', 'xsd':'<http://www.w3.org/2001/XMLSchema#>'}

#classes
classes=['focu:Course','focu:Grade','focu:courseTopics']
subclasses={'focu:University':'foaf:Organization','focu:Student':'foaf:Person'}
props=['foaf:name', 'foaf:schoolHomepage','foaf:familyName','foaf:givenName','foaf:mbox','focu:IDNumber', 'focu:courseName', 'focu:courseSubject', 'focu:courseNumber','focus:courseDescription']
propsDomRange = {'focu:isEnrolledAt': ['focu:Student','focu:University'], 'focu:completedCourseGrade':['focu:Student','focu:Grade'] ,'focu:takesCourse':['focu:Student','focu:Course'],'focu:hasTopics':['focu:courseDescription','focu:courseTopics']}

triples = 'BASE <http://example.org/>\n'

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

    triples+=('<{}> a focu:Course ;\n'.format(row[0])
            + '\t focu:courseSubject {} ;\n'.format(course[0])
            + '\t focu:courseNumber {} ;\n'.format(course[1])
            + '\t focu:courseName {} ;\n'.format(row[2])
            +'\t focu:courseDescription {} .\n'.format(row[3]))

    ''' formating for topics
    try:
        for a in range(len(annotations)-1):
            triples +='\t focu:hasTopics {} ;\n'.format(a)
            triples += '\t focu:hasTopics {} .\n'.format(annotations[len(annotations) - 1])
    except IndexError:
        pass'''

#print(triples)


'''************ working test with last description ************'''
#URL = apiPrefix + description
#responseDict = requests.get(url=URL,headers=headers).json()

#print nested dictionnary of resources and storing them into annotations

#cursor2 = conn.execute("SELECT * FROM courses")
#cursor2 = conn.execute("SELECT Course, Description FROM courses WHERE Description IS NOT NULL")
cursor2 = conn.execute("SELECT Course, Description FROM courses WHERE LENGTH(Description) > 15")
count=0
for row in cursor2:
    description = row[1]
    URL = apiPrefix + description
    #responseDict = requests.get(url=URL, headers=headers).json()
    responseDict = requests.get(url=URL, headers=headers)
    try:
        json_data = json.loads(responseDict.text)
        print(row[0])

        # print(json_data)
        if 'Resources' in json_data:
            # print(responseDict.get('Resources')[0]['@URI']) '''returns none if resource doesnt exist
            if len(json_data.get('Resources')) > 1:
                triples += ('<{}> focu:hasTopics {} ;\n'.format(row[0],json_data.get('Resources')[0]['@URI']))
                #print (json_data.get('Resources')) prints the whole Resources list
                #print('number of urls', len(json_data.get('Resources')))
                for urls in islice(json_data.get('Resources'), 1, len(json_data.get('Resources'))-1):
                    try:
                        #print('list of resources: ', urls.get('@URI'))  # test working properly
                        triples +='\t focu:hasTopics {} ;\n'.format(urls.get('@URI'))
                    except:
                        pass
                triples += '\t focu:hasTopics {} .\n'.format(json_data.get('Resources')[len(json_data.get('Resources'))-1].get('@URI'))
                #triples += '\t focu:hasTopics {} .\n'.format(urls.get('@URI'))
            else:
                triples += ('<{}> focu:hasTopics {} .\n'.format(row[0], json_data.get('Resources')[0]['@URI']))
    except:
        pass

    #sleep(1)
    count += 1
    if count == 30:
        break


#print(triples)
conn.close()

with open('triples.rdf','w', encoding='utf-8') as file:
    file.write(triples)


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