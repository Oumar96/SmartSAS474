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

if __name__ == "__main__":
    g = Graph()

    inputText = input("Hello, I am your smart university agent. Who are you looking for?\n")

    g.load("focu.rdf", format='turtle')

    actif = True
    while(actif):
        if(inputText == "stop"):
            print("Good bye !\n")
            actif = False
        else:
            if(inputText == "Number of triples"):
                get_total_number_of_triples()
                inputText = input("Anything else ?\n")
            elif(inputText == "stop"):
                print("Good bye !\n")
                actif = False
                done = True
            else:
                inputText = input("I don't understand what you are saying. Say 'stop' if you don't want to continue.?\n")
