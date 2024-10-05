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
from selenium.webdriver.support import expected_conditions as E

df = pd.read_csv('all_search_hashtags_data.csv')

print(len(df['author_names'].tolist()))
for a in df['author_names'].tolist():
    print(a[0])

# def extract_authors(driver, author_names):
#     data_authors = []

#     for author in author_names:
#         url = f"https://www.tiktok.com/@{author}"
#         driver.get(url)
#         time.sleep(2)

#         user_name = [user.text for user in driver.find_elements(By.CLASS_NAME, "css-11ay367-H1ShareTitle.e1457k4r8")]
#         print(user_name)
#         f_count = [fc.text for fc in driver.find_elements(By.CLASS_NAME, "css-1ldzp5s-DivNumber.e1457k4r1")]
#         following, follower = f_count[0].split("\n")[0], f_count[1].split("\n")[0]
#         likes = [like.text for like in 
#                 driver.find_elements(By.CLASS_NAME, "css-pmcwcg-DivNumber.e1457k4r1")][0].split("\n")[0]
#         data_authors.append({
#             'user_name': user_name,
#             'following': following,
#             'follower': follower,
#             'n_likes': likes
#         })

#         author_df = pd.DataFrame(data=data_authors, columns=data_authors[0].keys())
#         author_df.to_csv('author_data.csv', index=False)