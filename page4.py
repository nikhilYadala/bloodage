import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

title = "Predicting Biological Age"

intro_text = """
---
**Train your own age prediction model using gradient boosting decision tree (GBDT) and evalute its performance!**
"""

demo_lst = ['RIAGENDR - Gender',
       'RIDRETH1 - Race/Hispanic origin',
       'RIDRETH3 - Race/Hispanic origin w/ NH Asian',
       'RIDEXMON - Six-month time period', 'DMDBORN4 - Country of birth',
       'DMDEDUC2 - Education level - Adults 20+',
       'DMDMARTZ - Marital status', 'RIDEXPRG - Pregnancy status at exam',
       'SIALANG - Language of SP Interview',
       'SIAPROXY - Proxy used in SP Interview?',
       'SIAINTRP - Interpreter used in SP Interview?',
       'FIALANG - Language of Family Interview',
       'FIAPROXY - Proxy used in Family Interview?',
       'FIAINTRP - Interpreter used in Family Interview?',
       'MIALANG - Language of MEC Interview',
       'MIAPROXY - Proxy used in MEC Interview?',
       'MIAINTRP - Interpreter used in MEC Interview?',
       'AIALANGA - Language of ACASI Interview',
       'WTINTPRP - Full sample interview weight',
       'WTMECPRP - Full sample MEC exam weight',
       'SDMVPSU - Masked variance pseudo-PSU',
       'SDMVSTRA - Masked variance pseudo-stratum',
       'INDFMPIR - Ratio of family income to poverty']

disease_lst = ['MCQ010 - Ever been told you have asthma',
       'MCQ025 - Age when first had asthma', 'MCQ035 - Still have asthma',
       'MCQ040 - Had asthma attack in past year',
       'MCQ050 - Emergency care visit for asthma/past yr',
       'AGQ030 - Did SP have episode of hay fever/past yr',
       'MCQ053 - Taking treatment for anemia/past 3 mos',
       'MCQ080 - Doctor ever said you were overweight',
       'MCQ092 - Ever receive blood transfusion',
       'MCD093 - Year receive blood transfusion', 'MCQ145 - CHECK ITEM',
       'MCQ149 - Menstrual periods started yet?',
       'MCQ151 - Age in years at first menstrual period',
       'RHD018 - Estimated age in months at menarche',
       'MCQ160a - Doctor ever said you had arthritis',
       'MCQ195 - Which type of arthritis was it?',
       'MCQ160b - Ever told had congestive heart failure',
       'MCD180b - Age when told you had heart failure',
       'MCQ160c - Ever told you had coronary heart disease',
       'MCD180c - Age when told had coronary heart disease',
       'MCQ160d - Ever told you had angina/angina pectoris',
       'MCD180d - Age when told you had angina pectoris',
       'MCQ160e - Ever told you had heart attack',
       'MCD180e - Age when told you had heart attack',
       'MCQ160f - Ever told you had a stroke',
       'MCD180F - Age when told you had a stroke',
       'MCQ160m - Ever told you had thyroid problem',
       'MCQ170m - Do you still have thyroid problem',
       'MCD180M - Age when told you had thyroid problem',
       'MCQ160p - Ever told you had COPD, emphysema, ChB',
       'MCQ160l - Ever told you had any liver condition',
       'MCQ170l - Do you still have a liver condition',
       'MCD180l - Age when told you had a liver condition',
       'MCQ500 - Ever told you had any liver condition',
       'MCQ510a - Liver condition: Fatty liver',
       'MCQ510b - Liver condition: Liver fibrosis',
       'MCQ510c - Liver condition: Liver cirrhosis',
       'MCQ510d - Liver condition: Viral hepatitis',
       'MCQ510e - Liver condition: Autoimmune hepatitis',
       'MCQ510f - Liver condition: Other liver disease',
       'MCQ515 - CHECK ITEM',
       'MCQ520 - Abdominal pain during past 12 months?',
       'MCQ530 - Where was the most uncomfortable pain',
       'MCQ540 - Ever seen a DR about this pain',
       'MCQ550 - Has DR ever said you have gallstones',
       'MCQ560 - Ever had gallbladder surgery?',
       'MCQ570 - Age when 1st had gallbladder surgery?',
       'MCQ220 - Ever told you had cancer or malignancy',
       'MCQ230a - 1st cancer - what kind was it?',
       'MCQ230b - 2nd cancer - what kind was it?',
       'MCQ230c - 3rd cancer - what kind was it?',
       'MCQ230d - More than 3 kinds of cancer',
       'MCQ300b - Close relative had asthma?',
       'MCQ300c - Close relative had diabetes?',
       'MCQ300a - Close relative had heart attack?',
       'MCQ366a - Doctor told you to control/lose weight',
       'MCQ366b - Doctor told you to exercise',
       'MCQ366c - Doctor told you to reduce salt in diet',
       'MCQ366d - Doctor told you to reduce fat/calories',
       'MCQ371a - Are you now controlling or losing weight',
       'MCQ371b - Are you now increasing exercise',
       'MCQ371c - Are you now reducing salt in diet',
       'MCQ371d - Are you now reducing fat in diet',
       'OSQ230 - Any metal objects inside your body?']

