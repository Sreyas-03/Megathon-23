from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd


def scrape_linkedin(linkedin_link):
    PATH = "./geckodriver"
    # USERNAME = input("Enter your Linkedin Username")
    # PASSWORD = input("Enter your Password")
    USERNAME = "akshatsanghvi2021@gmail.com"
    PASSWORD = "sam6561"

    # driver = webdriver.Chrome(PATH)
    service = webdriver.FirefoxService(executable_path = PATH)
    driver = webdriver.Firefox(service=service)

    driver.get("https://www.linkedin.com/uas/login")
    # find username/email field and send the username itself to the input field
    driver.find_element("id", "username").send_keys(USERNAME)
    # find password input field and insert password as well
    driver.find_element("id", "password").send_keys(PASSWORD)
    # click login button
    # driver.find_element("submit").click()
    driver.find_element("tag name", "button").click()

    driver.get(linkedin_link)
    time.sleep(5)
    soup = bs(driver.page_source, "html5lib")
    with open("page.html", "w") as f:
        f.write(f"{soup.prettify()}") 
        
    about_element = soup.find(attrs={"class": "artdeco-entity-lockup__subtitle ember-view truncate"})
    experience_element = soup.find_all(attrs={"id": "experience"})
    driver.quit()
    return about_element.string.strip()
    # return f"{about_element.string.strip()}\n\n{experience_element}"

if __name__ == "__main__":
    linkedin = "https://www.linkedin.com/in/chaitanya100100/"
    print(scrape_linkedin(linkedin))
