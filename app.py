import page0
import page1
import page2
import page3
import page4
import streamlit as st
import requests

PAGES = {
    "Intro & Dataset": page0,
    "Exploratory Data Analysis": page1,
    "Age & Diseases": page2,
    "Biomarkers & Age": page3,
    "Predicting Biological Age": page4
}

video_url = ''

st.set_page_config(layout="wide")
# center image with style.css
f = requests.get('https://raw.githubusercontent.com/ZhouyaoXie/age-vis/main/style.css').content
st.markdown('<style>{}</style>'.format(f), unsafe_allow_html=True)

# page selection
st.sidebar.markdown('# Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

# about info
st.sidebar.markdown("# About")
st.sidebar.markdown("**@brief** Final Project for CMU 05839 interactive Data Science")
st.sidebar.markdown("**@Github** [Our code](https://github.com/ZhouyaoXie/age-vis)")
st.sidebar.markdown("""**@video **: [presentation](""" + video_url+')')
st.sidebar.markdown("""**@authors**:  \nNikhil Yadala | Manoj Ghuhan | Zhouyao Xie""")

page.app()