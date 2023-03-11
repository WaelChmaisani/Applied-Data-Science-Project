# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

# Create a dash application
app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                      html.Div(
                                         dcc.Dropdown(id='site-dropdown',
                                         options=[
                                         {'label': 'All Sites', 'value': 'ALL'},
                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                         ],
                                         value='ALL',
                                         placeholder="Select a Launch Site here",
                                         searchable=True
                                         )),

                                         html.Div(dcc.Graph(id='success-pie-chart')),


                     html.Div([      html.Div(html.H2('Payload range (kg):', style={'margin-right': '2em'})), 
                         
                                         
                                     dcc.RangeSlider(id='payload-slider',
                                                    min=0, max=10000, step=1000,
                                                    marks={0: '0',2500: '2500',5000: '5000',10000: '10000'},
                                                    value=[spacex_df["Payload Mass (kg)"].min(), spacex_df["Payload Mass (kg)"].max()])
                              ]),
                                     
                                     html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                       ])

# Function decorator to specify function input and output
@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
              Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")] )              

def get_pie_chart(entered_site,slider_range):
    filtered_df = spacex_df
    low, high = slider_range
    mask = (filtered_df["Payload Mass (kg)"] > low) & (filtered_df["Payload Mass (kg)"] < high)
    if entered_site == 'ALL':
        fig1 = px.pie(filtered_df, values='class',names='Launch Site', title='Total Success Launches by site')
        fig2 = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y="class", title='Correlation between Payload and Success for all Sites',color="Booster Version Category")
        return [fig1,fig2]
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        fig1 = px.pie(filtered_df, names='class', title="Total Success Launches for site" + " " + str(entered_site))
        fig2 = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y="class", title='Correlation between Payload and Success for Site'+ " " + str(entered_site),color="Booster Version Category")
        return [fig1,fig2]


# Run the application                   
if __name__ == '__main__':
    app.run_server()