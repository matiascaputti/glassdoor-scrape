from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from utils.helpers import login
from utils.helpers import search_jobs
from utils.helpers import read_listings
import random
import pickle 
import os
from dotenv import load_dotenv


project_folder = path = os.getcwd()
load_dotenv(os.path.join(project_folder, '.env'))

driver = webdriver.Chrome('./utils/chromedriver')
driver.implicitly_wait(1)
driver.maximize_window()

#define job posting search
url = "https://www.glassdoor.com"
job_title_input = "data scientist"
location_input = "new york"

driver.get(url)

email = os.getenv("GLASSDOOR_EMAIL")
password = os.getenv("GLASSDOOR_PASSWORD")
login(driver, email, password)

search_jobs(driver, job_title_input, location_input)

#initialize loop variables
idx = 1
results = {}
#find total number of job postings
job_count_field = driver.find_element_by_class_name("jobsCount")
job_count = int(job_count_field.get_attribute('textContent').split('\xa0')[0].replace('.', ''))
# import pdb; pdb.set_trace()
print(f'SEARCHING... {job_count} jobs found...')

while True:
    #let user know the scraping has started
    #find job listing elements on web page
    listings = driver.find_elements_by_class_name("jl")
    #read through job listings and store index and results
    idx, results = read_listings(driver, listings, job_count, idx, results)
    #find "next" button to go to next page of job listings
    next_btn = driver.find_element_by_class_name("next")
    #if there is no next button, finish the search
    if len(next_btn.find_elements_by_class_name("disabled ")) != 0:
        print("FINISHED")
        break
    #if the job listing index is higher than the total number of job postings found from the search, finish the search
    if idx > job_count:
        break
    #click the next button
    next_btn.click()
    #tell webdriver to wait until it finds the job listing elements on the new page
    WebDriverWait(driver, 100).until(lambda driver: driver.find_elements_by_class_name("jl"))
    sleep(5)

#archive search using pickle
with open(f'{job_title_input.replace(' ', '-')}_{location_input.replace(' ', '-')}.pickle', 'wb') as handle:
    pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

# close the browser window
driver.quit()
