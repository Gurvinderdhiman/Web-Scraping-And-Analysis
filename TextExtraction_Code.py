# Created By : Gurvinder Dhiman
# Created Date : 9 Feb - 14 Feb 2023

# Importing all required modules and packages

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# Importing the input file containing all the urls

df=pd.read_csv(r'C:\Users\user\PycharmProjects\pythonProject2\Task Submission by 14th Feb\Input.csv')[['URL_ID','URL']]
df=df.iloc[0:114]

df.drop('URL_ID',axis=1)
# getting all urls in li(list)
li = [url for url in df['URL']]
print(li)

# generating the text file
text_file = open(r'C:\Users\user\PycharmProjects\pythonProject2\Task Submission by 14th Feb\file name.txt', 'w',encoding='utf-8')
for url in li:
    page = requests.get(url)
    content = requests.get(url).content
    soup = bs(page.content,'html.parser')
    desc = soup.find('h1', class_='entry-title')
    soup = bs(page.content, 'html.parser')
    t = soup.find('div', class_='td-post-content')

    # handling null values in articles titles
    if desc is None:
        text_file.write("none\n")
    else:
        text_file.write(desc.text)

    # handling null values in articles texts
    if t is None:
        text_file.write("none\n")
    else:
        text_file.write(t.text)
# saving and closing the text file
text_file.close()