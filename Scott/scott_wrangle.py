import pandas as pd
import os
from datetime import datetime, timedelta
from env import get_db_url
import warnings
warnings.filterwarnings("ignore")


############ ACQUIRE LOGS FUNCTION ############

def acquire_logs():
    """
    Access the codeup server and return a dataframe of the logs table.
    
    """
    
    query = """
    select *
    from logs;
    """
    url = get_db_url('curriculum_logs')

    # Bring in the data
    df = pd.read_sql(query, url)

    return df


############ ACQUIRE COHORTS FUNCTION ############

def acquire_cohorts():
    """
    Access the codeup server and return a dataframe of the cohorts table.
    """
    query = """
    select *
    from cohorts;
    """
    url = get_db_url('curriculum_logs')

    # Bring in the data
    cohort_df = pd.read_sql(query, url)
    
    return cohort_df


############## ACQUIRE WEBTRAFFIC FUNCTION #############

def acquire_webtraffic():
    """
    Brings in the logs and cohort dataframes and joins them. Returns the resulting dataframe.
    """
    logs_df = acquire_logs()
    cohort_df = acquire_cohorts()
    
    cohort_df = cohort_df.rename(columns={'id': 'cohort_id'})
    df = pd.merge(logs_df, cohort_df, on='cohort_id', how='left')
    
    return df


############## PREP WEBTRAFFIC FUNCTION #################

def prep_webtraffic(df):
    """
    Takes in the dataframe and prepares it by settting the datetime index. Returns the prepared dataframe.
    """
    df.date = pd.to_datetime(df.date)
    df = df.set_index(df.date)
    df = df.drop(columns='date')
    
    return df


############### WRANGLE WEBTRAFFIC FUNCTION ##############

def wrangle_webtraffic():
    """
    Acquires and preps the webtraffic data. Outputs the resulting dataframe.
    """
    
    # Check if there's already a webtraffic.csv file, if there is, read it in
    if os.path.exists('webtraffic.csv'):
        df = pd.read_csv('webtraffic.csv')
        df = df.set_index(df.date)
        df = df.drop(columns='date')
        
    # If there isn't a webtraffic.csv file, acquire, prepare, and save it
    else:
        # Acquire and prepare the webtraffic data from the Codeup server 
        df = acquire_webtraffic()
        df = prep_webtraffic(df)

        # Save a .csv file of the prepared dataframe
        df.to_csv('webtraffic.csv')
    
    return df




