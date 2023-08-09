import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import wrangle_victoire_
import env

import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

# explore function
def get_explore_question_1():
    # load cleaned data
    codeup = wrangle_victoire_.wrangle_codeup()
    
    # drop nulls in the path column
    codeup = codeup[~codeup.path.isna()]
    # remove bad urls from path
    codeup = codeup[~codeup.path.isin(["/"])]
    
    # create a lesson column
    codeup["lesson"] = codeup.path.str.extract('^(.*?)(?=\/)')
    
    # group the dataframe
    lesson_counts = codeup.groupby(["program_id","cohort_id","lesson"]).date.agg(["count"]).sort_values(by=["program_id"], ascending=False)

    # Reset the index and create columns for group keys
    lesson_counts = lesson_counts.reset_index()
    
    # find name of highly visited lesson
    lesson_counts = lesson_counts.groupby(["program_id","cohort_id"])["lesson","count"].max()
    return lesson_counts


# explore function
def get_explore_question_2():
    # get engineered data
    lesson_counts = get_explore_question_1()
    
    # which cohort visited web-design
    web_design = lesson_counts[lesson_counts.lesson == "web-design"]
    
    # reset dataframe index
    web_design = web_design.reset_index()
    
    # get min and max cohort counts
    min_max_counts = web_design[(web_design["count"] == web_design["count"].max()) | (web_design["count"] == web_design["count"].min())]

    return min_max_counts