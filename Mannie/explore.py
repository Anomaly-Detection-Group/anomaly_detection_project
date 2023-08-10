# Initial imports
import pandas as pd

from datetime import datetime, timedelta

from env import get_db_url

import scott_wrangle


import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings("ignore")

def chart1(): 

    # bring in  df
    df = scott_wrangle.wrangle_webtraffic()

    # Filter the dataframe to just student entries in 2019 and stores it in the filtered dataframe 'df_f'
    df_f = df[(df.index > '2018-12-31') & (df.index < '2020-01-01') & (df.name != 'Staff')]

    # Create a dataframe of the 2019 data, from data science students
    ds_traffic = pd.DataFrame(df_f[df_f.program_id == 3].path.value_counts()).reset_index().rename(columns={'path': 'traffic_vol'})\
    .rename(columns={'index': 'path'})

    # Create a dataframe of the 2019 data, from data science students
    ds_traffic = pd.DataFrame(df_f[df_f.program_id == 3].path.value_counts()).reset_index().rename(columns={'path': 'traffic_vol'})\
    .rename(columns={'index': 'path'})

    # Create a dataframe of the 2019 data, groupby traffic volume (each traffic amount theoretically is unique to each path)
    # and sort to start with the highest volume paths first
    temp = pd.merge(df_f[(df_f.program_id == 3) & (df_f.path != '/')], ds_traffic, on='path', how='left').groupby('traffic_vol')\
    ['path', 'traffic_vol'].max().sort_index(ascending=False)

    # Plot the figure
    plt.figure(figsize=(10, 30)) 
    plt.barh(temp["path"], temp["traffic_vol"])
    plt.xlabel("Traffic Volume")
    plt.ylabel("Path")
    plt.title("Traffic Volume by Path")
    plt.yticks(fontsize=5)
    plt.grid(axis='x')
    plt.tight_layout()

# Create a dataframe of the 2019 data, groupby traffic volume (each traffic amount theoretically is unique to each path)
# and sort to start with the highest volume paths first

# temp = pd.merge(df_f[(df_f.program_id == 3) & (df_f.path != '/')], ds_traffic, on='path', how='left').groupby('traffic_vol')\
# ['path', 'traffic_vol'].max().sort_index(ascending=False)

def chart2(): 

    # bring in  df
    df = scott_wrangle.wrangle_webtraffic()

    # Filter the dataframe to just student entries in 2019 and stores it in the filtered dataframe 'df_f'
    df_f = df[(df.index > '2018-12-31') & (df.index < '2020-01-01') & (df.name != 'Staff')]

    # Make a list of webdev paths that were accessed by ds students
    check_paths = ['error-pages/asdfasdf', 'jquery', 'spring', 'java-i', 'toc', 'javascript-i', 'html-css']

    # Set the datetime cause apparently it wasn't actually set earlier somehow
    df_f.index = pd.to_datetime(df_f.index)
    df.index = pd.to_datetime(df.index)

    # create and plot a dataframe of 2019 traffic from ds students that matches the identified webdev paths aggregate to count the number
    # of times a path was accessed in a day
    df[(df.program_id == 3) & (df.path.str.contains('|'.join(check_paths)) & (df.name != 'Staff') )].resample('D').path.agg('count').plot()


def webdev():

    # bring in  df
    df = scott_wrangle.wrangle_webtraffic()

    # Display the paths that resulted in the top 30% of traffic to extract the topics that were revisited by webdev grads
    webdev = df[(df.index > pd.to_datetime(df.end_date) + timedelta(days=4*30)) & (df.program_id == 2)]\
    .groupby('path').time.count().sort_values(ascending=False).head(23)

    return webdev


def data_science():

    # bring in  df
    df = scott_wrangle.wrangle_webtraffic()

    # Display the paths that resulted in the top 30% of traffic to extract the topics that were revisited by webdev grads
    ds = df[(df.index > pd.to_datetime(df.end_date) + timedelta(days=4*30)) & (df.program_id == 2)]\
    .groupby('path').time.count().sort_values(ascending=False).head(23)

    return ds