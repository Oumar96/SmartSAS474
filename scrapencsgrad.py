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
    
    info = {}

    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')   
    course_div = soup.findAll("div", attrs={"class": "wysiwyg parbase section"})[2]
    coursediv_div = course_div.find("div", attrs={"class": "rte"})
    course_para = coursediv_div.findAll("p")
    # print(course_para)
    for elements in course_para:
        course_span = elements.findAll("span", attrs={"class": "large-text"})
        # print(course_span)
        for titles in course_span:
            course_title = titles.findAll("b")
            # print(course_title)
            if len(course_title) > 0:
                # print(course_title)
                for title in course_title:
                    # print("==========")
                    if (checkIfStartsWithCourseNumb(title.text) == True):
                        array_p2 = re.split(r" ", title.text)
                        course_code = array_p2[0] + " " + array_p2[1][:4]
                        print(course_code)
                        titleCourseTxt = array_p2[2:]
                        titledesc=''
                        for word in titleCourseTxt:
                            titledesc+= word +' '
                        print(titledesc)        

    quit_driver(driver)
        
        
                                    # for splittext in array_p1:
                                    #     # print(splittext)
                                    #     course_code = splittext[0]
                                    #     print(course_code) 
                    # txt_title = title.replace('<b>',' ')
                    # print(txt_title)
        
        # print("======")
        # print(elements) 
        # array_p = re.split(r"<p>", elements)
        # print(array_p)
        # bold = elements.find("b")
        # for element in bold:
        #     if (checkIfStartsWithCourseNumb(element) == True):
                # para = elements.find("p")
    #     print(elements)
    # quit_driver(driver)
#     course_p = coursediv_div.text
#     # print(course_p)
    
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
    pattern2 = re.findall("[A-Z]{4}\s[0-9]{4}", paragraph)
    if((len(pattern1)>0 and paragraph.startswith(pattern1[0])) or (len(pattern2)>0 and paragraph.startswith(pattern2[0]))):
        return True
    else:
        return False

scrap_course_data()