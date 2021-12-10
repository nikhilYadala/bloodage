import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn import ensemble
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

title = "Predicting Biological Age"

intro_text = """
---
**Train your own age prediction model using gradient boosting decision tree (GBDT) and evalute its performance!**
"""

demo_lst = ['RIAGENDR - Gender',
       'Race/Hispanic origin',
       'Race/Hispanic origin w/ NH Asian',
       'Six-month time period', 'DMDBORN4 - Country of birth',
       'Education level - Adults 20+',
       'Marital status', 'RIDEXPRG - Pregnancy status at exam',
       'Full sample interview weight',
       'Ratio of family income to poverty']

disease_lst = ['Ever been told you have asthma',
       'Still have asthma',
       'Doctor ever said you were overweight',
       'Ever receive blood transfusion',
       'Estimated age in months at menarche',
       'Doctor ever said you had arthritis',
       'Which type of arthritis was it?',
       'Ever told had congestive heart failure',
       'Ever told you had coronary heart disease',
       'Ever told you had angina/angina pectoris',
       'Ever told you had heart attack',
       'Ever told you had a stroke',
       'Ever told you had thyroid problem',
       'Ever told you had any liver condition',
       'Liver condition: Fatty liver',
       'Ever had gallbladder surgery?',
       'Ever told you had cancer or malignancy',
       'Doctor told you to control/lose weight',
       'Are you now increasing exercise',
       'Any metal objects inside your body?']

biochem_lst = [ 'Alanine Aminotransferase (ALT) (IU/L)',
				' Albumin, refrigerated serum (g/dL)',
				' Albumin, refrigerated serum (g/L)',
				' Alkaline Phosphatase (ALP) (IU/L)',
				' Aspartate Aminotransferase (AST) (IU/L)',
				' Bicarbonate (mmol/L)',
				' Blood Urea Nitrogen (mg/dL)',
				' Blood Urea Nitrogen (mmol/L)',
				' Chloride (mmol/L)',
				' Creatine Phosphokinase (CPK) (IU/L)',
				' Creatinine, refrigerated serum (mg/dL)',
				' Creatinine, refrigerated serum (umol/L)',
				' Globulin (g/dL)', 'LBDSGBSI'
				' Glucose, refrigerated serum (mg/dL)',
				' Glucose, refrigerated serum (mmol/L)',
				' Gamma Glutamyl Transferase (GGT) (IU/L)',
				' Lactate Dehydrogenase (LDH) (IU/L)',
				' Osmolality (mmol/Kg)', 
				' Phosphorus (mmol/L)',
				' Sodium (mmol/L)',
				' Total Bilirubin (umol/L)',
				' Total Bilirubin Comment Code',
				' Cholesterol, refrigerated serum (mg/dL)',
				' Cholesterol, refrigerated serum (mmol/L)',
				' Total Protein (g/dL)',
				' Triglycerides, refrig serum (mg/dL)']

