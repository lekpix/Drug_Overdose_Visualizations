# Dependencies
import dash
#import dash_html_components as html
from dash import html
# import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input,Output

import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np
import requests
from census import Census

# Import password and api key
from config2 import api_key, password  

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect


import matplotlib.pyplot as plt
import plotly.express as px


# Create a connection to database

engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/Census_DB') #drug_connecticut_db
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Census=Base.classes.census_ct
Drug_Master=Base.classes.drug_master
Drug_Type=Base.classes.drug_type

# Create our session (link) from Python to the DB
session=Session(engine)

app=dash.Dash(__name__)
# ---------------------------------------------------------------------------------------------
#Querying the database
Total_Death_Year=session.query(Drug_Type.year,func.count(Drug_Type.id)).group_by(Drug_Type.year).order_by(Drug_Type.year.desc()).all()
# Save the query results as a Pandas DataFrame and set the index to the date column

Total_Death_Year_DF=pd.DataFrame(Total_Death_Year,columns=["Year","Total_Death"])
# Total_Death_Year_DF

#----------------------------------------------------------------------------------------------
#App Layout
app.layout=html.Div(children=[
    html.H1(children="Drug Overdose Dashboard"),
    # dcc.Dropdown(id='Sel_Graph',
    # options=[
    #     {"label":"Year wise","value":Total_Death_Year_DF},
    #     {"label":"County wise","value":Total_Death_Year_DF}
    # ],
    # value=Total_Death_Year_DF),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    dcc.Graph(id='Total_death_YEAR')
])

@app.callback(
    Output(component_id='Total_death_YEAR',component_property='figure'),
    Input(component_id='my-input', component_property='value')
    
)
def update_graph(input):
    fig = px.line(Total_Death_Year_DF, x="Year", y="Total_Death")#, color="Total_Death",
# #      line_group="Total_Death")
# fig.show()
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)