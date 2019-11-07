from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate
import time

import re
import json
login_url='https://www.freelancer.com/login'
info_url="https://www.freelancer.com/search/python/"
df=pd.DataFrame()
job_list=[]
days_list=[]
prices_list=[]
numBids_list=[]
desc_list=[]
link_list=[]
data=[]
max_num_pages=6

def check_jobs():
    #iterate through each page
    for i in range(max_num_pages):
        #get the page using requests
        r = requests.get(info_url+'/'+str(i))
        #convert the html to an iterable BS4 object
        soup = BeautifulSoup(r.text, "lxml")

        # get the job postings
        jobs = soup.find_all("a", class_="JobSearchCard-primary-heading-link")
        for job in jobs:
            #
            job=job.text
            job=job.strip()
            job=job.replace('\n','')
            job = job.replace('\t', '')
            job = job.strip('/n')
            job_list.append(job)

        # get the days left
        days = soup.find_all("span", class_="JobSearchCard-primary-heading-days")
        for day in days:
            days_list.append(day.text)

        # get the prices and bids
        prices = soup.find_all("div", class_="JobSearchCard-secondary")
        for price in prices:
            #do some text processing
            price = price.text.replace("Avg Bid",'')
            price = price.replace("Bid now", '')
            price = price.strip()
            price = price.replace('\n','')
            price = price.replace('\t', '')
            price = price.strip('/n')
            #seperate the num bid from price and store them
            price_str=""
            bid_str=""
            switch=True
            for char in price:
                if(char==' '):
                    switch=False
                if(char=='/' or char=='h' or char=='r'):
                    switch=True
                if(switch):
                    price_str+=char
                if(not switch):
                    if (char == 'b'):
                        bid_str += ' '
                    if(char!=' '):
                        bid_str+=char

            prices_list.append(price_str)
            numBids_list.append(bid_str)

        # get the description
        descriptions = soup.find_all("p", class_="JobSearchCard-primary-description")
        for description in descriptions:
            description=description.text.strip()
            desc_list.append(description)
        for link in soup.find_all("a", class_="JobSearchCard-primary-heading-link"):
            link=link.get('href')
            link2='https://www.freelancer.com'+link
            link_list.append(link2)



    #
def update_df():
    df = pd.DataFrame()
    df['Job'],df['Price'],df['Days Until Expire'], df['# Bids'],df['Description'],df['link']=job_list,prices_list, days_list, numBids_list,desc_list,link_list
    df=df.drop_duplicates()
    df=df.sort_index(ascending=0)
    print(tabulate(df, headers='keys',tablefmt='psql'))

if __name__ == "__main__":
    while(True):
        check_jobs()
        update_df()
        time.sleep(40)


