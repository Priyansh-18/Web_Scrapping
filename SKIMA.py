#!/usr/bin/env python
# coding: utf-8

# In[75]:


#import libraries to get data from webpage and tranfrom it to text
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


#webdriver path
path = '/Users/Bhatiya Priyansh/Downloads/chromedriver'
driver = webdriver.Chrome(path)

#create file that stores job title and jobpage link from home page where jobs are listed
#geting jobpage link reqired browser to run angular js scripts

url_file = pd.DataFrame({'URL':[],'JOB_TITLE':[]})

#dice.com don't have morethen 100 pages of joblisting
for i in range(1,101):
    website = f"https://www.dice.com/jobs?countryCode=US&radius=30&radiusUnit=mi&page={i}&pageSize=100&language=en"
    driver.get(website)
    time.sleep(5)
    elements = driver.find_elements(By.CLASS_NAME, 'card-title-link')
    for e in elements:
        url_data = pd.DataFrame({'URL':[e.get_attribute('href')],'JOB_TITLE':[e.text]})
        url_file = pd.concat([url_file, url_data], ignore_index=True)
        
#get the jobpage links to the csv file we got 10000 jobpage links in this process      
url_file.to_csv('url_file.csv')



#scrapping function
def Scrapper(input_file,output_file_name):
    excel = pd.read_csv(input_file)
    out = pd.DataFrame()
    
    #login credentioal
    data = {
            'email':'priyanshbhatiya@gmail.com',
            'password':'Priyansh@123'
        }
    #login page url
    login_url = "https://www.dice.com/dashboard/login"
    
    with requests.session() as s:
        s.post(login_url, data=data)

        
    for index, row in excel.iterrows():
        url = row['SURL']
          

        response = s.get(url)
        sop = BeautifulSoup(response.content, "html.parser")

        if sop.find_all(class_="mb-1 col-span-4 order-3 lg:order-2 md:col-span-8 lg:col-span-7"):
            job_title = sop.find_all(class_="mb-1 col-span-4 order-3 lg:order-2 md:col-span-8 lg:col-span-7")
        else:
            job_title 
            
            
        if sop.find_all(class_="list-none"):
            salary = sop.find_all(class_="list-none")
        else:
            salary = 0
            
        
        company = sop.find_all(class_="list-none companyInfo flex flex-wrap mb-1")
        location = sop.find_all(class_="bullet")
        skil = sop.find_all(class_="Skills_skillBadge__8_llv")
        jobdisc = sop.find_all(class_="mb-16 min-h-[300px]")


        analysis = {
            
            "URL": url,
            "Job_Title": [job_title[0].text] if job_title else ['None'],
            "SALARY": [salary[0].p] if salary else ['None'],
            "COMPANY": [company[0].text] if company else ['None'],
            "LOCATION": [location[0].text] if location else ['None'],
            "SKILLS": [i.text for i in skil],
            "JOB_DESCRIPTION": [i.text for i in jobdisc]
                        }
        
        

        out = out.append(analysis, ignore_index=True)
        print(index)
        

          
       
    
    return out.to_csv(output_file_name)


#excel file with job page urls
input_file = 'url_file.csv'

#name your output file 
output_file_name = 'final_output.csv'

#call scrapper function to get data in excel file from job site
Scrapper(input_file,output_file_name)