biochem_lst = ['LBXSATSI - Alanine Aminotransferase (ALT) (IU/L)',
       'LBDSATLC - ALT Comment Code',
       'LBXSAL - Albumin, refrigerated serum (g/dL)',
       'LBDSALSI - Albumin, refrigerated serum (g/L)',
       'LBXSAPSI - Alkaline Phosphatase (ALP) (IU/L)',
       'LBXSASSI - Aspartate Aminotransferase (AST) (IU/L)',
       'LBXSC3SI - Bicarbonate (mmol/L)',
       'LBXSBU - Blood Urea Nitrogen (mg/dL)',
       'LBDSBUSI - Blood Urea Nitrogen (mmol/L)',
       'LBXSCLSI - Chloride (mmol/L)',
       'LBXSCK - Creatine Phosphokinase (CPK) (IU/L)',
       'LBXSCR - Creatinine, refrigerated serum (mg/dL)',
       'LBDSCRSI - Creatinine, refrigerated serum (umol/L)',
       'LBXSGB - Globulin (g/dL)', 'LBDSGBSI - Globulin (g/L)',
       'LBXSGL - Glucose, refrigerated serum (mg/dL)',
       'LBDSGLSI - Glucose, refrigerated serum (mmol/L)',
       'LBXSGTSI - Gamma Glutamyl Transferase (GGT) (IU/L)',
       'LBDSGTLC - GGT Comment Code',
       'LBXSIR - Iron, refrigerated serum (ug/dL)',
       'LBDSIRSI - Iron, refrigerated serum (umol/L)',
       'LBXSLDSI - Lactate Dehydrogenase (LDH) (IU/L)',
       'LBXSOSSI - Osmolality (mmol/Kg)', 'LBXSPH - Phosphorus (mg/dL)',
       'LBDSPHSI - Phosphorus (mmol/L)', 'LBXSKSI - Potassium (mmol/L)',
       'LBXSNASI - Sodium (mmol/L)', 'LBXSTB - Total Bilirubin (mg/dL)',
       'LBDSTBSI - Total Bilirubin (umol/L)',
       'LBDSTBLC - Total Bilirubin Comment Code',
       'LBXSCA - Total Calcium (mg/dL)',
       'LBDSCASI - Total Calcium (mmol/L)',
       'LBXSCH - Cholesterol, refrigerated serum (mg/dL)',
       'LBDSCHSI - Cholesterol, refrigerated serum (mmol/L)',
       'LBXSTP - Total Protein (g/dL)', 'LBDSTPSI - Total Protein (g/L)',
       'LBXSTR - Triglycerides, refrig serum (mg/dL)',
       'LBDSTRSI - Triglycerides, refrig serum (mmol/L)',
       'LBXSUA - Uric acid (mg/dL)', 'LBDSUASI - Uric acid (umol/L)']

def train_model():
	return 0

def app():
	st.title(title)
	st.markdown(intro_text)

	with st.form(key = 'hyperparameters'):
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
		
		col2.markdown("Select features to include in training:")
		demo_features = .multiselect("Demographics features:", 
			options = demo_lst, default = demo_lst)
		di_features = col2.multiselect("Diseases features:", options = disease_lst, default = disease_lst)
		bio_features = col2.multiselect("Biochemistry features:", options = biochem_lst, default = biochem_lst)
		selected_features = demo_features + di_features + bio_features

		st.form_submit_button(label = "Train Model!")

	model_training_state = st.markdown("Model training... This might take a few minutes...")
	start = time.time()
	re = train_model()
	end = time.time()
	model_training_state.markdown(' ')
	col1, col2, col3, col4 = st.columns(4)
	col1.metric(label = 'Accuracy', value = 0.974)
	col2.metric(label = 'Training Time', value = str(int(end-start)) + 's')
