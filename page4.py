import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

title = "Predicting Biological Age"

intro_text = """
**Train your own age prediction model using gradient boosting decision tree (GBDT) and evalute its performance!**
"""

def app():
	st.title(title)
	st.markdown(intro_text)
	col2, col1 = st.columns(2)
	col1.slider("Number of Trees:", min_value = 10, max_value = 2000, value = 1000, 
		help = "The number of decision trees used in the model. \
			A larger value typically decreases training error but will take longer to train and might cause overfittng.")
	col1.slider("Depth of Trees:", min_value = 2, max_value = 10, value = 6, 
		help = "The maximum depth of individual decision trees.\
		 The maximum depth limits the number of nodes in the tree.")
	col1.select_slider("Learning rate:", options = [0.001, 0.01, 0.02, 0.05, 0.1], value = 0.01, 
		help = "Learning rate. This shrinks the contribution of each tree by the specified amount.")
	col1.slider("Min Splits:", min_value = 10, max_value = 50, value = 30, 
		help = "The minimum number of samples required to split an internal node of a tree.")
	
	col2.markdown("Select sets of features to include in training:")
	col2.checkbox("Demographics features:", value = True)
	col2.checkbox("Diseases features:", value = True)
	col2.checkbox("Biochemistry features:", value = True)
