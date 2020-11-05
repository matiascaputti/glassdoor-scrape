# Scraping Glassdoor to Determine Highest Demand Job Skills

I started out trying to use **Beautiful Soup** to parse the raw html, but quickly found that many of the large employers and top job sites do not include job posting text in the raw HTML. Rather it seems that they are populating the job posting data into the DOM using Javascript. This makes things a bit more complicated, but not insurmountable.

Instead of Beautiful Soup, I ended up using a tool called **Selenium (python library)** to select DOM elements and scrape. Selenium is a browser driver, ie. automated browser that can programmaticaly emulate any actions a normal user would do. I used **chromedriver** since I was working with Chrome. This driver can be found in `utils/chromecriver`.

Finally, I used **nltk** in conjunction with collections to count keywords in job postings; **pandas** to create dataframes to structure the data and **pickle** to save dataframe objects for archival purposes.


## Glassdoor credentials

Create a `.env` file with your Glassdoor credentials following `.env.template` structure.


## Run scraping script

This python script will scrape Glassdoor job postings. This is actually in two files - `scrape_glassdoor.py` (main) and `utils/helpers.py` (helper functions).

`python scrape_glassdoor.py`


## Data wrangling and analysis

Open and execute `1- Read data.ipynb` Jupyter Notebook cells.

Originally I had hoped to apply some NLP machine learning techniques, primarly keyword extraction. I experimented with a RAKE algorithm for keyword/phrase extraction. Unfortunately, the best results I got were much less useful than hardcoding the anticipated keywords and counting from the hardcoded dictionaries.

The analysis in the Jupyter Notebook shows a pareto of skills as well as a simple "80/20" type analysis. I may come back to this project in the future to do some more NLP analysis using the corpus of job postings that I scraped.


#### Sources

https://github.com/natmod/glassdoor-scrape
https://github.com/nanthasnk/Glassdoor-Jobs-Salary-Prediction