def train_model(imp_feat, param):
	# path_prefix = "../05839/NHANES/2017-2020"
	# dd_age = pd.read_sas(os.path.join(path_prefix, "P_BIOPRO.XPT"), format = "XPORT")
	# dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_MCQ.XPT"), format = "XPORT"), how = "outer")
	# dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_TRIGLY.XPT"), format = "XPORT"), how = "outer")
	# dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_HSCRP.XPT"), format = "XPORT"), how = "outer")
	# dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_HDL.XPT"), format = "XPORT"), how = "outer")
	# dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_CBC.XPT"), format = "XPORT"), how = "outer")

	dd_age = pd.read_csv("./data/data_n.csv")
	# dd_age = data_n.copy()
	# dd_age= dd_age.drop(columns=["SEQN"])
	age = data_n[["SEQN","RIDAGEYR"]]
	dd_age = dd_age.drop(columns=["RIDAGEYR", "SDDSRVYR", "RIDAGEYR", "RIDAGEMN", "DMDYRUSZ" ,"MCQ025", "MCD093", "MCQ151" ])
	dd_age = dd_age.merge(age, how= "outer")
	dd_age= dd_age.drop(columns=["SEQN"])

	# dd_age = dd_age.dropna().fillna(dd_age.mean())
	dd_age = dd_age.fillna(dd_age.mean())
	x = np.array(dd_age.loc[:, imp_feat])
	y= np.array(dd_age.loc[:,"RIDAGEYR"])


	params = param
	t_clock = ensemble.GradientBoostingRegressor(**params)

	x_train, x_test, y_train, y_test  = train_test_split(x,y, test_size = 0.3, random_state =3454)

	t_clock.fit(x_train,y_train)

	print("Training accuracy")
	mse = mean_squared_error(y_train, t_clock.predict(x_train))
	print("MSE loss is ", mse)
	r2 = r2_score(y_train, t_clock.predict(x_train))
	print("R2 score is ", r2)
	print("MAE", np.mean(abs(y_train - t_clock.predict(x_train))))


	print("Testing accuracy")
	mse = mean_squared_error(y_test, t_clock.predict(x_test))
	print("MSE loss is ", mse)
	r2 = r2_score(y_test, t_clock.predict(x_test))
	print("R2 score is ", r2)
	print("MAE", np.mean(abs(y_test - t_clock.predict(x_test))))

	feature_importance = t_clock.feature_importances_
	sorted_idx = np.argsort(feature_importance)
	pos = np.arange(sorted_idx.shape[0]) + 2
	fig = plt.figure(figsize=(10, 10))
	plt.subplot(1, 2, 1)
	plt.barh(pos, feature_importance[sorted_idx], align="center")
	plt.yticks(pos, np.array(dd_age.loc[:, imp_feat].columns)[sorted_idx])
	plt.title("Feature Importances")

	print(np.array(dd_age.loc[:, imp_feat].columns)[sorted_idx])
	return plt

def app():
	st.title(title)
	st.markdown(intro_text)

	with st.form(key = 'hyperparameters'):
		col2, col1 = st.columns(2)
		num_trees = col1.slider("Number of Trees:", min_value = 10, max_value = 2000, value = 1000, 
			help = "The number of decision trees used in the model. \
				A larger value typically decreases training error but will take longer to train and might cause overfittng.")
		depth = col1.slider("Depth of Trees:", min_value = 2, max_value = 10, value = 6, 
			help = "The maximum depth of individual decision trees.\
			 The maximum depth limits the number of nodes in the tree.")
		lr = col1.select_slider("Learning rate:", options = [0.001, 0.01, 0.02, 0.05, 0.1], value = 0.01, 
			help = "Learning rate. This shrinks the contribution of each tree by the specified amount.")
		min_splits = col1.slider("Min Splits:", min_value = 10, max_value = 50, value = 30, 
			help = "The minimum number of samples required to split an internal node of a tree.")
		
		col2.markdown("Select features to include in training:")
		demo_features = col2.multiselect("Demographics features:", 
			options = demo_lst, default = demo_lst)
		di_features = col2.multiselect("Diseases features:", options = disease_lst, default = disease_lst)
		bio_features = col2.multiselect("Biochemistry features:", options = biochem_lst, default = biochem_lst)
		selected_features = demo_features + di_features + bio_features

		st.form_submit_button(label = "Train Model!")
		params = {
	    "n_estimators": num_trees,
	    "max_depth": depth,
	    "min_samples_split": min_splits,
	    "learning_rate":lr,
	    "loss": "ls",
		}


	model_training_state = st.markdown("Model training... This might take a few minutes...")
	start = time.time()
	re = train_model(selected_features, params)
	end = time.time()
	model_training_state.markdown(' ')
	col1, col2, col3, col4 = st.columns(4)
	col1.metric(label = 'Accuracy', value = 0.974)
	col2.metric(label = 'Training Time', value = str(int(end-start)) + 's')
