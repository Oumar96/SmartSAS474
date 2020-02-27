from chrome_driver import create_driver, quit_driver
from bs4 import BeautifulSoup
import re
import regex
import json
import requests
from itertools import cycle

def scrap_course_data():
    href = "https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html"
    driver = create_driver()
    driver.get(href)
    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')   
    course_div = soup.findAll("div", attrs={"class": "wysiwyg parbase section"})[2]
    coursediv_div = course_div.find("div", attrs={"class": "rte"})
    course_para = coursediv_div.findAll("p")
    for elements in course_para: 
        bold = elements.find("b")
        for element in bold:
            if (checkIfStartsWithCourseNumb(element) == True):
                para = elements.find("p")
                print(para)
#     course_p = coursediv_div.text
#     # print(course_p)
    # array_p = re.split(r"\n\n", course_p)
    # array_p = re.split(r"\n\n", course_para)
#     for courses in array_p:
#         array_p1 = re.split(r"\n\xa0\n", courses)
#         for element in array_p1:
#             array_p2 = re.split(r"\n", element)
#     for elements in course_para:
#         if (checkIfStartsWithCourseNumb(elements) == True):
#             print(elements)

def checkIfStartsWithCourseNumb(paragraph):
    pattern1 = re.findall("[A-Z]{4}\s[0-9]{3}", paragraph)
    pattern2 = re.findall("[A-Z]{3}\s[0-9]{3}", paragraph)
    if((len(pattern1)>0 and paragraph.startswith(pattern1[0])) or (len(pattern2)>0 and paragraph.startswith(pattern2[0]))):
        return True
    else:
        return False

scrap_course_data()