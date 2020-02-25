'''Python programs that can transform the dataset into RDF triples. '''

#base='';
#ConcordiaHomepage="https://www.concordia.ca/"

#read URIs annotations
#ex:'URI': 'http://dbpedia.org/resource/Presidency_of_Barack_Obama',

Prefixes = {'ex':'<http://example.org/>', 'owl':'<https://www.w3.org/2002/07/owl#>', 'foaf':'<http://xmlns.com/foaf/0.1/>', 'rdfs':'<https://www.w3.org/2000/01/rdf-schema#>', 'rdf':'<https://www.w3.org/1999/02/22-rdf-syntax-ns#>', 'focu':'<http://focu.io/schema#>', 'xsd':'<http://www.w3.org/2001/XMLSchema#>'}

#classes
classes=['focu:University','focu:Course','focu:Student','focu:Grade']
props=['foaf:name', 'foaf:schoolHomepage','foaf:familyName','foaf:givenName','foaf:mbox','focu:IDNumber', 'focu:CourseName', 'focu:CourseSubject', 'focu:courseNumber','focus:courseDescription']
propsDomRange = {'focu:isEnrolledAt': ['focu:Student','focu:University'], 'focu:completedCourseGrade':['focu:Student','focu:Grade'] ,'focu:takesCourse':['focu:Student','focu:Course']}
triples=''

for key, value in Prefixes.items():
    triples += ("@prefix {}: {} .\n".format(key, value))

for c in classes:
    triples += c + ' a rdfs:Class .\n'

for prop in props:
    triples += prop + ' a rdf:Property .\n'

triples +='\n'

for prop, domran in propsDomRange.items():
    triples += (prop + ' a rdf:Property ;\n'
                + '\t rdfs:domain {} ;\n\t rdfs:range {} .\n'.format(domran[0], domran[1]))

print(triples);

'''with open('triples.txt', 'wb') as file:
    file.write(triples)'''

