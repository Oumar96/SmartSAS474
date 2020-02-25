from chrome_driver import create_driver, quit_driver
from bs4 import BeautifulSoup
import re
import regex
import json


def scrap_undergrad():
    url = "https://www.concordia.ca/academics/undergraduate/calendar/current/courses-quick-links.html"

    driver = create_driver()
    driver.get(url)

    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'lxml')
    all_faculties = soup.findAll("span", {"class": "large-text"})

    info = {}
    list_of_faculties = []

    for faculty in all_faculties:
        faculty_link = faculty.findAll("a")
        if(len(faculty_link) >0):
            if(len(faculty_link)>1):
                number_of_faculties_in_tag = len(faculty_link)
                count = 0
                array_faculty_names = re.split('\s+', faculty.text)
                while count<number_of_faculties_in_tag:
                    faculty_name = array_faculty_names[count]
                    link = faculty_link[count]['href']
                    count= count+1
                    info[faculty_name] = {"href":link}
                    list_of_faculties.append(faculty_name)

            else:
                faculty_name = faculty.text
                link = faculty_link[0]['href']
                info[faculty_name] = {"href":link}
                list_of_faculties.append(faculty_name)
        else:
            faculty_name = faculty.text
            link = faculty.find_parent("a")['href']
            info[faculty_name] = {"href":link}
            list_of_faculties.append(faculty_name)


    with open('./undergraduate.json', 'w') as outfile:
        json.dump(info, outfile)

    driver.close()
    driver.quit()
    return list_of_faculties, info

def scrap_faculty_courses(faculty_link,array_undergrad_info):
    driver = create_driver()
    driver.get(faculty_link)
    try:

        #Selenium hands the page source to Beautiful Soup
        soup=BeautifulSoup(driver.page_source, 'lxml')
        courses_section= soup.find('a',{"id": "courses"})
        courses_parent_tag = courses_section.parent.parent.text
        courses_array = re.split(r"\n\n", courses_parent_tag)
        if(len(courses_array)<=2):
            index_of_hashtag = faculty_link.index("#")+1
            faculty_id = faculty_link[index_of_hashtag:]
            courses_section= soup.find('a',{"id": faculty_id})
            courses_parent_tag = courses_section.parent.text
            courses_array = re.split(r"\n\n", courses_parent_tag)

        for courses in courses_array:
            courses_separated = re.split(r"\n\xa0\n", courses)
            for course in courses_separated:
                if checkIfStartsWithCourseNumb(course):
                    array_undergrad_info=get_course_number_and_descrption(array_undergrad_info,course)

    except AttributeError:
        try:
            soup=BeautifulSoup(driver.page_source, 'lxml')
            index_of_hashtag = faculty_link.index("#")+1
            faculty_id = faculty_link[index_of_hashtag:]
            # print(faculty_id)
            courses_section= soup.find('a',{"id": faculty_id})
            courses_parent_tag = courses_section.parent.parent.text
            # print(courses_section)
            courses_array = re.split(r"\n\n", courses_parent_tag)

            for courses in courses_array:
                courses_separated = re.split(r"\n\xa0\n", courses)
                for course in courses_separated:
                    if checkIfStartsWithCourseNumb(course):
                        array_undergrad_info=get_course_number_and_descrption(array_undergrad_info,course)
        except AttributeError:
            try:
                soup=BeautifulSoup(driver.page_source, 'lxml')
                index_of_hashtag = faculty_link.index("#")+1
                faculty_id = faculty_link[index_of_hashtag:]
                # print(faculty_id)
                courses_section= soup.find('a',{"id": faculty_id})
                courses_parent_tag = courses_section.parent.text
                # print(courses_section)
                courses_array = re.split(r"\n\n", courses_parent_tag)

                for courses in courses_array:
                    courses_separated = re.split(r"\n\xa0\n", courses)
                    for course in courses_separated:
                        if checkIfStartsWithCourseNumb(course):
                            array_undergrad_info=get_course_number_and_descrption(array_undergrad_info,course)
            except AttributeError:
                soup=BeautifulSoup(driver.page_source, 'lxml')
                index_of_hashtag = faculty_link.index("#")+1
                faculty_id = faculty_link[index_of_hashtag:]
                courses_section= soup.find('a',{"name": faculty_id})
                courses_parent_tags = courses_section.parent.findAll('p')
                course_parent_tag = ''
                for course in courses_parent_tags:
                    course_parent_tag = course_parent_tag+course.text
                courses_array = re.split(r"\n\n", course_parent_tag)

                for courses in courses_array:
                    courses_separated = re.split(r"\n\xa0\n", courses)
                    for course in courses_separated:
                        if checkIfStartsWithCourseNumb(course):
                            array_undergrad_info=get_course_number_and_descrption(array_undergrad_info,course)
    driver.close()
    driver.quit()

    return array_undergrad_info

def checkIfStartsWithCourseNumb(paragraph):
    pattern1 = re.findall("[A-Z]{4}\s[0-9]{3}", paragraph)
    pattern2 = re.findall("[A-Z]{3}\s[0-9]{3}", paragraph)
    if((len(pattern1)>0 and paragraph.startswith(pattern1[0])) or (len(pattern2)>0 and paragraph.startswith(pattern2[0]))):
        return True
    else:
        return False

def get_course_number_and_descrption(array_undergrad_info,paragraph):
    array = re.split('\s+', paragraph)
    count = 0
    course_code = ""
    for element in array:
        if count<2:
            course_code = course_code+" "+element
            count=count+1
    course_code = course_code[1:]
    try:
        title_and_description_array = re.split("\xa0", paragraph)
        title_and_description = title_and_description_array[len(title_and_description_array)-1].replace("\xa0","")[0:]
    except IndexError:
        title_and_description_index = paragraph.index("\xa0")
        title_and_description_temp = paragraph[title_and_description_index:]
        title_and_description = re.split(course_code, title_and_description_temp)[0].replace("\xa0","")[0:]

    title_and_description_array = re.split("\n", title_and_description)
    title = title_and_description_array[0]
    credit = "In description"
    try:
        description = title_and_description_array[1]
    except IndexError:
        description = "No description"
    try:
        credits_index = title.index("credit")-2
        credit = title[credits_index]
        title = title[:credits_index-2]
        # print("Course Code: ",course_code)
        # print("Credits: ", credit)
        # print("Title: ",title)
        # print("Description: ",description)
        info = {
            "course": course_code,
            "credits": credit,
            "title": title,
            "description": description
        }
        array_undergrad_info.append(info)
    except ValueError:
        # print("Course Code: ",course_code)
        # print("Credits: ", credit)
        # print("Title: ",title)
        # print("Description: ",description)
        info = {
            "course": course_code,
            "credits": credit,
            "title": title,
            "description": description
        }
        array_undergrad_info.append(info)
    return array_undergrad_info

def save_in_json(array):
    with open('./undergraduate-info.json', 'w') as outfile:
        json.dump(array, outfile)

if __name__ == "__main__":
    list_of_faculties, info = scrap_undergrad()
    # print("faculties: \n")
    array_undergrad_info = []
    for faculty in info:
        # print(faculty)
        href =info[faculty].get('href')
        link = "https://www.concordia.ca{}".format(href,sep='')
        # print(link)
        array_undergrad_info = scrap_faculty_courses(link,array_undergrad_info)
    # array = scrap_faculty_courses("https://www.concordia.ca/academics/undergraduate/calendar/current/sec81/81-100.html#jazz")
    save_in_json(array_undergrad_info)