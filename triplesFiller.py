'''Python programs that can transform the dataset into RDF triples. '''
import sqlite3
import spotlight
import requests
import json
from collections import defaultdict
from time import sleep
from itertools import islice

conn = sqlite3.connect('courses.sqlite')

triples = ""

top_of_rdf = open("focu.rdf", "r")
triples += top_of_rdf.read()

apiPrefix = "https://api.dbpedia-spotlight.org/en/annotate?text="
headers = {'accept': 'application/json'}
cursor = conn.execute("SELECT * from courses")

for row in cursor:
    course = row[0].replace(' ','').replace(',','').replace('*','')
    description = row[3].replace('\n', ' ').replace("\n\xa0\n"," ")
    triples+=('<{}> a focu:Course ;\n'.format(course)
            + '\t focu:courseSubject "{}" ;\n'.format(course[0])
            + '\t focu:courseNumber "{}" ;\n'.format(course[1])
            + '\t focu:courseName "{}" ;\n'.format(row[2])
            +'\t focu:courseDescription "{}" ;\n'.format(description)
            +'\t rdfs:label "{}"@en .\n'.format(course)
            +'focu:grade{} rdfs:subPropertyOf focu:Grades.\n'.format(course)
            )

cursor2 = conn.execute("SELECT Course, Description FROM courses WHERE LENGTH(Description) > 15")
count=0
for row in cursor2:
    print(count)
    print("=============================================")
    print("Course: ",row[0].replace(' ',''))
    print("Description: ", row[1])
    courseCode = row[0].replace(' ','')
    description = row[1].replace('\n', ' ').replace("\n\xa0\n"," ")
    URL = apiPrefix + description
    print("URL: ", URL)
    response_code=0
    responseDict = requests.get(url=URL, headers=headers)
    print(responseDict)
    print(responseDict.status_code)
    number_of_tries = 0
    while(responseDict.status_code != 200):
        sleep(2)
        number_of_tries += 1
        if(number_of_tries >= 3):
            sleep(120)
        print("===============Trying number",number_of_tries,"===========")
        responseDict = requests.get(url=URL, headers=headers)

    json_data = responseDict.json()
    print("JSON DATA: ", json_data)
    print("Count", count)
    count=count +1

    if 'Resources' in json_data:
        if len(json_data.get('Resources')) > 1:
            triples += ('<{}> focu:hasTopics <{}> ;\n'.format(courseCode,json_data.get('Resources')[0]['@URI']))
            for urls in islice(json_data.get('Resources'), 1, len(json_data.get('Resources'))-1):
                try:
                    triples +='\t focu:hasTopics <{}> ;\n'.format(urls.get('@URI'))
                except:
                    pass
            triples += '\t focu:hasTopics <{}> .\n'.format(json_data.get('Resources')[len(json_data.get('Resources'))-1].get('@URI'))
        else:
            triples += ('<{}> focu:hasTopics <{}> .\n'.format(courseCode, json_data.get('Resources')[0]['@URI']))
print(triples)
conn.close()

with open('triples.rdf','w', encoding='utf-8') as file:
    file.write(triples)
