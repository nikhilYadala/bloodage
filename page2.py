import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import math
from PIL import Image

title = "Exploratory Analysis"

finding1_title = """
# How does marital status affect thyroid?
"""

finding1_text = """
 In the above visualization, the goal was to explore the factors that affect the diagnosis of thyroid. Thyroid is an autoimmune disease, where stress is one of the signals that can induce systemic changes in the body leading to the diagnosis of the disease. Further stress is manifested from multiple avenues of professional and peresonal lives. We wanted to underestand how the marital status of a person (a persoanl life factor) correlates with thyroid. We observed that the probability of the thyroid is highest among the divorced indivdiuals (due to personal stress?). The probability between Marrird and Unmarried is slightly similar, but higher among the married individiuals.
"""

finding2_title = """

"""

finding2_text = """

"""

finding3_title = """

"""

finding3_text = """

"""

def app():
	st.title(title)

	st.markdown(finding1_title)

	st.markdown(finding1_title)

	st.markdown(finding2_title)

	st.markdown(finding2_text)

	st.markdown(finding3_title)

	st.markdown(finding3_text)
