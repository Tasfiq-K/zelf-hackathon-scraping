import os
import re
import time
import pickle
import random
import argparse
import pandas as pd
from tqdm import tqdm

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def get_searched_links(search_inputs, hash_tags):
    webdriver_path = "/usr/local/bin/geckodriver"
    options = Options()
    options.set_preference('profile', webdriver_path)
    driver = Firefox(options=options)
    
    data = []
    # get data using searches 
    for kw in search_inputs:
        url = f"https://www.tiktok.com/search?lang=en&q={kw}&t=1728099684294"
        driver.get(url)
        time.sleep(10)
        scroll_down(driver)

        links = [link.get_attribute('href') for link in 
                 driver.find_elements(By.CLASS_NAME, 'css-1g95xhm-AVideoContainer.e19c29qe13')]
        
        author_names_1 = [auth.text for auth in driver.find_elements(By.CLASS_NAME, 'css-2zn17v-PUniqueId.etrd4pu6')]

        captions = [cap.text for cap in driver.find_elements(By.CLASS_NAME, 'css-6opxuj-H1Container.ejg0rhn1')]
        # print(captions)
        data.append({
            'vid_url':links,
            'author_names':author_names_1,
            'captions': captions
        })
    
    # get data using hash tags 
    for htag in hash_tags:
        url = f"https://www.tiktok.com/tag/{htag}"
        print(url)
        
        driver.get(url)
        time.sleep(30)
        scroll_down(driver)

        links = [link.get_attribute('href') for link in 
                 driver.find_elements(By.CLASS_NAME, 'css-1g95xhm-AVideoContainer.e19c29qe13')]
        captions = [cap.text for cap in 
                    driver.find_elements(By.CLASS_NAME, "css-1wrhn5c-AMetaCaptionLine.eih2qak0")]
        author_names_2 = [auth.text for auth in 
                        driver.find_elements(By.CLASS_NAME, "user-name.css-1gi42ki-PUserName.exdlci15")]
        # print(captions)
        # print(author_names)
        data.append({
            'vid_url':links,
            'author_names':author_names_2,
            'captions': captions
        })

        df = pd.DataFrame(data=data, columns=data[0].keys())
        # df.to_csv('tiktok_post_hashtags.csv', index=False)
        df.to_csv('all_search_hashtags_data.csv', index=False)
    
    extract_authors(driver, author_names_1 + author_names_2)
    driver.quit()


def extract_authors(driver, author_names):
    data_authors = []

    for author in author_names:
        url = f"https://www.tiktok.com/@{author}"
        driver.get(url)
        time.sleep(2)

        user_name = [user.text for user in driver.find_elements(By.CLASS_NAME, "css-11ay367-H1ShareTitle.e1457k4r8")]
        print(user_name)
        f_count = [fc.text for fc in driver.find_elements(By.CLASS_NAME, "css-1ldzp5s-DivNumber.e1457k4r1")]
        following, follower = f_count[0].split("\n")[0], f_count[1].split("\n")[0]
        likes = [like.text for like in 
                driver.find_elements(By.CLASS_NAME, "css-pmcwcg-DivNumber.e1457k4r1")][0].split("\n")[0]
        data_authors.append({
            'user_name': user_name,
            'following': following,
            'follower': follower,
            'n_likes': likes
        })

        author_df = pd.DataFrame(data=data_authors, columns=data_authors[0].keys())
        author_df.to_csv('author_data.csv', index=False)

    # print(len(f_count))
    # print(f_count)
    # print("fll", following)
    # print("fllw", follower)
    # print(likes[0].split("\n")[0])

    
def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(5)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height