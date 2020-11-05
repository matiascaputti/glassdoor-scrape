from time import sleep
import random
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from selenium.webdriver.common.keys import Keys

def login(driver, email, password):
    """Login before search"""
    login_button = driver.find_element_by_class_name("sign-in")
    login_button.click()

    form = driver.find_element_by_name("emailSignInForm")

    user_email = form.find_element_by_id("userEmail")
    user_email.send_keys(email)

    user_password = form.find_element_by_id("userPassword")
    user_password.send_keys(password)

    user_password.send_keys(Keys.RETURN);
    sleep(3)
    return

def search_jobs(driver, job_title_input, location_input):
    """Enter query terms into search box and run job search"""
    form = driver.find_element_by_id("scBar")

    job_title = form.find_element_by_id("sc.keyword")
    job_title.clear()
    job_title.send_keys(job_title_input)

    location = form.find_element_by_id("sc.location")
    location.click()
    sleep(1)
    for i in range(1, 30):
        location.send_keys(Keys.BACK_SPACE)
    location.send_keys(location_input)

    location.send_keys(Keys.RETURN)
    sleep(2)
    return

def read_listings(driver, listings, job_count, idx, results):
    """take a list of job listings and record the title, company name, location, and description in a dictionary.
       Return the dictionary and an index representing the number of job listings stored"""
    for listing in listings:
        try:
            listing.click()
            print(f'{round(idx/job_count*100, 2)}%')
            
            #check for the pop-up
            try:
                driver.find_element_by_class_name("modal_closeIcon").click()
            except:
                pass

            details = driver.find_element_by_class_name("jobDetails")
            title = details.find_element_by_class_name("title").text
            company_name = details.find_element_by_class_name("employerName").text.split('\n')[0]
            company_location = details.find_element_by_class_name("location").text
            description = details.find_element_by_class_name("jobDescriptionContent.desc").text
            try:
                salary = details.find_element_by_class_name("salary").text
            except:
                salary = ''
            results[idx] =  {'title' : title, 'company' : company_name, 'location' : company_location, 'description' : description, 'salary': salary}
            idx += 1
        except:
            pass
    return idx, results

def create_df(results_dict):
    """convert a results dictionary into a pandas Dataframe (and drop duplicate entries)"""
    df = pd.DataFrame(results_dict, index=['company', 'description', 'location', 'salary', 'title'])
    df = df.transpose()
    print(str(sum(df.duplicated())) + " duplicates found.")
    df = df.drop_duplicates()
    print("dataframe created.")
    return df

def tokenize_description(description):
    """take a job description and return a list of tokens excluding stop words"""
    tokens = word_tokenize(description)
    stopset = set(stopwords.words('english'))
    tokens = [w.lower() for w in tokens if not w in stopset]
    text = nltk.Text(tokens)
    return list(set(text))
        
