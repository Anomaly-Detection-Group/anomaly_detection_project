import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import wrangle_
import env

import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

# explore function
def get_explore_question_1():
    """
    Goal: Do all work needed and return results for question 1
    """
    # load cleaned data
    codeup = wrangle_.wrangle_codeup()

    # drop nulls in the path column
    codeup = codeup[~codeup.path.isna()]
    # remove bad urls from path
    codeup = codeup[~codeup.path.isin(["/"])]

    # create a lesson column
    codeup["lesson"] = codeup.path.str.extract('^(.*?)(?=\/)')
    
    # Group by program_id, cohort_id, and lesson, then count the occurrences of each lesson
    lesson_counts = codeup.groupby(["program_id","cohort_id", "lesson"])["lesson"].count().reset_index(name="referred_to_lesson_count")

    # Find the top ten lesson counts in each cohort_id within each program_id
    lesson_counts = lesson_counts.sort_values(by=["program_id","cohort_id", "referred_to_lesson_count"], ascending=[True,True,False]).groupby(["cohort_id"]).head(1)
    return lesson_counts


# explore function
def get_explore_question_2():
    """
    Goal: Do all work needed and return results for question 2
    """
    # load cleaned data
    codeup = wrangle_.wrangle_codeup()

    # drop nulls in the path column
    codeup = codeup[~codeup.path.isna()]
    # remove bad urls from path
    codeup = codeup[~codeup.path.isin(["/"])]

    # create a lesson column
    codeup["lesson"] = codeup.path.str.extract('^(.*?)(?=\/)')

    # Group by program_id, cohort_id, and lesson, then count the occurrences of each lesson
    lesson_counts = codeup.groupby(["cohort_id", "lesson"])["lesson"].count().reset_index(name="referred_to_lesson_count")
    
    # Find the top ten lesson counts in each cohort_id within each program_id
    top_5_in_cohort = lesson_counts.sort_values(by=["cohort_id", "referred_to_lesson_count"], ascending=[True,False]).groupby(["cohort_id"]).head(5)

    # look at one lesson to compare top results
    plt.figure(figsize=(12,3))
    results = top_5_in_cohort[top_5_in_cohort.lesson == "javascript-i"][["cohort_id","referred_to_lesson_count"]].sort_values(by="cohort_id").set_index("cohort_id")
    sns.barplot(x=results.index, y=results.referred_to_lesson_count)
    plt.xticks(rotation=90)
    plt.title("cohort reference to javascript-1 count")
    plt.xlabel("cohort id")
    plt.ylabel("referred javascript-i count")

    return plt.gcf()

def get_explore_question_3():
    """
    Goal: Do all work needed and return results for question 3
    """
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

def get_explore_question_4():
    """
    Goal: Do all work needed and return results for question 4
    """
    