import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_url = 'https://raw.githubusercontent.com/ZhouyaoXie/age-vis/main/data/data_n.csv'

title = 'Biomarkers & Age'

intro_text ="""
In this section, we investigate the correlation between age and various types of essential biomarkers.\
The x-axis shows the distribution of age, while the y-axis shows the distribution of the values of \
the selected marker. You can play with different markers and see how the visualization changes.
"""

marker_dict = {
    'LBXSTR':'Triglycerides',
    'LBXSCR':'Creatinine',
    'LBXSAPSI':'Alkaline Phosphatase',
    'LBXSASSI':'Aspartate Aminotransferase',
    'LBXSGL':'Glucose',
    'LBXSTB':'Total Bilirubin',
    'LBXSCH':'Cholesterol'
}


@st.cache
def load_data():
    """
    Load the aggregate dataframe as well as processing dataframes for plotting.

    """
    data_n = pd.read_csv(data_url)
    df_creatinine=data_n[['RIDAGEYR','LBXSCR']]
    df_creatinine=df_creatinine[df_creatinine['LBXSCR']<=2]
    df_phosphatase=data_n[['RIDAGEYR','LBXSAPSI']]
    # sns.histplot(df_phosphatase['LBXSAPSI'])
    df_phosphatase=df_phosphatase[df_phosphatase['LBXSAPSI']<=200]
    # sns.jointplot(x=df_phosphatase["RIDAGEYR"], y=df_phosphatase["LBXSAPSI"], kind='hex', marginal_kws=dict(bins=30, fill=True))
    df_aspartate=data_n[['RIDAGEYR','LBXSASSI']]
    # sns.histplot(df_aspartate['LBXSASSI'])
    df_aspartate=df_aspartate[df_aspartate['LBXSASSI']<=50]
    # sns.jointplot(x=df_aspartate["RIDAGEYR"], y=df_aspartate["LBXSASSI"], kind='hex', marginal_kws=dict(bins=30, fill=True))
    df_glucose=data_n[['RIDAGEYR','LBXSGL']]
    # sns.histplot(df_glucose['LBXSGL'])
    df_glucose=df_glucose[df_glucose['LBXSGL']<=180]
    df_glucose=df_glucose[df_glucose['LBXSGL']>=60]
    # sns.jointplot(x=df_glucose["RIDAGEYR"], y=df_glucose["LBXSGL"], kind='hex', marginal_kws=dict(bins=30, fill=True))
    df_bilirubin=data_n[['RIDAGEYR','LBXSTB']]
    # sns.histplot(df_bilirubin['LBXSTB'])
    df_bilirubin=df_bilirubin[df_bilirubin['LBXSTB']<=1.55]
    # sns.jointplot(x=df_bilirubin["RIDAGEYR"], y=df_bilirubin["LBXSTB"], kind='hex', marginal_kws=dict(bins=20, fill=True))
    df_cholestrol=data_n[['RIDAGEYR','LBXSCH']]
    # sns.histplot(df_cholestrol['LBXSCH'])
    df_cholestrol=df_cholestrol[df_cholestrol['LBXSCH']<=350]
    # sns.jointplot(x=df_cholestrol["RIDAGEYR"], y=df_cholestrol["LBXSCH"], kind='hex', marginal_kws=dict(bins=30, fill=True))
    df_triglycerides=data_n[['RIDAGEYR','LBXSTR']]
    # sns.histplot(df_cholestrol['LBXSTR'])
    df_triglycerides=df_triglycerides[df_triglycerides['LBXSTR']<=400]
    # sns.jointplot(x=df_triglycerides["RIDAGEYR"], y=df_triglycerides["LBXSTR"], kind='hex', marginal_kws=dict(bins=30, fill=True))
    marker_plots = {
        'Triglycerides':df_triglycerides.rename(columns={'LBXSTR':'Triglycerides','RIDAGEYR':'Age'}),
        'Creatinine':df_creatinine.rename(columns={'LBXSCR':'Creatinine','RIDAGEYR':'Age'}),
        'Alkaline Phosphatase':df_phosphatase.rename(columns={'LBXSAPSI':'Alkaline Phosphatase','RIDAGEYR':'Age'}),
        'Aspartate Aminotransferase':df_aspartate.rename(columns={'LBXSASSI':'Aspartate Aminotransferase','RIDAGEYR':'Age'}),
        'Glucose':df_glucose.rename(columns={'LBXSGL':'Glucose','RIDAGEYR':'Age'}),
        'Total Bilirubin':df_bilirubin.rename(columns={'LBXSTB':'Total Bilirubin','RIDAGEYR':'Age'}),
        'Cholesterol':df_cholestrol.rename(columns={'LBXSCH':'Cholesterol','RIDAGEYR':'Age'}),
        }
    return data_n, marker_plots

def plot_joint(marker_plots, biomarker):
    df = marker_plots[biomarker]
    fig = sns.jointplot(x=df['Age'], y=df[biomarker], kind='hex', marginal_kws=dict(bins=30, fill=True))
    st.pyplot(fig)

def app():
    st.title(title)
    st.markdown('----')
    data_load_state = st.markdown('*Loading data... \
        If this is the first time you are launching this app, this is going to take a few seconds.*')
    data_n, marker_plots = load_data()
    data_load_state.markdown('*Loading graphics...*')
    data_load_state.markdown(intro_text)
    
    # select biomarker
    select = st.selectbox('Select a biomarker to explore:', list(marker_dict.values()))
    select = 'Creatinine' if not select else select

    st.markdown('#### Correlation Between Age and ' + select)
    plot_joint(marker_plots, biomarker = select)



