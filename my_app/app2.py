from shiny import *
import pandas as pd
import pandas_datareader.data as web
import os
from shapely import wkt
from shapely.geometry import Point
import matplotlib.pyplot as plt


root_path = r'/Users/catherine/Documents/GitHub/PythonII_Final_Project'
companies1_path = os.path.join(root_path, 'Company Screening 1.csv')
companies1 = pd.read_csv(companies1_path, skiprows=6)
companies1.columns = companies1.iloc[0]
companies1 = companies1.drop(labels=0, axis=0)
companies1 = companies1.replace( '[\$,)]','', regex=True ).replace( '[(]','-',   regex=True )

cols1 = ['Market Capitalization [My Setting] [01/01/2020] ($USDmm, Historical rate)','Total Enterprise Value [My Setting] [01/01/2020] ($USDmm, Historical rate)',
         '2 Year Beta [Latest]','% Price Change [01/01/2020-12/31/2021]']
companies1[cols1]=companies1[cols1].astype(float)

companies2_path = os.path.join(root_path, 'Company Screening 2.csv')
companies2 = pd.read_csv(companies2_path, skiprows=6)
companies2.columns = companies2.iloc[0]
companies2 = companies2.drop(labels=0, axis=0)
companies2 = companies2.replace( '[\$,)]','', regex=True ).replace( '[(]','-',   regex=True )

cols2 = ['Market Capitalization [My Setting] [01/01/2021] ($USDmm, Historical rate)','Total Enterprise Value [My Setting] [01/01/2021] ($USDmm, Historical rate)',
         '2 Year Beta [Latest]','% Price Change [01/01/2018-12/31/2019]']

companies2[cols2]=companies2[cols2].astype(float)

df = companies1.merge(companies2, how='inner', on = ['Company Name','Exchange:Ticker','Geographic Locations'])

#shiny part

app_ui = ui.page_fluid(
    #Adjust the styles to center everything
    ui.tags.style("#container {display: flex; flex-direction: column; align-items: center;}"),
    #Main container div
    ui.tags.div(
    ui.h2('Company Basic Information'),
    ui.input_select(id='C',label = 'Choose a company',choices = list(df['Company Name'] )),
    ui.output_plot('viz'),
    ui.output_table('info'),
    id = 'container')
)

def server(input, output, session):
    @reactive.Calc
    def get_dataframe_merge():
       df = companies1.merge(companies2, how='inner', on = ['Company Name','Exchange:Ticker','Geographic Locations'])
       df = df.drop(['Exchange:Ticker','2 Year Beta [Latest]_y'], axis=1)
       df = df.rename(columns={'Market Capitalization [My Setting] [01/01/2020] ($USDmm, Historical rate)':'Market Cap in 2020',
                       'Total Enterprise Value [My Setting] [01/01/2020] ($USDmm, Historical rate)': 'Enterprise Value 2020',
                       '2 Year Beta [Latest]_x': 'Beta','Market Capitalization [My Setting] [01/01/2021] ($USDmm, Historical rate)':'Market Cap in 2021',
                       'Total Enterprise Value [My Setting] [01/01/2021] ($USDmm, Historical rate)': 'Enterprise Value 2021','% Price Change [01/01/2020-12/31/2021]':'% Price Change 2020-2021',
                       '% Price Change [01/01/2018-12/31/2019]':'% Price Change 2018-2019'})
       new_cols = ['Company Name','Beta','Geographic Locations','Market Cap in 2020',
                  'Market Cap in 2021',
                   'Enterprise Value 2020','Enterprise Value 2021',
                  '% Price Change 2018-2019','% Price Change 2020-2021'
                   ]
       df =df.reindex(columns=new_cols)
       
       return df[df['Company Name'] == input.C()]
  
    @output
    @render.plot
    def viz():
        
    #bar plot visualization of market value, enterprise value in 2018 and 2020
     information = get_dataframe_merge()
     new_merge = information.drop(['Beta','% Price Change 2018-2019','% Price Change 2020-2021'],axis=1)
     new_merge = new_merge.set_index('Company Name')
     new_merge = new_merge.T.reset_index()
     new_merge= new_merge.rename(columns = {0:'Value'})
     new_merge = new_merge.set_index('Value')
     new_merge = new_merge.drop(['Geographic Locations'], axis=0)
     new_merge = new_merge.reset_index()
     fig,axes = plt.subplots(1,2)
     new_merge.plot.bar(x='Value', ax=axes[0])
     
    #line plot for price change 
          
     price_change = information[['Company Name','% Price Change 2018-2019','% Price Change 2020-2021']]
     price_change = price_change.rename(columns={'% Price Change 2020-2021':'2020-2021','% Price Change 2018-2019':'2018-2019'})
     price_change = price_change.set_index('Company Name')
     price_change = price_change.T.reset_index()
     price_change = price_change.rename(columns={0:'Year'})
     price_change.plot(x = 'Year',ax=axes[1])
     return fig
    
     
      
   
    
    @output
    @render.table
    def info():
        companies = get_dataframe_merge()
        
        return companies


    
        
        

app = App(app_ui, server)