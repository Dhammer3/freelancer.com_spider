from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate
import re
import json
login_url='https://www.freelancer.com/login'
info_url="https://www.freelancer.com/search/python/"

job_list=[]
days_list=[]
prices_list=[]
numBids_list=[]
desc_list=[]
link_list=[]
data=[]
max_num_pages=6

def check_jobs():
    for i in range(max_num_pages):
        r = requests.get(info_url+'/'+str(i))
        soup = BeautifulSoup(r.text, "lxml")

        # get the job postings
        jobs = soup.find_all("a", class_="JobSearchCard-primary-heading-link")
        for job in jobs:
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
            price = price.text.replace("Avg Bid",'')
            price = price.replace("Bid now", '')
            price=price.strip()
            price=price.replace('\n','')
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
            description=description.text
            description = description.strip()
            #print(description)
            #print("===================================")
            desc_list.append(description)
        for link in soup.find_all("a", class_="JobSearchCard-primary-heading-link"):
            link=link.get('href')
            link2='https://www.freelancer.com'+link
            link_list.append(link2)



    #

check_jobs()

#data=[job_list, prices_list, days_list, numBids_list, desc_list]

df=pd.DataFrame()
df['Job']=job_list
df['Price']=prices_list
df['Days Until Expire']=days_list
df['# Bids']=numBids_list
df['Description']=desc_list
df['link']=link_list
print(tabulate(df, headers='keys',tablefmt='psql'))
