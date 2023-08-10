# imports
import pandas as pd
import numpy as np
import env

# get and clean data
def wrangle_codeup():
    """
    Goal: To return clean cohort and logs data from codeup data base for exploraton
    """
    # get access url
    # api_url = env.get_db_access("logs")
    cohorts_url = env.get_db_access("curriculum_logs")

    # read api_access data
    # codeup_api = pd.read_sql('SELECT * FROM api_access', api_url)
    codeup_cohorts = pd.read_sql('SELECT * FROM cohorts', cohorts_url)
    codeup_logs = pd.read_sql('SELECT * FROM logs', cohorts_url)
    
    # merge the cohorts data with the logs data
    codeup = codeup_cohorts.merge(codeup_logs, left_on="id", right_on="cohort_id", how="right")
    return codeup