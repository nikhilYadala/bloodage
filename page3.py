import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_url = 'https://raw.githubusercontent.com/ZhouyaoXie/age-vis/main/data/data_n.csv'
biomarker_lst = ['LBXSCR', 'LBXSAPSI', 'LBXSASSI', 'LBXSGL', 'LBDSTBSI', 'LBDSCHSI', 'LBXSTR']

title = 'Biomarkers & Age'

intro_text ="""
some intro goes here

"""

disease_analysis = {
    'Diabetes': 'some analysis goes here'
}


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
    return data_n

def plot_joint(data_n, biomarker = 'LBXSCR'):
	# fig = plt.figure(figsize = (5,9))
	df_creatinine=data_n[['RIDAGEYR',biomarker]]
	fig = sns.jointplot(x=df_creatinine["RIDAGEYR"], y=df_creatinine[biomarker], kind='hex', 
		marginal_kws=dict(bins=30, fill=True))
	st.pyplot(fig)

def app():
    st.title(title)
    st.markdown('----')
    data_load_state = st.markdown('*Loading data... \
        If this is the first time you are launching this app, this is going to take a few seconds.*')
    data_n = load_data()
    data_load_state.markdown('*Loading graphics...*')
    data_load_state.markdown(intro_text)
    
    # select biomarker
    select = st.selectbox('Select a biomarker to explore:', biomarker_lst)
    select = 'LBXSCR' if not select else select

    st.markdown('#### Correlation Between Age and ' + select)
    plot_joint(data_n, biomarker = select)

    st.markdown(disease_analysis.get(select, ' '))



