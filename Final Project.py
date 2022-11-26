# Data Skills 2
# Autumn 2022
#
# Final Project
# by Ronghua Gai and Xinyu Liu
#
# Assignments
# 1. Data wrangling (G)
# 2. Plotting (L)
#	Two static
#	Two Shiny Interactive
# 3. Text processing (G)
#   Text analysis - HW3
# 4. Analysis (L)
#   Fit a model
# 5. Writeup (G)
# 	2-3 pages
#
#
# #################################################
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup



### Part 1
# Change your base path HERE!!!
base_path = r'/Users/simonking/Documents/GitHub/Python II/PythonII_Final_Project'


# Set the paths, read the CapIQ csv fiels, and do basic cleaning
companies1_path = os.path.join(base_path, 'Company Screening 1.csv')
companies2_path = os.path.join(base_path, 'Company Screening 2.csv')

companies1 = pd.read_csv(companies1_path, skiprows=6)
companies1.columns = companies1.iloc[0]
companies1 = companies1.drop(labels=0, axis=0)

companies2 = pd.read_csv(companies2_path, skiprows=6)
companies2.columns = companies2.iloc[0]
companies2 = companies2.drop(labels=0, axis=0)


# Parse the online dataset
response = requests.get('https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html', verify=False)
soup = BeautifulSoup(response.text, 'lxml')

table = soup.find('table')
industries_rows = []
for row in table.find_all('tr'):
    tds = row.find_all('td')
    industries_rows.append([' '.join(val.text.split()) for val in tds])  
    
industries = pd.DataFrame(industries_rows)
industries.columns = industries.iloc[0].str.strip()
industries = industries.drop(labels=[0,97], axis=0)





### Part 2










### Part 3












### Part 4







