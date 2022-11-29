import requests
from bs4 import BeautifulSoup
from shiny import *
import pandas as pd
import geopandas
from geopandas import gpd
import pandas_datareader.data as web
import os
import matplotlib.pyplot as plt
from shapely import wkt
from shapely.geometry import Point

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



app_ui = ui.page_fluid(
    ui.input_select(id='I',label = 'Choose an industry',choices = list(industries['Industry Name'] )),
    ui.output_text('txt')
    
)

def server(input, output, session):
    @reactive.Calc
    def get_industry():
        idf = industries.set_index('Industry Name')
        return idf
    
    
    
    @output
    @render.text
    def txt():
        industry = get_industry()
        number = industry.loc[input.I()]['Beta']
        return 'Beta is '+number


app = App(app_ui, server)
