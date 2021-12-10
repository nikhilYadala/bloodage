import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import requests
from io import BytesIO

title = "Exploratory Data Analysis"
intro = """
Some intro goes here
"""
img_url1 = 'https://github.com/ZhouyaoXie/age-vis/blob/main/img/page2-thyroid-marriage.png?raw=true'
img_url2 = 'https://github.com/ZhouyaoXie/age-vis/blob/main/img/page2-year-asthma.png?raw=true'
img_url3 = 'https://github.com/ZhouyaoXie/age-vis/blob/main/img/page2-weight-diabetes.png?raw=true'

finding1_title = """
## Marital status vs. thyroid
"""
finding1_text = """
 In the above visualization, the goal was to explore the factors that affect the diagnosis of thyroid. Thyroid is an autoimmune disease, where stress is one of the signals that can induce systemic changes in the body leading to the diagnosis of the disease. Further stress is manifested from multiple avenues of professional and peresonal lives. We wanted to underestand how the marital status of a person (a persoanl life factor) correlates with thyroid. We observed that the probability of the thyroid is highest among the divorced indivdiuals (due to personal stress?). The probability between Marrird and Unmarried is slightly similar, but higher among the married individiuals.
"""

finding2_title = """
## Length of stay in USA vs. Asthma
"""
finding2_text = """
In this analysis, we goal was to understand if the length of stay in US changed the probability of getting a disease. We chose Asthma as the disease for our analysis as it is not directly correlated with the age of a person(longer the stay in USA implies higher age). We observed that chance of getting Asthma doesn't vary a lot if the length of stay in USA is <=15 years. However, we observed that with an increase in the duration of stay in US beyond 15 years, the chances of getting Asthma also increases. There can be multiple reasons for this correlation, pollution, temperature, state in USA etc but determine the exact reasons will require availability of richer data.
"""

finding3_title = """
## Weight vs. Diabetes
"""
finding3_text = """
In this Analysis, we try to study the corelation between the weight of a person and the diabetic condition. As expected, we observe that the average weight of person having diabetes is greater than the boderline condition and the weight of the person in boderline condition is greater than non-diabetic condition. This shows the importance of mainting physical fitness for leading a healthier life.
"""

def open_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def app():
    st.title(title)
    st.markdown(intro)
    st.markdown(finding1_title)
    img1 = open_image(img_url1)
    st.image(img1, caption='', width = 600)
    st.markdown(finding1_text)

    st.markdown(finding2_title)
    img2 = open_image(img_url2)
    st.image(img2, caption='', width = 600)
    st.markdown(finding2_text)

    st.markdown(finding3_title)
    img3 = open_image(img_url3)
    st.image(img3, caption='', width = 600)
    st.markdown(finding3_text)
