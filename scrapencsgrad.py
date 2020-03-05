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
    array_gradencs_info = []
    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')
    course_div = soup.findAll("div", attrs={"class": "wysiwyg parbase section"})[2]
    coursediv_div = course_div.find("div", attrs={"class": "rte"})
    course_para = coursediv_div.findAll("p")
    # print(course_para)
    for elements in course_para:
        course_span = elements.findAll("span", attrs={"class": "large-text"})
            
            

        for titles in course_span:
            courseDesceription = titles.text
            course_title = titles.findAll("b")
            if len(course_title) > 0:
                for title in course_title:
                    if (checkIfStartsWithCourseNumb(title.text) == True):
                        array_p2 = re.split(r" ", title.text)
                        course_code = array_p2[0] + " " + array_p2[1][:4]
                        titleCourseTxt = array_p2[2:]
                        titledesc=''
                        for word in titleCourseTxt:
                            titledesc+= word +' '

                        info = {
                                "course": course_code,
                                "credits": "",
                                "title": titledesc,
                                "description": courseDesceription
                            }
                        array_gradencs_info.append(info)
    quit_driver(driver)
    return array_gradencs_info

def save_in_json(array):
    with open('./ENCSgrad-info.json', 'w') as outfile:
        json.dump(array, outfile)

def checkIfStartsWithCourseNumb(paragraph):
    pattern1 = re.findall("[A-Z]{4}\s[0-9]{3}", paragraph)
    pattern2 = re.findall("[A-Z]{4}\s[0-9]{4}", paragraph)
    if((len(pattern1)>0 and paragraph.startswith(pattern1[0])) or (len(pattern2)>0 and paragraph.startswith(pattern2[0]))):
        return True
    else:
        return False

if __name__ == "__main__":
    array_gradencs_info = scrap_course_data()
    # # print("faculties: \n")
    # array_undergrad_info = []
    # for faculty in info:
    #     # print(faculty)
    #     href =info[faculty].get('href')
    #     link = "https://www.concordia.ca{}".format(href,sep='')
    #     # print(link)
    #     array_undergrad_info = scrap_faculty_courses(link,array_undergrad_info)
    # # array_undergrad_info = scrap_faculty_courses("https://www.concordia.ca/academics/undergraduate/calendar/current/sec81/81-100.html#jazz",array_undergrad_info)
    save_in_json(array_gradencs_info)
    # save_in_db(array_undergrad_info)