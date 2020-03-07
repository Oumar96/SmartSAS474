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

    for link in faculty_link:
        url = "https://www.concordia.ca" + link['href']
        scrap_courses(url)
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
                print(href)
        except:
             pass
    quit_driver(driver)
        

scrap_grad_encs()