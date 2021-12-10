import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

title = "Predicting Biological Age"

intro_text = """
**Train your own age prediction model using gradient boosting decision tree (GBDT) and evalute its performance!**
"""

def train_model():
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

	params = {
	    "n_estimators": 4000,
	    "max_depth": 8,
	    "min_samples_split": 30,
	    "learning_rate": 0.01,
	    "loss": "ls",
	}
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
		
		col2.markdown("Select sets of features to include in training:")
		col2.checkbox("Demographics features:", value = True)
		col2.checkbox("Diseases features:", value = True)
		col2.checkbox("Biochemistry features:", value = True)

		st.form_submit_button(label = "Train Model!")

	model_training_state = st.markdown("Model training... This might take a few minutes...")
	start = time.time()
	re = train_model()
	end = time.time()
	model_training_state.markdown(' ')
	col1, col2, col3, col4 = st.columns(4)
	col1.metric(label = 'Accuracy', value = 0.974)
	col2.metric(label = 'Training Time', value = str(int(end-start)) + 's')
