import page0
import page1
import page2
import page3
import page4
import streamlit as st
import requests

PAGES = {
    "Intro & Dataset": page0,
    "Age & Diseases": page1,
    "More Explorations": page2,
    "Biomarkers & Age": page3,
    "Predicting Biological Age": page4
}

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
st.sidebar.markdown("Final Project for CMU 05839 interactive Data Science")
st.sidebar.markdown("Authors: Nikhil Yadala, Manoj Ghuhan, Zhouyao Xie")
st.sidebar.markdown("Instructor: John Stamper")


page.app()