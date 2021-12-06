import streamlit as st 
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

data_url = 'https://raw.githubusercontent.com/ZhouyaoXie/age-vis/main/data/data_n.csv'
disease_lst = ['Diabetes', 'Heart_Attack', 'Thyroid', 'Asthma', 'Kidney_Stones', 'Hepatitis']

title = 'Age & Diseases'

intro_text ="""
In the previous page, we analysed how various attributes correlate with disease (Marraige with thyroid, 
weight with diabetes, length of stay in the USA with the prevalence af asthma). While we had observed some 
correaltions, we are more interestd in understand the causality or other confounding factors. In general, the 
probability of getting diagnosed with a disease increses through age. 

The chronological age (number of years since birth) is ccorrelated linearly with
- Marital status : On an average, unmarried people would be of lesser age compared to the couple that is either 
married or divorced)
- Length of stay in US : This is an obvious correlation. The higher someone stays in a country the higher their 
age would be

This excercise is to understand how age affects the probabiltiy of getting diagnosed with various diseases, including 
Diabetes, Heart attack, Thyroid, Asthma, Kidney problems, and Hepatitis. 
We can see that except for Asthma, all other diseases have increased prevalance in elderly people. 
Our understanding is that Asthma, if present, is often screened at a very early age (before 10 years), and hence we 
see a bulge only in the lower part of the violin plot for Asthma.
"""

disease_analysis = {
    'Diabetes': 'some analysis goes here'
}

@st.cache
def load_data():
    """
    Load the aggregate dataframe as well as processing dataframes for plotting.

    """
    data_n = pd.read_csv(data_url)
    dd_age_thyroid = load_age_thyroid_data(data_n)
    dd_age_diabetes = load_age_diabetes_data(data_n)
    dd_age_heartAttack = load_age_heartattack_data(data_n)
    dd_age_asthma = load_age_asthma_data(data_n)
    dd_age_kidney = load_age_kidney_data(data_n)
    dd_age_hepatitis = load_age_hepatitis_data(data_n)

    dd_dist_heartAttack = load_dist_heartattack(data_n)
    dd_dist_thyroid = load_dist_thyroid_data(data_n)
    dd_dist_asthma = load_dist_asthma_data(data_n)

    plots_violin = {
        "Diabetes": dd_age_diabetes[dd_age_diabetes["DIQ010"]==1].rename(columns = {"RIDAGEYR": "Diabetes"}), 
        "Heart_Attack" : dd_age_heartAttack[dd_age_heartAttack["MCQ160E"]==1].rename(columns = {"MCD180E": "Heart_Attack"}),
        "Thyroid" : dd_age_thyroid[dd_age_thyroid["MCQ160M"]==1].rename(columns = {"MCD180M": "Thyroid"}),
        "Asthma" : dd_age_asthma[dd_age_asthma["MCQ010"]==1].rename(columns = {"MCQ025": "Asthma"}),
        "Kidney_Stones" : dd_age_kidney[dd_age_kidney["KIQ026"]==1].rename(columns = {"RIDAGEYR": "Kidney_Stones"}),
        "Hepatitis" : dd_age_hepatitis[dd_age_hepatitis["HEQ010"]==1].rename(columns = {"RIDAGEYR": "Hepatitis"})
        }

    plots_dist = {
            "Hepatitis":dd_age_hepatitis.rename(columns={'HEQ010':'Hepatitis'}).replace({1: 'Yes', 2: 'No'}),
            "Kidney_Stones":dd_age_kidney.rename(columns={"KIQ026":"Kidney_Stones"}).replace({1: 'Yes', 2: 'No'}),
            "Diabetes":dd_age_diabetes.rename(columns={"DIQ010":"Diabetes"}).replace({1: 'Yes', 2: 'No',3:'Boderline'}),
            "Heart_Attack":dd_dist_heartAttack.rename(columns={"MCQ160E":"Heart_Attack"}).replace({1: 'Yes', 2: 'No'}),
            "Asthma":dd_dist_asthma.rename(columns={"MCQ010":"Asthma"}).replace({1: 'Yes', 2: 'No'}),
            "Thyroid":dd_dist_thyroid.rename(columns={"MCQ160M":"Thyroid"}).replace({1: 'Yes', 2: 'No'}),
        }
    return data_n, plots_violin, plots_dist

def load_age_thyroid_data(data_n):
    dd_age_thyroid = data_n[["SEQN","RIDAGEYR","MCQ160M","MCD180M"]]
    #remove missing entries and the datapoints where the users have refused to provide the marraige information
    dd_age_thyroid = dd_age_thyroid[~dd_age_thyroid["RIDAGEYR"].isin([])]
    #remove missing entries the datapoitns where the users have refused to provide the thyroid information
    dd_age_thyroid = dd_age_thyroid[~dd_age_thyroid["MCD180M"].isin([77777,99999])]
    #remove rows with any NA
    dd_age_thyroid = dd_age_thyroid.dropna()

    return dd_age_thyroid

def load_dist_thyroid_data(data_n):
    dd_dist_thyroid = data_n[["SEQN","RIDAGEYR","MCQ160M"]]
    #remove missing entries and the datapoints where the users have refused to provide the marraige information
    dd_dist_thyroid = dd_dist_thyroid[~dd_dist_thyroid["RIDAGEYR"].isin([])]
    dd_dist_thyroid = dd_dist_thyroid[dd_dist_thyroid["MCQ160M"].isin([1.0,2.0])]
    #remove missing entries the datapoitns where the users have refused to provide the thyroid information
    # dd_age_thyroid = dd_age_thyroid[~dd_age_thyroid["MCD180M"].isin([77777,99999])]
    #remove rows with any NA
    dd_dist_thyroid = dd_dist_thyroid.dropna()

    return dd_dist_thyroid

