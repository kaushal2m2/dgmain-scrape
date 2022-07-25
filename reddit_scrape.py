# scrapes the cybersecurity subreddit, retrieving posts that don't link outside reddit
# gets the date, post title, post body, and top 5 responses
# uses old reddit since it is more scrape friendly and reddit says it has no plans to remove old reddit

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

# the url of the subreddit that is being scraped:
url = "https://old.reddit.com/r/cybersecurity/new/"
# this url is for r/cybersecurity's new posts. to sort by
# something else simply paste a different link here
# ex: to scrape top posts for previous month:
# url = "https://old.reddit.com/r/cybersecurity/top/?sort=top&t=month"


maxdays = 31  # the max number of days ago the post can be made

# opens chrome beta for given link

# path to chromedriver file
chromedriver_path = "/Users/kaushalmarimuthu/Documents/KaushalCSDocs/digitalmain/chromedriver"
option = Options()
# path to google chrome beta
option.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'
driver = webdriver.Chrome(service=Service(ChromeDriverManager(
    version='104.0.5112.20').install()), options=option)  # chrome beta version number
driver.get(url)
time.sleep(2)

# title row for csv file
with open('questions_reddit.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Question', 'Question Body', "Reply"])

valid = True  # whether the posts we are looking at are within maxdays away
while valid:
    # num of posts on the page
    cts = len(driver.find_elements(By.CSS_SELECTOR, "a.title.may-blank "))
    for i in range(cts):
        elem = driver.find_elements(
            By.CSS_SELECTOR, "a.title.may-blank ")[i]  # find ith post
        driver.execute_script(
            "arguments[0].scrollIntoView({'block':'center'});", elem)
        time.sleep(1)
        hr = elem.get_attribute("href")
        # check if post is a reddit typed post (non-ad)
        if hr.startswith("https://old.reddit.com/r/cybersecurity/"):
            elem.click()  # navigate to post
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            title = soup.title.string.replace(" : cybersecurity", "")

            dt = soup.find("time").text  # find the date the post was published
            diff = (datetime.today() -
                    datetime.strptime(dt, "%d %b %Y")).days  # how many days ago the post was made

            # since when organized by "new", posts are ordered new to old, once a post
            # older than wanted is found, we exit the program
            if diff > maxdays:
                valid = False
                break

            # get the text in every discussion "box" on the page
            txts = soup.select(
                "div.usertext-body.may-blank-within.md-container div.md")
            q = ""
            if len(txts) > 1:
                # second element with the selector is the question (first is junk)
                q = txts[1].text

            rps = []
            # go through the rest of the "boxes", get the first 5 responses if they exist
            for j in range(2, len(txts)):
                if j > 6:
                    break
                rps.append(txts[j].text)

            # write to csv file
            with open('questions_reddit.csv', 'a') as f:
                writer = csv.writer(f)
                for rp in rps:
                    writer.writerow([dt, title, q, rp])
            driver.back()
    if not valid:  # if an old post was encountered
        break

    # find next button and click it
    nx = driver.find_element(By.CSS_SELECTOR, "span.next-button a")
    driver.execute_script(
        "arguments[0].scrollIntoView({'block':'center'});", nx)
    time.sleep(1)
    nx.click()
    time.sleep(1)

driver.quit()
