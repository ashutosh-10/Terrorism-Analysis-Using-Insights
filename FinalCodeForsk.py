


import pandas as pd
import webbrowser

import dash
import dash_html_components as html
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import plotly.graph_objects as go  
import plotly.express as px



app = dash.Dash()
project_name = None


def load_data():
    dataset_name = "global_terror.csv"
  
    global df
    df = pd.read_csv(dataset_name)
  
    global month_list
    month = {
           "January":1,
           "February": 2,
           "March": 3,
           "April":4,
           "May":5,
           "June":6,
           "July": 7,
           "August":8,
           "September":9,
           "October":10,
           "November":11,
           "December":12
           }
    month_list= [{"label":key, "value":values} for key,values in month.items()]
  
    global region_list
    temp_list = sorted( df['region_txt'].unique().tolist())
    region_list = [{"label": str(i), "value": str(i)}  for i in temp_list  ]
    
    global attack_type_list
    temp_list = df['attacktype1_txt'].unique().tolist()
    attack_type_list = [{"label": str(i), "value": str(i)}  for i in temp_list]
  
    global year_list
    year_list = sorted ( df['iyear'].unique().tolist()  )
  
    global year_dict
    year_dict = {str(year): str(year) for year in year_list}


def open_browser():
    
    webbrowser.open_new('http://127.0.0.1:8050/')



def create_app_ui():

    main_layout = html.Div(
    [
    html.H1('Terrorism Analysis with Insights', id='Main_title'),
    dcc.Dropdown(
          id='month-dropdown', 
          options=month_list,
          placeholder='Select Month',
    ),
    dcc.Dropdown(
          id='date-dropdown', 

          placeholder='Select Day',
    ),
            
    dcc.Dropdown(
          id='region-dropdown', 
          options=region_list,
          placeholder='Select Region',
    ),
    dcc.Dropdown(
          id='country-dropdown', 
          options=[{'label': 'All', 'value': 'All'}],
          placeholder='Select Country'
    ),
    dcc.Dropdown(
          id='state-dropdown', 
          options=[{'label': 'All', 'value': 'All'}],
          placeholder='Select State or Province'
    ),
    dcc.Dropdown(
          id='city-dropdown', 
          options=[{'label': 'All', 'value': 'All'}],
          placeholder='Select City'
    ),
            
            
    dcc.Dropdown(
          id='attacktype-dropdown', 
          options=attack_type_list,
          placeholder='Select Attack Type'
    ),
  
    html.H5('Select the Year', id='year_title'),
    dcc.RangeSlider(
          id='year-slider',
          min=min(year_list),
          max=max(year_list),
          value=[min(year_list),max(year_list)],
          marks=year_dict
    ),
    html.Br(),
    dcc.Loading(dcc.Graph(id='graph-object', figure = go.Figure()))

    ]
    )
    
    return main_layout



@app.callback(
    Output('graph-object', 'figure'),
    [
    Input('month-dropdown', 'value'),
    Input('date-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('state-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('attacktype-dropdown', 'value'),
    Input('year-slider', 'value')
    ]
    )
def update_app_ui(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value):
  
    print("Data Type of month value = " , str(type(month_value)))
    print("Data of month value = " , month_value)
    
    print("Data Type of Day value = " , str(type(date_value)))
    print("Data of Day value = " , date_value)
    
    print("Data Type of region value = " , str(type(region_value)))
    print("Data of region value = " , region_value)
    
    print("Data Type of country value = " , str(type(country_value)))
    print("Data of country value = " , country_value)
    
    print("Data Type of state value = " , str(type(state_value)))
    print("Data of state value = " , state_value)
    
    print("Data Type of city value = " , str(type(city_value)))
    print("Data of city value = " , city_value)
    
    print("Data Type of Attack value = " , str(type(attack_value)))
    print("Data of Attack value = " , attack_value)
    
    print("Data Type of year value = " , str(type(year_value)))
    print("Data of year value = " , year_value)
  
    figure = go.Figure()


    year_range = range(year_value[0], year_value[1]+1)

    new_df = df[df["iyear"].isin(year_range)]
    

    if month_value is None:
        pass
    else:
        if date_value is None:
            new_df = new_df[new_df["imonth"]==month_value]
                            
        else:
            new_df = new_df[(new_df["imonth"]==month_value)&
                             (new_df["iday"]==date_value)]

    if region_value is None:
        pass
    else:
        if country_value is None:
            new_df = new_df[new_df["region_txt"]==region_value]
        else:
            if state_value is None:
                new_df = new_df[(new_df["region_txt"]==region_value)&
                                (new_df["country_txt"]==country_value)]
            else:
                if city_value is None:
                    new_df = new_df[(new_df["region_txt"]==region_value)&
                                (new_df["country_txt"]==country_value) &
                                (new_df["provstate"]==state_value)]
                else:
                    new_df = new_df[(new_df["region_txt"]==region_value)&
                                (new_df["country_txt"]==country_value) &
                                (new_df["provstate"]==state_value)&
                                (new_df["city"]==city_value)]
    
                   
    if attack_value is None:
        pass
    else:
        new_df = new_df[new_df["attacktype1_txt"]==attack_value]
      

                        
    if new_df.shape[0]:
        pass
    else: 
        new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
       'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
        
        new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
   
    
    figure = px.scatter_mapbox(new_df,
                  lat="latitude", 
                  lon="longitude",
                  color="attacktype1_txt",
                  hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                  zoom=1
                  )                       
    figure.update_layout(mapbox_style="open-street-map",
              autosize=True,
              margin=dict(l=0, r=0, t=25, b=20),
              )
  
    return figure
      

@app.callback(
  Output("date-dropdown", "options"),
  [Input("month-dropdown", "value")])
def update_date(month):
    date_list = [x for x in range(1, 32)]

    if month in [1,3,5,7,8,10,12]:
        return [{"label":m, "value":m} for m in date_list]
    elif month in [4,6,9,11]:
        return [{"label":m, "value":m} for m in date_list[:-1]]
    elif month==2:
        return [{"label":m, "value":m} for m in date_list[:-2]]
    
    else:
        return []


@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    
    return[{"label": str(i), "value": str(i)}  for i in df[df['region_txt'] == region_value] ['country_txt'].unique().tolist() ]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
    
    return [{"label": str(i), "value": str(i)}  for i in df[df['country_txt'] == country_value] ['provstate'].unique().tolist() ]


@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
    
    return [{"label": str(i), "value": str(i)}  for i in df[df['provstate'] == state_value] ['city'].unique().tolist() ]


def main():
    load_data()
    
    open_browser()
    
    global project_name
    project_name = "Terrorism Analysis with Insights" 
      
      
    global app
    app.layout = create_app_ui()
    app.title = project_name
    
    app.run_server() 
  
    print("This would be executed only after the script is closed")
    app = None
    project_name = None


if __name__ == '__main__':
    main()
