import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import wrangle_victoire_
import env

import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

# load cleaned data
codeup = wrangle_victoire_.wrangle_codeup()

# drop nulls in the path column
codeup = codeup[~codeup.path.isna()]
# remove bad urls from path
codeup = codeup[~codeup.path.isin(["/"])]

# create a lesson column
codeup["lesson"] = codeup.path.str.extract('^(.*?)(?=\/)')

# explore function
def get_explore_question_1():
    
    # Group by program_id, cohort_id, and lesson, then count the occurrences of each lesson
    lesson_counts = codeup.groupby(["program_id","cohort_id", "lesson"])["lesson"].count().reset_index(name="referred_to_lesson_count")

    # Find the top ten lesson counts in each cohort_id within each program_id
    lesson_counts = lesson_counts.sort_values(by=["program_id","cohort_id", "referred_to_lesson_count"], ascending=[True,True,False]).groupby(["cohort_id"]).head(1)
    return lesson_counts


# explore function
def get_explore_question_2():
    # Group by program_id, cohort_id, and lesson, then count the occurrences of each lesson
    lesson_counts = codeup.groupby(["cohort_id", "lesson"])["lesson"].count().reset_index(name="referred_to_lesson_count")
    
    # Find the top ten lesson counts in each cohort_id within each program_id
    top_5_in_cohort = lesson_counts.sort_values(by=["cohort_id", "referred_to_lesson_count"], ascending=[True,False]).groupby(["cohort_id"]).head(5)

    # look at one lesson to compare top results
    plt.figure(figsize=(10,3))
    top_5_in_cohort[top_5_in_cohort.lesson == "javascript-i"].referred_to_lesson_count.sort_values(ascending=False).plot(kind="bar")
    plt.title("cohort reference to javascript-1 count")
    plt.xlabel("cohort id")
    plt.ylabel("referred javascript-i count")

    return plt.gcf()