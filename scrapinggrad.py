from chrome_driver import create_driver, quit_driver
from bs4 import BeautifulSoup
import re
import regex
import json
import requests

def scrap_grad_encs():

    page = "https://www.concordia.ca/academics/graduate/calendar/current.html"

    driver = create_driver()
    driver.get(page)

    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')
    faculty_div = soup.findAll("div", attrs={"class": "wysiwyg parbase section"})[2]
    faculty_link = faculty_div.findAll("a")
    scrap_courses("https://www.concordia.ca/academics/graduate/calendar/current/fasc.html")
    # for link in faculty_link:
    #     url = "https://www.concordia.ca" + link['href']
    #     scrap_courses(url)
    scrap_course_data("https://www.concordia.ca/academics/graduate/calendar/current/fasc/ahsc-ma.html")
    quit_driver(driver)
    
def scrap_courses(url):
    driver = create_driver()
    driver.get(url)
    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')
    faculty_div = soup.find("div", attrs={"class": "rte"})
    faculty_a = faculty_div.findAll("a")
    count = 0
    for links in faculty_a:
        try:
            href = links['href']
            if (re.match('/academics/graduate/calendar/current/',href)):
                count+=1
                # print(href)
        except:
             pass
    quit_driver(driver)

def scrap_course_data(href):
    driver = create_driver()
    driver.get(href)
    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')   
    course_div = soup.findAll("div", attrs={"class": "wysiwyg parbase section"})[2]
    coursediv_div = course_div.find("div", attrs={"class": "rte"})
    course_p = coursediv_div.text
    # print(course_p)
    array_p = re.split(r"\n\n", course_p)
    # for element in array_p:
    #     print("===================")
    #     print(element)
    for courses in array_p:
        array_p1 = re.split(r"\n\xa0\n", courses)
        for element in array_p1:
            array_p2 = re.split(r"\n", element)
            print(array_p2)
            for elements in array_p2:
                print("===================")
                print(elements)
                # # print(checkIfStartsWithCourseNumb(elements))

# def checkIfStartsWithCourseNumb(paragraph):
#     pattern1 = re.findall("[A-Z]{4}\s[0-9]{3}", paragraph)
#     pattern2 = re.findall("[A-Z]{3}\s[0-9]{3}", paragraph)
#     if((len(pattern1)>0 and paragraph.startswith(pattern1[0])) or (len(pattern2)>0 and paragraph.startswith(pattern2[0]))):
#         return True
#     else:
#         return False
    
    
scrap_grad_encs()