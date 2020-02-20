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
                # print(faculty_link)
                number_of_faculties_in_tag = len(faculty_link)
                count = 0

                # array = re.split('\s+', faculty.text)
                # # array = faculty.text.replace("&nbsp", "").strip()
                # for element in array:
                #     print(element)
                #     print("...........................")
                # # print(len(array))
                array_faculty_names = re.split('\s+', faculty.text)
                while count<number_of_faculties_in_tag:
                    faculty_name = array_faculty_names[count]
                    link = faculty_link[count]['href']
                    # print(faculty_name,": ",link)
                    # print("==========")
                    count= count+1
                    info[faculty_name] = {"link":link}
                    list_of_faculties.append(faculty_name)

            else:
                faculty_name = faculty.text
                link = faculty_link[0]['href']
                info[faculty_name] = {"link":link}
                list_of_faculties.append(faculty_name)
                # print(faculty_name,": ",link)
                # print("==========")
        else:
            faculty_name = faculty.text
            link = faculty.find_parent("a")['href']
            info[faculty_name] = {"link":link}
            list_of_faculties.append(faculty_name)
            # print(faculty_name,": ",link)
            # print("==========")


    with open('./undergraduate.json', 'w') as outfile:
        json.dump(info, outfile)


    return list_of_faculties, info


if __name__ == "__main__":
    list_of_faculties, info = scrap_undergrad()
    print("List of all the undergraduate faculties: \n")
    print(list_of_faculties)
    print("\n\n")
    print("Links to all the undergraduate faculties course lists page: \n")
    print(info)