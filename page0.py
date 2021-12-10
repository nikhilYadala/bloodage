import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import requests
from io import BytesIO

title = "Motivation"
img_url = "https://github.com/ZhouyaoXie/age-vis/blob/main/img/page0-eda.png?raw=true"
data_url = 'https://raw.githubusercontent.com/ZhouyaoXie/age-vis/main/data/data_n.csv'

intro_text = """
---
Today, we know of several [hallmarks of aging] (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3836174/) : 
Genomic instability, Telomere attrition, Epigenetic alterations, Loss of proteostasis, Deregulated Nutrient sensing, 
Mitochondrial dysfunction, cellular senescence, stem cell exhaustion..!

Drugs like [Rapamycin (mTOR inhibitor)](https://link.springer.com/article/10.1007/s11357-020-00274-1), 
[metformin (the diabetes drug)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3736576/),
 [Resveratrol](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2546476/), 
 etc have been proven to increase the lifespan (time to death) as well as healthspan
  (QALY - Quality adjusted life years) in mice as well as other preclinical studies. 
  To test the efficacy of these drugs in humans, we need to do Randomized controlled trials (RCT). 
  But the only gold standard measure we have (for the endpoint of an RCT) is max life expectancy. 
  This would mean that the RCT has to be conducted over a span of several decades (until most of the 
  cohort reaches their natural age of death) and establish whether or not the drug had an effect on aging. 
  Moreover, human behaviour and body is much more complex than the animals in a predefined laboratory setting.
   Hence, it is difficult to decouple the effect of confounding drugs/habits/cognitive behavior on the effect of aging.
    All of this makes it harder to come up with drugs that target these pathways of aging in humans.
     These problems could be solved, if we have biomarkers of aging!

Our goal is to develop a model to predit the biological age ( a representation of the actual health status of an 
individual), and understand, present how various parameters and factors affect the biological age (and hence the 
diseases assocciated with age).

"""

dataset_text = """

# Dataset Overview
---
The [National Health and Nutrition Examination Survey (NHANES)](https://www.cdc.gov/nchs/nhanes/about_nhanes.htm) is
 a program of studies designed to assess the health and nutritional status of adults and children in the United States. 
 Data are collected every year using a combination of interviews and physical exams. The NHANES interview includes 
 demographic, socioeconomic, dietary, and health-related questions. The examination component consists of medical, 
 dental, and physiological measurements, as well as laboratory tests administered by highly trained medical personnel.

Because of the pandemic, data collection for the 2019-2020 cycle was cancelled. As of March 2020, data collection was
 completed in 18 of 30 locations or primary sampling units ([PSUs] usually a county or a group of counties) in the 
 2019-2020 sample. These incomplete data were combined with the full data set from the previous cycle (2017-2018) to
  create a nationally representative dataset, 
  [2017-March 2020 pre-pandemic data](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020). 
  It is this dataset that we have chosen to perform our analysis on.

"""

eda_caption = """

The barplots above show the distributions of a subset of the categorical variables that we 
looked at. We have a relatively balanced gender distribution in the data, 
with the majority of people interviewed were born in the US. Also, we have more people who 
are married than single or widowed/divorced in the dataset. Regarding race/ethnicity, 
non-hispanic White is the largest group, followed by non-hispanic Black, Mexican American, 
non-hispanic Asian, and others. For diseases such as thyroid problems and heart attacks, 
 it is not surprising to see that the majority of the interviewee answered "no" to the question 
 "have you ever been told that you have had the disease".

 For a detailed description of each field, please check the documentation on
  [NHANES website](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2017-2020).

"""

def open_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

@st.cache
def load_data():
    """
    Load the aggregate dataframe as well as processing dataframes for plotting.

    """
    data_n = pd.read_csv(data_url, index_col = False)
    return data_n

def app():
    st.title(title)
    st.markdown(intro_text)
    st.markdown(dataset_text)
    img1 = open_image(img_url)
    st.image(img1, caption='', width = 800)
    st.markdown(eda_caption)
    st.markdown('------')

    with st.expander("Click here to download our aggregate data:"):
        data_n = load_data()
        st.download_button('Download our data', data_n.to_csv(), file_name = 'nhanes_data.csv')