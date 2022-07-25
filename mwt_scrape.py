# scrapes malware tips' security forums
# retrieves data from the "General Security Discussions", and "Threat Analyis" sections
# for each post recent enough, it gets the date, post title, post body, and first page responses

# WORKING July 24, 2022

# dependences : beautifulsoup4, selenium, chromedriver, google chrome beta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import time
import csv

# url for malware tips
url = "https://malwaretips.com/"

maxdays = 31  # the max number of days ago the post can be made

# opens chrome beta for given link

# path to chromedriver file
chromedriver_path = "/Users/kaushalmarimuthu/Documents/KaushalCSDocs/digitalmain/chromedriver"
option = Options()
# path to google chrome beta
option.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'
driver = webdriver.Chrome(service=Service(ChromeDriverManager(
    version='104.0.5112.20').install()), options=option)
driver.get(url)
time.sleep(4)

driver.find_elements(By.CLASS_NAME, "uix_categoryTitle")[
    4].click()  # open "Security Topics" section
time.sleep(2)

# title row for csv file
with open('questions_mwt.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Question', 'Question Body', "Reply"])

# scrape first 2 topics, "General Security Discussions" and "Threat Analysis"
for i in range(1, 3):
    driver.find_elements(By.CSS_SELECTOR, ".node-title a")[i].click()
    skip = len(driver.find_elements(By.CSS_SELECTOR,
               ".structItem-status.structItem-status--sticky"))  # how many pinned posts (to skip)
    fd = 1  # how many posts found

    while fd > 0:
        fd = 0
        for j in range(20):  # 20 non pinned posts per page
            # gets jth post
            elem = driver.find_elements(
                By.CSS_SELECTOR, ".structItem-title")[j+skip].find_elements(By.TAG_NAME, "a")
            elem = elem[len(elem) - 1]
            driver.execute_script(
                "arguments[0].scrollIntoView({'block':'center'});", elem)
            time.sleep(2)

            # gets date jth post is posted
            tm = driver.find_elements(
                By.CLASS_NAME, "u-dt")[(skip+j)*2].get_attribute("data-date-string")
            # how many days ago it was posted
            diff = (datetime.today() - datetime.strptime(tm, "%b %d, %Y")).days
            if diff <= maxdays:  # make sure post isn't too far back
                fd += 1
                elem.click()  # open post
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string.replace(" | MalwareTips Forums", "")
                # find each text "box" on the post
                bod = soup.find_all(class_="bbWrapper")
                if len(bod) > 0:
                    body = bod[0].text  # first text "box" is the question body
                    rps = []
                    if len(bod)-1 > 1:
                        # rest of the text "boxes" are response (last is junk)
                        for k in range(1, len(bod)-1):
                            # if its a reply response, remove parent
                            if bod[k].text.find("Click to expand...") != -1:
                                rps.append(
                                    bod[k].text[(bod[k].text.find("Click to expand...") + 18):])
                            else:
                                rps.append(bod[k].text)
                    # write to csv file
                    with open('questions_mwt.csv', 'a') as f:
                        writer = csv.writer(f)
                        for rp in rps:
                            writer.writerow([tm, title, body, rp])
                    driver.back()
                    time.sleep(2)
        if fd > 0:  # if theres atleast 1 post found on this page, open next page
            driver.find_elements(
                By.CSS_SELECTOR, ".pageNav-jump.pageNav-jump--next")[1].click()
            skip = 0
            time.sleep(1)
        else:  # if no posts on this page, go back to previous page
            e = driver.find_element(
                By.CLASS_NAME, "p-breadcrumbs").find_elements(By.TAG_NAME, "li")[1]
            driver.execute_script(
                "arguments[0].scrollIntoView({'block':'center'});", e)
            e.click()
    time.sleep(1)

driver.quit()
