from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
import re



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
    if(len(all_familiar_with)>0):
        for familiar_with in all_familiar_with:
            formated_familiar_with = "<{}>".format(familiar_with)
            query3 = """PREFIX rdfs:<https://www.w3.org/2000/01/rdf-schema#>
                    SELECT ?object
                    WHERE {{
                        {} rdfs:label ?object.
                    }}""".format(formated_familiar_with)
            qfamiliarres = g.query(query3)
            for res in qfamiliarres:
                print(res[0], "is familiar with the topic")
    else:
        print("No student is familiar with this topic")

def get_course_description(course):
    subject = "<http://example.org/"+course+">"

    query = """SELECT ?description
                WHERE {{
                    {} focu:courseDescription ?description.
                }}""".format(subject)

    qres = g.query(query)
    if(len(qres) > 0):
        for row in qres:
            print("Here is the description of {}:".format(course))
            print(row[0])
    else:
        print("{} is not a course".format(course))

def get_courses_student_took(student):
    subject = "<http://example.org/"+student+"#me>"

    query = """SELECT ?description
                WHERE {{
                    {} focu:Grades ?description.
                }}""".format(subject)

    qres = g.query(query)

    if(len(qres) > 0):
        for row in qres:
            grade = re.split('\s+', row[0])[0]
            course = re.split('\s+', row[0])[1]
            print("{} took {} and got {} as a grade".format(student, course, grade))
            get_course_description(course)
    else:
        print("{} is not a student in our University".format(subject))

def get_courses_that_cover_topic(topic):
    topic_formated = topic.replace(" ","_")
    link = "<http://dbpedia.org/resource/"+topic_formated+">"

    query = """SELECT ?course
                WHERE {{
                    ?course focu:hasTopics {}.
                }}""".format(link)

    qres = g.query(query)

    if(len(qres) >0):
        for row in qres:
            print(row[0].replace("http://example.org/",""))
    else:
        print("No course covers this topic")

def endsWithQuestionMark(question):
    if(question[len(question)-1] != '?'):
        question=question+'?'
    return question

if __name__ == "__main__":
    g = Graph()

    inputText = input("Hello, I am your smart university agent. What are you looking for?\n")

    g.load("triples.rdf", format='turtle')

    patternCourseDescription = re.compile(r"What is [a-zA-Z0-9 ]* about\?$", re.IGNORECASE)
    patternStudentCourses = re.compile(r"Which courses did [a-zA-Z]* take\?$", re.IGNORECASE)
    patternCourseTopics = re.compile(r"Which courses cover [a-zA-Z0-9 ]*\?$", re.IGNORECASE)
    patternFamiliarWith = re.compile(r"Who is familiar with [a-zA-Z0-9 ]*\?$", re.IGNORECASE)

    actif = True
    while(actif):
        if(inputText == "stop"):
            print("Good bye !\n")
            actif = False

        else:
            inputText=endsWithQuestionMark(inputText)

# ========================================Assignement 1 =========================
            if(inputText == "How many triples are there?"): #1
                get_total_number_of_triples()
                inputText = input("Anything else ?\n")

            elif(inputText == "How many students are there?"): #2
                get_number_of_students()
                inputText = input("Anything else ?\n")

            elif(inputText == "How many courses are there?"): #2
                get_number_of_courses()
                inputText = input("Anything else ?\n")

            elif(inputText == "How many topics are there?"): #2
                get_number_of_topics()
                inputText = input("Anything else ?\n")

            elif(inputText == "Find course topics?"): #3
                inputText = input("What course do you want the topics for ?\n")
                print("These are all topics covered:")
                topics = get_topics_of_course(inputText)
                print_course_topics(topics)
                inputText = input("Anything else ?\n")

            elif(inputText == "Find courses passed?"): #4
                inputText = input("For which student do you want to know the classes that he/she passed ?\n")
                get_courses_passed_by_student(inputText)
                inputText = input("Anything else ?\n")

            elif(inputText == "Find topics familiar with?"):#5
                inputText = input("For what topic do you want to know the students who are familiar with it?\n")
                get_student_familiar_with_topic(inputText)
                inputText = input("Anything else ?\n")

            elif(inputText == "Find student familiar with topics?"):#6
                inputText = input("For what students do you want to know the topics they are familiar with?\n")
                get_topics_student_famliar_with(inputText)
                inputText = input("Anything else ?\n")

#====================================Assignment2===============================
            elif(re.match(patternCourseDescription,inputText)): #A2 - 1 “What is <course> about?”
                #divide by space and concatinate third and 4th word
                course=''
                if(len(re.split('\s+', inputText)) == 5):
                    course = re.split('\s+', inputText)[2]+re.split('\s+', inputText)[3]
                    course = course.upper()
                elif(len(re.split('\s+', inputText)) == 4):
                    course = re.split('\s+', inputText)[2]
                    course = course.upper()
                get_course_description(course)
                inputText = input("Anything else ?\n")

            elif(re.match(patternStudentCourses,inputText)): #A2 - 2 “Which courses did <Student> take?”
                student = re.split('\s+', inputText)[3].lower().capitalize()
                get_courses_student_took(student)
                inputText = input("Anything else ?\n")

            elif(re.match(patternCourseTopics,inputText)): #A2 - 3 “Which courses cover <Topic>?”
                topic = inputText[20:len(inputText)-1].lower()
                topic = topic[0].upper()+topic[1:]
                get_courses_that_cover_topic(topic)
                inputText = input("Anything else ?\n")

            elif(re.match(patternFamiliarWith,inputText)): #A2 - 4 “Who is familiar with <Topic>?”
                topic = inputText[21:len(inputText)-1].lower()
                topic = topic[0].upper()+topic[1:]
                get_student_familiar_with_topic(topic)
                inputText = input("Anything else ?\n")

            elif(inputText == "stop"):
                print("Good bye !\n")
                actif = False
                done = True
            else:
                inputText = input("I don't understand what you are saying. Say 'stop' if you don't want to continue.?\n")
