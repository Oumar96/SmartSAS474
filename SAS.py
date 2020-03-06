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
    topics = []
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
            info = {
                "topic_name":topic_name,
                "link_of_topic":link_of_topic
            }
            topics.append(info)
    return topics


def print_course_topics(topics):
    for topic in topics:
        print(topic.get("topic_name"), ": ",topic.get("link_of_topic"))

def get_topics_student_famliar_with(student):
    classes_passed_by_student = get_courses_passed_by_student(student)

    print(student, "is familiar with the following topics(be patient might take a while):")
    all_topics = []
    for class_passed in classes_passed_by_student:
        topics_for_class = get_topics_of_course(class_passed)
        for topic in topics_for_class:
            all_topics.append(topic.get("topic_name"))
            # print(topic.get("topic_name"))
        print("A step closer...")

    all_topics = list(dict.fromkeys(all_topics))
    for topic in all_topics:
        print(topic)


def get_courses_passed_by_student(student):
    subject = "<http://example.org/"+student+"#me>"

    query = """SELECT ?course
                WHERE {{
                    {} focu:Grades ?course.
                }}""".format(subject)

    qres = g.query(query)
    classes_passed = []
    for row in qres:
        index_of_space = row[0].index(" ")
        grade = row[0][:index_of_space]
        course = row[0][index_of_space+1:]
        if(grade != "F"):
            classes_passed.append(course)
            print("{} passed {}".format(student,course))
    return classes_passed

def get_student_familiar_with_topic(topic):
    topic = "Biopsychosocial model"
    topic_formated = topic.replace(" ","_")
    link = "<http://dbpedia.org/resource/"+topic_formated+">"

    query = """SELECT ?course
                WHERE {{
                    ?course focu:hasTopics {}.
                }}""".format(link)

    qres = g.query(query)

    query2 = """SELECT ?student ?course
            WHERE {{
                ?student focu:Grades ?course.
            }}"""
    query_all_grades = g.query(query2)

    all_familiar_with = []
    for row in qres:
        for grade in query_all_grades:
            student = grade[0]
            grade_for_course = grade[1]
            index_of_space = grade_for_course.index(" ")
            grade = grade_for_course[:index_of_space]
            course = URIRef("http://example.org/"+grade_for_course[index_of_space+1:])
            if(course == row[0]):
                if(grade != "F"):
                    all_familiar_with.append(student)

    all_familiar_with = list(dict.fromkeys(all_familiar_with))
    # print(all_familiar_with)
    for familiar_with in all_familiar_with:
         print(familiar_with, "is familiar with the topic")
        # formated_familiar_with = "<{}>".format(familiar_with)
        # print(type(formated_familiar_with))
        # query3 = """SELECT ?label
        #         WHERE {{
        #             {} rdfs:label ?label.
        #         }}""".format(formated_familiar_with)
        # print(query3)
        # qfamiliarres = g.query(query3)
        # for res in qfamiliarres:
        #     print(res[0], "is familiar with the topic")


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
            if(inputText == "triples"): #1
                get_total_number_of_triples()
                inputText = input("Anything else ?\n")

            elif(inputText == "students"): #2
                get_number_of_students()
                inputText = input("Anything else ?\n")

            elif(inputText == "courses"): #2
                get_number_of_courses()
                inputText = input("Anything else ?\n")

            elif(inputText == "topics"): #2
                get_number_of_topics()
                inputText = input("Anything else ?\n")

            elif(inputText == "course topics"): #3
                inputText = input("What course do you want the topics for ?\n")
                print("These are all topics covered:")
                topics = get_topics_of_course(inputText)
                print_course_topics(topics)
                inputText = input("Anything else ?\n")

            elif(inputText == "familiar with"):#5
                inputText = input("For what topic do you want to know the students who are familiar with it?\n")
                get_student_familiar_with_topic(inputText)
                inputText = input("Anything else ?\n")

            elif(inputText == "student topics"):#6
                inputText = input("For what students do you want to know the topics they are familiar with?\n")
                get_topics_student_famliar_with(inputText)
                inputText = input("Anything else ?\n")

            elif(inputText == "stop"):
                print("Good bye !\n")
                actif = False
                done = True
            else:
                inputText = input("I don't understand what you are saying. Say 'stop' if you don't want to continue.?\n")
