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
    #Adjust the styles to center everything
    ui.tags.style("#container {display: flex; flex-direction: column; align-items: center;}"),
    #Main container div
    ui.tags.div(
    ui.h2('Unlevered Beta corrected for Cash in Each Industry'),
    ui.input_select(id='I',label = 'Choose an industry',choices = list(industries['Industry Name'] )),
    ui.output_plot('viz'),
    ui.output_table('table'),
    id='container')
    
)

def server(input, output, session):
    @reactive.Calc
    def get_industry():
        industry =  industries[industries['Industry Name'] == input.I()]
        return industry[['Industry Name','2018','2019','2020','2021']]
   
        
        
    @output
    @render.table
    def table():
        industry = get_industry()
        
        return industry
    
    
    @output
    @render.plot
    def viz():
        industry = get_industry()
        industry = industry.set_index('Industry Name')
        industry = industry.astype(float)
        industry = industry.T.reset_index()
        industry= industry.rename(columns = {0:'Year'})
        fig,ax = plt.subplots()
        ax.plot(industry['Year'],industry.iloc[:,1])
        ax.scatter(industry['Year'],industry.iloc[:,1])
        ax.set_title(f"{input.I()} Unlevered Beta")
        return fig
        
app = App(app_ui, server)