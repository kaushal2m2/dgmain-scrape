# scrapes tech republic's security forums, getting the date, post title, post body, and top 5 responses for each
# post in each section

# WORKING July 24th, 2022


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

# url for tech republic 
url = "https://www.techrepublic.com/topic/security/"

maxdays = 31  # the max number of days ago the post can be made

# opens chrome beta for given link

# path to chromedriver file
chromedriver_path = "/Users/neelkanthshitolay/Documents/PyCharm/digitalmain/chromedriver"
option = Options()
# path to google chrome beta
option.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'
driver = webdriver.Chrome(service=Service(ChromeDriverManager(
    version='104.0.5112.20').install()), options=option)
driver.get(url)
time.sleep(3)

driver.find_element(
    By.XPATH, "//*[@id=\"onetrust-close-btn-container\"]/button").click()  # close cookies pop up

time.sleep(2)

# title row for csv file
with open('questions_techrepublic.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Question', 'Question Body', "Reply"])

for i in range(1, 12):
    # get the element linking to the subtopic and click it
    elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"lia-body\"]/div[3]/center/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/section/div/article[" + str(i) + "]/h3/a")))
    driver.execute_script(
        "arguments[0].scrollIntoView({'block':'center'});", elem)
    time.sleep(1)
    elem.click()
    time.sleep(4)

    recent = True
    pg = 1

    # while the posts are recent (until 1 full page is posts that are too old)
    while(recent):
        # get the html of the page to read the dates
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        dat = soup.find_all('time', datetime='MM-dd-yyyy hh:mm a')
        diff = [(datetime.today() - datetime.strptime(dt.string.strip()
                 [0:10], "%m-%d-%Y")).days for dt in dat]  # difference between each post date and today
        ct = 0
        for j in range(1, 16):  # 15 posts per page
            # find the jth post
            post = driver.find_element(
                By.XPATH, "/html/body/div[3]/center/div/div/div/div/div[1]/div[2]/div[1]/div/div[2]/section/article[" + str(j) + "]/div/h3/a")
            driver.execute_script(
                "arguments[0].scrollIntoView({'block':'center','inline':'center'});", post)
            time.sleep(2)
            if diff[j-1] <= maxdays:  # if its recent enough open the post
                ct += 1
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(post))
                post.click()
                time.sleep(2)

                # get the html of the code to parse for the info
                info = driver.page_source
                sp = BeautifulSoup(info, 'html.parser')

                date = dat[j-1].string.strip()[0:10]

                title = sp.title.string.strip().strip(" - Tech Republic Security")

                # gets each message "box" in the page
                bod = sp.find_all('div', 'lia-message-body-content')
                body = ""
                if len(bod) > 0:  # first message "box" is the question body
                    prt = bod[0].find_all('p')
                    for bo in prt:
                        body += bo.text
                        body += '\n'

                rps = []
                # rest of the message "boxes" are the responses
                if len(bod) > 1:
                    for k in range(1, len(bod)):
                        if(k > 3):  # capped at 5 (best) responses per post
                            break
                        rs = ""
                        prt = bod[k].find_all('p')
                        for bo in prt:
                            rs += bo.text
                            rs += '\n'
                        rps.append(rs)

                # write to csv file
                with open('questions_tr.csv', 'a') as f:
                    writer = csv.writer(f)
                    for rp in rps:
                        writer.writerow([date, title, body, rp])
                driver.back()
                time.sleep(2)
        if ct == 0:  # if no posts found on page
            recent = False
        # find next button
        nx = driver.find_elements(
            By.CSS_SELECTOR, ".lia-link-navigation.lia-js-data-pageNum-" + str(pg+1) + ".lia-custom-event")
        if len(nx) < 1:  # if no next button
            recent = False
        else:  # click next button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(nx[len(nx)-1]))
            driver.execute_script(
                "arguments[0].scrollIntoView({'block':'center'});", nx[len(nx)-1])
            time.sleep(2)
            nx[len(nx)-1].click()
        pg += 1  # next page
        time.sleep(3)
    driver.get(url)

driver.quit()