def load_age_diabetes_data(data_n):
    dd_age_diabetes = data_n[["SEQN","RIDAGEYR","DIQ010"]]
    #remove missing entries and the datapoints where the users have refused to provide the marraige information
    dd_age_diabetes = dd_age_diabetes[~dd_age_diabetes["RIDAGEYR"].isin([])]
    #remove missing entries the datapoitns where the users have refused to provide the diabetes information
    dd_age_diabetes = dd_age_diabetes[~dd_age_diabetes["DIQ010"].isin([7,9])]
    #remove rows with any NA
    dd_age_diabetes = dd_age_diabetes.dropna()

    return dd_age_diabetes

def load_age_heartattack_data(data_n):
    dd_age_heartAttack = data_n[["SEQN","RIDAGEYR","MCQ160E","MCD180E"]]
    #remove missing entries and the datapoints where the users have refused to provide the marraige information
    dd_age_heartAttack = dd_age_heartAttack[~dd_age_heartAttack["MCQ160E"].isin([])]
    #remove missing entries the datapoitns where the users have refused to provide the heartAttack information
    dd_age_heartAttack = dd_age_heartAttack[~dd_age_heartAttack["MCD180E"].isin([77777,99999])]
    #remove rows with any NA
    dd_age_heartAttack = dd_age_heartAttack.dropna()

    return dd_age_heartAttack

def load_dist_heartattack(data_n):
    dd_dist_heartAttack = data_n[["SEQN","RIDAGEYR","MCQ160E"]]
    #remove missing entries and the datapoints where the users have refused to provide the marraige information
    dd_dist_heartAttack = dd_dist_heartAttack[dd_dist_heartAttack["MCQ160E"].isin([1.0,2.0])]
    #remove missing entries the datapoitns where the users have refused to provide the heartAttack information
    # dd_age_heartAttack = dd_age_heartAttack[~dd_age_heartAttack["MCD180E"].isin([77777,99999])]
    #remove rows with any NA
    dd_dist_heartAttack = dd_dist_heartAttack.dropna()

    return dd_dist_heartAttack

def load_age_asthma_data(data_n):
    dd_age_asthma = data_n[["SEQN","RIDAGEYR","MCQ010","MCQ025"]]
    #remove missing entries and the datapoints where the users have refused to provide the marraige information
    dd_age_asthma = dd_age_asthma[~dd_age_asthma["MCQ010"].isin([])]
    #remove missing entries the datapoitns where the users have refused to provide the asthma information
    dd_age_asthma = dd_age_asthma[~dd_age_asthma["MCQ025"].isin([77777,99999])]
    #remove rows with any NA
    dd_age_asthma = dd_age_asthma.dropna()

    return dd_age_asthma

def load_dist_asthma_data(data_n):
    dd_dist_asthma = data_n[["SEQN","RIDAGEYR","MCQ010"]]
    #remove missing entries and the datapoints where the users have refused to provide the marraige information
    dd_dist_asthma = dd_dist_asthma[dd_dist_asthma["MCQ010"].isin([1.0,2.0])]
    #remove missing entries the datapoitns where the users have refused to provide the asthma information
    # dd_age_asthma = dd_age_asthma[~dd_age_asthma["MCQ025"].isin([77777,99999])]
    #remove rows with any NA
    dd_dist_asthma = dd_dist_asthma.dropna()

    return dd_dist_asthma

def load_age_kidney_data(data_n):
    dd_age_kidney = data_n[['SEQN','RIDAGEYR','KIQ026']]
    dd_age_kidney = dd_age_kidney[dd_age_kidney['KIQ026'].isin([1,2])]
    dd_age_kidney = dd_age_kidney.dropna()
    dd_age_kidney[dd_age_kidney['KIQ026']==1]['RIDAGEYR']

    return dd_age_kidney

def load_age_hepatitis_data(data_n):
    dd_age_hepatitis = data_n[['SEQN','RIDAGEYR','HEQ010']]
    dd_age_hepatitis = dd_age_hepatitis[dd_age_hepatitis['HEQ010'].isin([1,2])]
    dd_age_hepatitis = dd_age_hepatitis.dropna()
    dd_age_hepatitis[dd_age_hepatitis['HEQ010']==1]['RIDAGEYR']

    return dd_age_hepatitis

def plot_violin(plots, disease = 'Diabetes'):
    fig, ax = plt.subplots(1,1, figsize = (5,9))
    sns.violinplot(data = plots[disease], y = disease, ax=ax)
    ax.set_xlabel('distribution')
    return fig

def plot_dist(plots, disease = 'Diabetes'):
    fig, ax = plt.subplots(1,1, figsize = (5,9))
    sns.histplot(data = plots[disease], x = disease, ax=ax)
    return fig

def app():

    st.title(title)
    data_load_state = st.markdown('*Loading data... \
        If this is the first time you are launching this app, this is going to take a few seconds.*')
    data_n, violin_plots, dist_plots = load_data()
    data_load_state.markdown('*Loading graphics...*')
    data_load_state.markdown(intro_text)

    col1, col2 = st.columns(2)

    # select disease
    select = st.selectbox('Select a disease to explore:', disease_lst)
    select = 'Diabetes' if not select else select

    # plot left panel
    col1.markdown('#### Age distribution of ' + select)
    col1.pyplot(plot_violin(violin_plots, select))

    # plot right panel
    col2.markdown('#### Frequency Distribution of ' + select)
    col2.pyplot(plot_dist(dist_plots, select))

    st.markdown(disease_analysis.get(select, ' '))