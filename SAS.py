from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF



def get_total_number_of_triples():
    qres = g.query(
        """SELECT (COUNT(*) as ?Triples)
            WHERE {
                ?subject ?predicate ?object
                }
        """)
    for row in qres:
        print("The number of triples in this Knowledge base is: ", row[0])

def get_number_of_students():
    qres = g.query(
        """SELECT (COUNT(*) as ?Triples)
            WHERE {
                ?subject a focu:Student
                }
        """)
    for row in qres:
        print("The number of students is: ", row[0])

def get_number_of_courses():
    qres = g.query(
        """SELECT (COUNT(*) as ?Triples)
            WHERE {
                ?subject a focu:Course
                }
        """)
    for row in qres:
        print("The number of courses is: ", row[0])

def get_number_of_topics():
    qres = g.query(
        """SELECT (COUNT(*) as ?Triples)
            WHERE {
                ?subject focu:hasTopics ?object
                }
        """)
    for row in qres:
        print("The number of topics is: ", row[0])

def get_topics_of_course(course):
    subject = "<http://example.org/"+course+">"
    query = """SELECT ?link
                WHERE {{
                    {} focu:hasTopics ?link.
                }}""".format(subject)

    qres = g.query(query)
    
    print("These are all topics covered:")
    # Getting all topics
    for row in qres:
        link_of_topic = row[0]
        link = URIRef(row[0])
        dbpediaGraph = Graph()
        dbpediaGraph.load(link)

        subject_in_link = "<{}>".format(link)
        query2 = """SELECT ?label
            WHERE {{
                {} rdfs:label ?label.
                FILTER (LANG(?label) = 'en') . 
                }}
        """.format(subject_in_link)

        # Getting the label for every topic
        qres2 = dbpediaGraph.query(query2)
        for row in qres2:
            topic_name = row[0]
            print(topic_name, ": ",link_of_topic)

# def get_topics_student_famliar_with(student):
#     subject = "<http://example.org/"+student+">"
#     focu:Grades "A+ AHSC220" ;
#     query = """SELECT ?course
#                 WHERE {{
#                     {} focu:hasTopics ?link.
#                 }}""".format(subject)

#     qres = g.query(query)


if __name__ == "__main__":
    g = Graph()

    inputText = input("Hello, I am your smart university agent. What are you looking for?\n")

    g.load("triples.rdf", format='turtle')

    actif = True
    while(actif):
        if(inputText == "stop"):
            print("Good bye !\n")
            actif = False

        else:
            if(inputText == "triples"):
                get_total_number_of_triples()
                inputText = input("Anything else ?\n")

            elif(inputText == "students"):
                get_number_of_students()
                inputText = input("Anything else ?\n")

            elif(inputText == "courses"):
                get_number_of_courses()
                inputText = input("Anything else ?\n")

            elif(inputText == "topics"):
                get_number_of_topics()
                inputText = input("Anything else ?\n")

            elif(inputText == "course topics"):
                inputText = input("What course do you want the topics for ?\n")
                get_topics_of_course(inputText)
                inputText = input("Anything else ?\n")

            # elif(inputText == "student topics"):
            #     inputText = input("For what students do you want to know the topics they are familiar with?\n")
            #     get_topics_of_course(inputText)

            elif(inputText == "stop"):
                print("Good bye !\n")
                actif = False
                done = True
            else:
                inputText = input("I don't understand what you are saying. Say 'stop' if you don't want to continue.?\n")