def find_skills_frequency(results_df):
    """count frequency of key words (as defined in dictionaries within function) appearing in job descriptions and return dataframe with skill frequency"""
    words = []
    for description in results_df['description']:
        words.append(tokenize_description(description))
    
    doc_frequency = Counter()
    [doc_frequency.update(word) for word in words]
    
    prog_lang_dict = Counter({
        'R': doc_frequency['r'],
        'Python': doc_frequency['python'],
        'Java': doc_frequency['java'],
        'C++': doc_frequency['c++'],
        'Julia': doc_frequency['julia'],
        'Perl': doc_frequency['perl'],
        'Scripting': doc_frequency['scripting'],
        'Linux': doc_frequency['linux'],
        'Matlab': doc_frequency['matlab'],
        'JavaScript': doc_frequency['javascript'],
        'Scala': doc_frequency['scala'],
        'Octave': doc_frequency['octave']
    })
                      
    analysis_tool_dict = Counter({
        'Excel': doc_frequency['excel'], 
        'Tableau': doc_frequency['tableau'],
        'NumPy': doc_frequency['numpy'],
        'Pandas': doc_frequency['pandas'],
        'Matplotlib': doc_frequency['matplotlib'],
        'Seaborn': doc_frequency['seaborn'],
        'D3.js': doc_frequency['d3'],
        'SAS': doc_frequency['sas'],
        'SPSS': doc_frequency['spss'],
        'D3': doc_frequency['d3'],
        'Spotfire': doc_frequency['spotfire'],
        'Stata': doc_frequency['stata'],
        'Power BI': doc_frequency['power bi'],
        'Plotly': doc_frequency['plotly'],
        'Looker': doc_frequency['looker'],
        'Airflow': doc_frequency['airflow']
    })

    machine_learning_dict = Counter({
        'sklearn': doc_frequency['scikit'],
        'NLP': doc_frequency['nlp'],
        'NLTK': doc_frequency['nltk'],
        'Keras': doc_frequency['keras'],
        'TensorFlow': doc_frequency['tensorflow'],
        'PyTorch': doc_frequency['pytorch'],
        'Theano': doc_frequency['theano'],
        'SageMaker': doc_frequency['sagemaker'],
        'H2O': doc_frequency['h2o'],
        'Caffe': doc_frequency['caffe'],
        'OpenCV': doc_frequency['opencv']
    })
                
    database_dict = Counter({
        'SQL': doc_frequency['sql'],
        'NoSQL': doc_frequency['nosql'],
        'MongoDB': doc_frequency['mongodb'],
        'MySQL': doc_frequency['mysql'],
        'Postgres': doc_frequency['postgres'],
        'Cassandra': doc_frequency['cassandra'],
        'Redshift': doc_frequency['redshift'],
        'DynamoDB': doc_frequency['dynamo'],
        'Redis': doc_frequency['redis']
    })

    cloud_dict = Counter({
        'Azure': doc_frequency['azure'],
        'AWS': doc_frequency['aws'],
        'GoogleCloud': doc_frequency['google cloud'],
    })

    edu_dict = Counter({
        'Bachelor': doc_frequency['bachelor'],
        'Master': doc_frequency['master'],
        'PhD': doc_frequency['phd'],
        'MBA': doc_frequency['mba']
    })

    education_dict = Counter({
        'Computer Science': doc_frequency['computer-science'],  
        'Statistics': doc_frequency['statistics'], 
        'Mathematics': doc_frequency['mathematics'],
        'Physics': doc_frequency['physics'], 
        'Machine Learning': doc_frequency['machine-learning'], 
        'Economics': doc_frequency['economics'], 
        'Software Engineer': doc_frequency['software-engineer'],
        'Information System': doc_frequency['information-system'], 
        'Quantitative Finance': doc_frequency['quantitative-finance']
    })

    big_data_dict = Counter({
        'Hadoop': doc_frequency['hadoop'],
        'MapReduce': doc_frequency['mapreduce'],
        'Spark': doc_frequency['spark'],
        'Pig': doc_frequency['pig'],
        'Hive': doc_frequency['hive'],
        'Shark': doc_frequency['shark'],
        'Oozie': doc_frequency['oozie'],
        'ZooKeeper': doc_frequency['zookeeper'],
        'Flume': doc_frequency['flume'],
        'Mahout': doc_frequency['mahout'],
        'Teradata': doc_frequency['teradata']
    })

    lang_dict = Counter({
        'French': doc_frequency['french'],
        'German': doc_frequency['german'],
        'Spanish': doc_frequency['spanish'],
        'Chinese': doc_frequency['chinese'],
        'Japanese': doc_frequency['japanese']
    })

    other_dict = Counter({
        'Decision making': doc_frequency['decision making'],
        'Japanese': doc_frequency['japanese']
    })

    skills = prog_lang_dict + analysis_tool_dict + machine_learning_dict + cloud_dict \
                + edu_dict + education_dict + big_data_dict + lang_dict + other_dict
    
    skills_frame = pd.DataFrame(list(skills.items()), columns = ['Term', 'NumPostings'])
    skills_frame.NumPostings = (skills_frame.NumPostings)*100/len(results_df)
    
    # Sort the data for plotting purposes
    skills_frame.sort_values(by='NumPostings', ascending = False, inplace = True)
    return skills_frame

