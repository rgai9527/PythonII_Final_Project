from shiny import *
import pandas as pd
import pandas_datareader.data as web
import os
from shapely import wkt
from shapely.geometry import Point


root_path = r'/Users/catherine/Documents/GitHub/PythonII_Final_Project'
companies1_path = os.path.join(root_path, 'Company Screening 1.csv')
companies1 = pd.read_csv(companies1_path, skiprows=6)
companies1.columns = companies1.iloc[0]
companies1 = companies1.drop(labels=0, axis=0)

companies2_path = os.path.join(root_path, 'Company Screening 2.csv')
companies2 = pd.read_csv(companies2_path, skiprows=6)
companies2.columns = companies2.iloc[0]
companies2 = companies2.drop(labels=0, axis=0)


app_ui = ui.page_fluid(
    ui.input_select(id='C',label = 'Choose a company',choices = list(companies1['Company Name'] )),
    ui.input_select(id='Y',label = 'Choose a Year', choices = ['2018','2020']),
    ui.output_table('info')
    
)

def server(input, output, session):
    @reactive.Calc
    def get_dataframe_C1():
       df =pd.read_csv(r'/Users/catherine/Documents/GitHub/PythonII_Final_Project/Company Screening 1.csv', skiprows=6)
       df.columns = df.iloc[0]
       df = df.drop(labels=0, axis=0)
       return df[df['Company Name'] == input.C()]
  
    def get_dataframe_C2():
      companies2_path = os.path.join(r'/Users/catherine/Documents/GitHub/PythonII_Final_Project', 'Company Screening 2.csv')
      df2= pd.read_csv(companies2_path, skiprows=6)
      df2.columns = df2.iloc[0]
      df2 = df2.drop(labels=0, axis=0)
      return df2[df2['Company Name'] == input.C()]
    
    
    @output
    @render.table
    def info():
        if input.Y() == '2020':
          companies = get_dataframe_C1()
        else:
          companies = get_dataframe_C2()
        
        return companies


app = App(app_ui, server)
