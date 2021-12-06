import page0
import page1
import page2
import page3
import page4
import streamlit as st

PAGES = {
    "Intro & Dataset": page0,
    "Age & Diseases": page1,
    "Interesting Findings": page2,
    "Biomarkers & Age": page3,
    "Predicting Biological Age": page4
}
st.set_page_config(layout="wide")
st.sidebar.markdown('# Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
st.sidebar.markdown("# About")
st.sidebar.markdown("Authors: Nikhil Yadala, Manoj Ghuhan, Zhouyao Xie")
st.sidebar.markdown("CMU 05839 interactive Data Science")
st.sidebar.markdown("Instructor: John Stamper")
page.app()