# Data Skills 2
# Autumn 2022
#
# Final Project
# by Ronghua Gai and Xinyu Liu
#
#
# Assignments:
# 1. Data wrangling (GAI)
# 2. Plotting (LIU)
# 3. Text processing (GAI)
# 4. Analysis (LIU)
# 5. Writeup (GAI)
#
#
#
# #################################################
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import spacy
import pycountry
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from spacytextblob.spacytextblob import SpacyTextBlob





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

#1 static plot for specific industries including
#Air transport, computer service, pharma drugs, food wholesaler, gas product, real estate general industries

    #select specific industries
industries = industries.reset_index()
spe_indus = ['Air Transport', 'Computer Services', 'Drugs (Pharmaceutical)', 'Food Wholesalers', 'Oil/Gas (Production and Exploration)', 'Real Estate (General/Diversified)','Total Market']
indu_spe = industries[industries['Industry Name'].isin(spe_indus)]
indu_spe = indu_spe.set_index('Industry Name')
    #convert the type to float
indu_spe = indu_spe.iloc[:,11:14].astype(float).T
    #plot
indu_spe.plot.line()
plt.legend(bbox_to_anchor=(1.0, 1.0))



#2Heatmap of Individual firms??? latest 2-year Beta vs. % Price Change 
   #merge companies1 and 2
merge = companies1.merge(companies2, how='inner', on = ['Company Name','Exchange:Ticker','Geographic Locations'])
 
   #create a new dataframe contained year, 2-year beta
heat_frame = merge[['Company Name','2 Year Beta [Latest]_x','2 Year Beta [Latest]_y','% Price Change [01/01/2020-12/31/2021]','% Price Change [01/01/2018-12/31/2019]']]
heat_frame = heat_frame.set_index('Company Name')
heat_frame = heat_frame.replace( '[\$,)]','', regex=True ).replace( '[(]','-',   regex=True ).astype(float)
  
   #create a new dataframe indicates the numbers of companies in specific range of beta
max_beta = 50
min_beta = -20
interval = (max_beta-min_beta)/5
def find_numbers(S1,v1,v2):
    number = 0
    for a in S1:
        if min(v1,v2)<= a <= max(v1,v2):
            number+=1 
    return number

price_range = [(float('-inf'),-100),(-100,-50),(-50,0),(0,50),(50,100),(100,150),
             (150,200),(200,250),(250,300),(300,350),(350,400),(400,450),(450,500),(500,float('inf'))]

number_list_2020 = []
number_list_2018 = []
for a in price_range:
    number_list_2020.append(find_numbers(heat_frame['% Price Change [01/01/2020-12/31/2021]'],a[0],a[1]))

for b in price_range:
    number_list_2018.append(find_numbers(heat_frame['% Price Change [01/01/2018-12/31/2019]'],b[0],b[1]))

df_heat = pd.DataFrame ({'%_Price_change_range':price_range,'2020':number_list_2020, '2018':number_list_2018})
df_heat = df_heat.set_index('%_Price_change_range')

    #plot the heat map of x-year, y-beta range, numbers of companies
fig, ax = plt.subplots(figsize=(13,7))
sns.heatmap(df_heat,fmt="",cmap='RdYlGn',ax=ax)



   #plot the heat map of x-year, y-beta range, numbers of companies

#3 interactive plots for industry beta 

#organize the industries dataframe
    #transpose the industries dataframe
industries = industries.set_index('Industry Name')
industry_beta = industries.iloc[:,11:14]
industry_beta = industry_beta.T
    #transform to numeric column of 2018, 2019,2020,2021 beta
industry_beta= industry_beta.astype(float)
    #to be continued
print(industries.loc['Advertising']['Beta'])





### Part 3

# Set up the base path
text_path = os.path.join(base_path, 'Texts') 
textfig_path = os.path.join(base_path, 'Text_Processing_plot.png')  


# Create a dictionary to restore all refugee text files
reports = {}
for file in os.listdir(text_path):
    if file.endswith(".txt"):
        file_path = os.path.join(text_path, file)
        with open(file_path, 'r') as f:
            reports[file[:-4]] = f.readlines()


# Convert the dictionary into dataframe, clean and merge the data, prepare for intepretation
## Conversion
reports_clean = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in reports.items() ]))

## Drop blank rows
reports_clean = reports_clean.drop([2,4,6,8,10])

## Merge rows together,reset index, and clean the data
reports_clean = reports_clean.apply(lambda x: ''.join(x.astype(str))).reset_index()
reports_clean = reports_clean.rename({0: 'Text', 'index': 'Date'}, axis=1)
reports_clean = reports_clean.applymap(lambda x: x.replace('\n', '. ').replace('..', '.'))
reports_clean = reports_clean.sort_values(by='Date').reset_index().drop(columns=['index'])


# Analyze the sentiment of each article
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob');

## Add a new column to store sentiment levels
reports_clean['Sentiment'] = 0
for i in range(len(reports_clean['Text'])):
    reports_clean.iloc[i,2] = nlp(reports_clean.iloc[i,1])._.blob.polarity


# Plot the sentiments
fig = plt.figure()
fig, ax = plt.subplots()
plt.rcParams["figure.figsize"] = [8, 4]
plt.rcParams["figure.autolayout"] = True
ax.plot(reports_clean['Date'], reports_clean['Sentiment'], 'b*-')
ax.set_xlabel('Year 2022')
ax.set_ylabel('Sentiment')
ax.set_title('US Stock Market Sentiments')
plt.savefig(textfig_path)












### Part 4















