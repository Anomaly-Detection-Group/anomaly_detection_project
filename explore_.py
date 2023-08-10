import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import env


def get_explore_question_3():
    # Query the databse to retireve the data log and cohorts and joined them
    url = env.get_db_access('curriculum_logs')
    query = '''
    SELECT * 
    FROM logs
    JOIN cohorts as c ON c.id=cohort_id;
    '''
    active_students = pd.read_sql(query, url)


    # Changing the date to datetime
    active_students.date = pd.to_datetime(active_students.date)
    active_students = active_students.set_index(active_students.date)
    active_students.start_date = pd.to_datetime(active_students.start_date)
    active_students.end_date = pd.to_datetime(active_students.end_date)
    active_students.created_at = pd.to_datetime(active_students.created_at)
    active_students.updated_at = pd.to_datetime(active_students.updated_at)

    # Removing the points after the end date for the cohort
    active_students = active_students[active_students['date']<active_students['end_date']]

    # Low activity based on the date
    low_activity = active_students.groupby('user_id')[['date', 'path']].nunique()\
    .sort_values(by='path', ascending=True)
    
    # Creating the list of low activity students
    low_act_students = low_activity.index.to_list()
    
    # DataFrame with only the low actitvity students
    low_active_df = active_students[active_students['user_id'].isin(low_act_students)]

    # get user activity
    last_active_day = low_active_df.groupby('user_id')['date', 'end_date'].max()
    last_active_day['days_apart_from_end_date'] = last_active_day.end_date-last_active_day.date
    last_active_day = last_active_day.sort_values(by='days_apart_from_end_date', ascending=False)
    
    # get students and last day accesed site
    days_from_end_df = pd.DataFrame(last_active_day.days_apart_from_end_date.value_counts(normalize=True).sort_values(ascending=False))
    days_from_end_df['user_count'] = last_active_day.days_apart_from_end_date.value_counts().sort_values(ascending=False)
    
    # get anomaly users
    one_day_list = low_activity[low_activity['date']==1]
    return one_day_list, days_from_end_df