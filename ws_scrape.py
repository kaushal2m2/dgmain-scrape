# scrapes wilder's security's forums
# retrieves data from the "Security Products", "Privacy Related Topics", and "Other Security Topics" sections
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

# url for wilders security
url = "https://www.wilderssecurity.com/"

maxdays = 31  # the max number of days ago the post can be made (min 7)

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

# title row for csv file
with open('questions_ws.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Question', 'Question Body', "Reply"])

# we want to scrape 2nd, 3rd, and 4th subsections since they relate to security
for i in range(1, 4):
    # find the button to access each subsection and click
    e = driver.find_elements(By.CSS_SELECTOR, ".categoryText")[
        i].find_element(By.TAG_NAME, "a")
    driver.execute_script(
        "arguments[0].scrollIntoView({'block':'center'});", e)
    time.sleep(1)
    e.click()
    # how many topics per section
    lt = len(driver.find_elements(By.CLASS_NAME, "nodeTitle"))
    for j in range(lt):
        el = driver.find_elements(By.CLASS_NAME, "nodeTitle")[
            j].find_element(By.TAG_NAME, "a")  # find jth topic
        driver.execute_script(
            "arguments[0].scrollIntoView({'block':'center'});", el)
        time.sleep(1)
        el.click()  # open jth topic
        ct = 1  # how many valid posts per page
        time.sleep(1)
        # sort by start date
        driver.find_element(By.CLASS_NAME, "postDate").click()
        time.sleep(1)
        while ct > 0:
            ct = 0
            # how many posts on the page
            ltt = len(driver.find_elements(By.CLASS_NAME, "titleText"))
            for k in range(ltt):  # process every post
                elem = driver.find_elements(By.CLASS_NAME, "titleText")[
                    k]  # kth post
                driver.execute_script(
                    "arguments[0].scrollIntoView({'block':'center'});", elem)
                dt = elem.find_element(
                    By.CLASS_NAME, "DateTime").text  # gets the date
                diff = 0
                # finds difference in date. posts might be labeled with "Monday at xx:xx", if they are within 7 days
                # these posts will also be processed
                try:
                    diff = (datetime.today() -
                            datetime.strptime(dt, "%b %d, %Y")).days
                except ValueError:
                    diff = 0
                if diff <= maxdays:  # check if date is within maxdays ago
                    ct += 1
                    time.sleep(1)
                    elem.find_element(By.TAG_NAME, "a").click()  # opens post
                    time.sleep(1)
                    html = driver.page_source
                    # html of the page
                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.title.string.replace(
                        " | Wilders Security Forums", "")
                    # gets all the message "boxes" on the page
                    data = soup.find_all("blockquote", class_="messageText")
                    q = ""
                    rps = []
                    if len(data) > 0:
                        # first message "box" is the question body
                        q = data[0].text
                        if len(data) > 1:
                            # all other extracted message "boxes" are responses
                            for l in range(1, len(data)):
                                rps.append(data[l].text)
                    # write to csv file
                    with open('questions_ws.csv', 'a') as f:
                        writer = csv.writer(f)
                        for rp in rps:
                            writer.writerow([dt, title, q, rp])
                    driver.back()
                    time.sleep(2)
            if ct != 0:  # if there was a valid post in the section, go to next page
                nx = driver.find_elements(
                    By.CSS_SELECTOR, ".PageNav .text")
                if len(nx) != 0:  # if theres a next button
                    nx[len(nx)-1].click()
                else:  # if no next button
                    ct = 0
            if ct == 0:  # if no valid post on current page, or no next button go back to topics page
                driver.find_elements(
                    By.CSS_SELECTOR, ".crust a.crumb span")[3].click()
            time.sleep(2)
    driver.find_elements(By.CSS_SELECTOR, ".crust a.crumb span")[
        0].click()  # go back to subsections page
    time.sleep(1)
driver.quit()
