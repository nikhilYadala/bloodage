import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn import ensemble
import sys
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

title = "Predicting Biological Age"

intro_text = """
---
**Train your own age prediction model using gradient boosting decision tree (GBDT) and evalute its performance!**
"""

# demo_lst = ['RIAGENDR - Gender',
#        'Race/Hispanic origin',
#        'Race/Hispanic origin w/ NH Asian',
#        'Six-month time period', 'DMDBORN4 - Country of birth',
#        'Education level - Adults 20+',
#        'Marital status', 'RIDEXPRG - Pregnancy status at exam',
#        'Full sample interview weight',
#        'Ratio of family income to poverty']

# disease_lst = ['Ever been told you have asthma',
#        'Still have asthma',
#        'Doctor ever said you were overweight',
#        'Ever receive blood transfusion',
#        'Estimated age in months at menarche',
#        'Doctor ever said you had arthritis',
#        'Which type of arthritis was it?',
#        'Ever told had congestive heart failure',
#        'Ever told you had coronary heart disease',
#        'Ever told you had angina/angina pectoris',
#        'Ever told you had heart attack',
#        'Ever told you had a stroke',
#        'Ever told you had thyroid problem',
#        'Ever told you had any liver condition',
#        'Liver condition: Fatty liver',
#        'Ever had gallbladder surgery?',
#        'Ever told you had cancer or malignancy',
#        'Doctor told you to control/lose weight',
#        'Are you now increasing exercise',
#        'Any metal objects inside your body?']

# biochem_lst = [ 'Alanine Aminotransferase (ALT) (IU/L)',
#               ' Albumin, refrigerated serum (g/dL)',
#               ' Albumin, refrigerated serum (g/L)',
#               ' Alkaline Phosphatase (ALP) (IU/L)',
#               ' Aspartate Aminotransferase (AST) (IU/L)',
#               ' Bicarbonate (mmol/L)',
#               ' Blood Urea Nitrogen (mg/dL)',
#               ' Blood Urea Nitrogen (mmol/L)',
#               ' Chloride (mmol/L)',
#               ' Creatine Phosphokinase (CPK) (IU/L)',
#               ' Creatinine, refrigerated serum (mg/dL)',
#               ' Creatinine, refrigerated serum (umol/L)',
#               ' Globulin (g/dL)', 'LBDSGBSI'
#               ' Glucose, refrigerated serum (mg/dL)',
#               ' Glucose, refrigerated serum (mmol/L)',
#               ' Gamma Glutamyl Transferase (GGT) (IU/L)',
#               ' Lactate Dehydrogenase (LDH) (IU/L)',
#               ' Osmolality (mmol/Kg)', 
#               ' Phosphorus (mmol/L)',
#               ' Sodium (mmol/L)',
#               ' Total Bilirubin (umol/L)',
#               ' Total Bilirubin Comment Code',
#               ' Cholesterol, refrigerated serum (mg/dL)',
#               ' Cholesterol, refrigerated serum (mmol/L)',
#               ' Total Protein (g/dL)',
#               ' Triglycerides, refrig serum (mg/dL)']

demographics_lst = ['SEQN',
'SDDSRVYR',
 'RIDSTATR',
 'RIAGENDR',
 'RIDAGEYR',
 # 'RIDAGEMN',
 'RIDRETH1',
 'RIDRETH3',
 'RIDEXMON',
 'DMDBORN4',
 # 'DMDYRUSZ',
 'DMDEDUC2',
 'DMDMARTZ',
 'RIDEXPRG',
 # 'SIALANG',
 # 'SIAPROXY',
 # 'SIAINTRP',
 # 'FIALANG',
 # 'FIAPROXY',
 # 'FIAINTRP',
 # 'MIALANG',
 # 'MIAPROXY',
 # 'MIAINTRP',
 # 'AIALANGA',
 # 'WTINTPRP',
 # 'WTMECPRP',
 # 'SDMVPSU',
 # 'SDMVSTRA',
 'INDFMPIR']

disease_lst = ['SEQN','MCQ010',
 'MCQ025',
 'MCQ035',
 'MCQ040',
 'MCQ050',
 'AGQ030',
 'MCQ053',
 'MCQ080',
 'MCQ092',
 'MCD093',
 'MCQ145',
 'MCQ149',
 'MCQ151',
 'RHD018',
 'MCQ160a',
 'MCQ195',
 'MCQ160b',
 'MCD180b',
 'MCQ160c',
 'MCD180c',
 'MCQ160d',
 'MCD180d',
 'MCQ160e',
 'MCD180e',
 'MCQ160f',
 'MCD180F',
 'MCQ160m',
 'MCQ170m',
 'MCD180M',
 'MCQ160p',
 'MCQ160l',
 'MCQ170l',
 'MCD180l',
 'MCQ500',
 'MCQ510a',
 'MCQ510b',
 'MCQ510c',
 'MCQ510d',
 'MCQ510e',
 'MCQ510f',
 'MCQ515',
 'MCQ520',
 'MCQ530',
 'MCQ540',
 'MCQ550',
 'MCQ560',
 'MCQ570',
 'MCQ220',
 'MCQ230a',
 'MCQ230b',
 'MCQ230c',
 'MCQ230d',
 'MCQ300b',
 'MCQ300c',
 'MCQ300a',
 'MCQ366a',
 'MCQ366b',
 'MCQ366c',
 'MCQ366d',
 'MCQ371a',
 'MCQ371b',
 'MCQ371c',
 'MCQ371d',
 'OSQ230']

biochem_lst = ['SEQN','LBXSATSI',
 'LBDSATLC',
 'LBXSAL',
 'LBDSALSI',
 'LBXSAPSI',
 'LBXSASSI',
 'LBXSC3SI',
 'LBXSBU',
 'LBDSBUSI',
 'LBXSCLSI',
 'LBXSCK',
 'LBXSCR',
 'LBDSCRSI',
 'LBXSGB',
 'LBDSGBSI',
 'LBXSGL',
 'LBDSGLSI',
 'LBXSGTSI',
 'LBDSGTLC',
 'LBXSIR',
 'LBDSIRSI',
 'LBXSLDSI',
 'LBXSOSSI',
 'LBXSPH',
 'LBDSPHSI',
 'LBXSKSI',
 'LBXSNASI',
 'LBXSTB',
 'LBDSTBSI',
 'LBDSTBLC',
 'LBXSCA',
 'LBDSCASI',
 'LBXSCH',
 'LBDSCHSI',
 'LBXSTP',
 'LBDSTPSI',
 'LBXSTR',
 'LBDSTRSI',
 'LBXSUA',
 'LBDSUASI']

demo_d = {'SEQN': 'Respondent sequence number',
    'SDDSRVYR': 'Data release cycle',
     'RIDSTATR': 'Interview/Examination status',
     'RIAGENDR': 'Gender',
     'RIDAGEYR': 'Age in years at screening',
     'RIDAGEMN': 'Age in months at screening',
     'RIDRETH1': 'Race/Hispanic origin',
     'RIDRETH3': 'Race/Hispanic origin w/ NH Asian',
     'RIDEXMON': 'Six-month time period',
     'DMDBORN4': 'Country of birth',
     'DMDYRUSZ': 'Length of time in US',
     'DMDEDUC2': 'Education level',
     'DMDMARTZ': 'Marital status',
     'RIDEXPRG': 'Pregnancy status at exam',
     'SIALANG': 'Language of SP Interview',
     'SIAPROXY': 'Proxy used in SP Interview?',
     'SIAINTRP': 'Interpreter used in SP Interview?',
     'FIALANG': 'Language of Family Interview',
     'FIAPROXY': 'Proxy used in Family Interview?',
     'FIAINTRP': 'Interpreter used in Family Interview?',
     'MIALANG': 'Language of MEC Interview',
     'MIAPROXY': 'Proxy used in MEC Interview?',
     'MIAINTRP': 'Interpreter used in MEC Interview?',
     'AIALANGA': 'Language of ACASI Interview',
     'WTINTPRP': 'Full sample interview weight',
     'WTMECPRP': 'Full sample MEC exam weight',
     'SDMVPSU': 'Masked variance pseudo-PSU',
     'SDMVSTRA': 'Masked variance pseudo-stratum',
     'INDFMPIR': 'Ratio of family income to poverty'}

dis_d = {'MCQ010': 'Ever been told you have asthma',
 'MCQ025': 'Age when first had asthma',
 'MCQ035': 'Still have asthma',
 'MCQ040': 'Had asthma attack in past year',
 'MCQ050': 'Emergency care visit for asthma/past yr',
 'AGQ030': 'Did SP have episode of hay fever/past yr',
 'MCQ053': 'Taking treatment for anemia/past 3 mos',
 'MCQ080': 'Doctor ever said you were overweight',
 'MCQ092': 'Ever receive blood transfusion',
 'MCD093': 'Year receive blood transfusion',
 'MCQ145': 'CHECK ITEM',
 'MCQ149': 'Menstrual periods started yet?',
 'MCQ151': 'Age in years at first menstrual period',
 'RHD018': 'Estimated age in months at menarche',
 'MCQ160a': 'Doctor ever said you had arthritis',
 'MCQ195': 'Which type of arthritis was it?',
 'MCQ160b': 'Ever told had congestive heart failure',
 'MCD180b': 'Age when told you had heart failure',
 'MCQ160c': 'Ever told you had coronary heart disease',
 'MCD180c': 'Age when told had coronary heart disease',
 'MCQ160d': 'Ever told you had angina/angina pectoris',
 'MCD180d': 'Age when told you had angina pectoris',
 'MCQ160e': 'Ever told you had heart attack',
 'MCD180e': 'Age when told you had heart attack',
 'MCQ160f': 'Ever told you had a stroke',
 'MCD180F': 'Age when told you had a stroke',
 'MCQ160m': 'Ever told you had thyroid problem',
 'MCQ170m': 'Do you still have thyroid problem',
 'MCD180M': 'Age when told you had thyroid problem',
 'MCQ160p': 'Ever told you had COPD, emphysema, ChB',
 'MCQ160l': 'Ever told you had any liver condition',
 'MCQ170l': 'Do you still have a liver condition',
 'MCD180l': 'Age when told you had a liver condition',
 'MCQ500': 'Ever told you had any liver condition',
 'MCQ510a': 'Liver condition: Fatty liver',
 'MCQ510b': 'Liver condition: Liver fibrosis',
 'MCQ510c': 'Liver condition: Liver cirrhosis',
 'MCQ510d': 'Liver condition: Viral hepatitis',
 'MCQ510e': 'Liver condition: Autoimmune hepatitis',
 'MCQ510f': 'Liver condition: Other liver disease',
 'MCQ515': 'CHECK ITEM',
 'MCQ520': 'Abdominal pain during past 12 months?',
 'MCQ530': 'Where was the most uncomfortable pain',
 'MCQ540': 'Ever seen a DR about this pain',
 'MCQ550': 'Has DR ever said you have gallstones',
 'MCQ560': 'Ever had gallbladder surgery?',
 'MCQ570': 'Age when 1st had gallbladder surgery?',
 'MCQ220': 'Ever told you had cancer or malignancy',
 'MCQ230a': '1st cancer',
 'MCQ230b': '2nd cancer',
 'MCQ230c': '3rd cancer',
 'MCQ230d': 'More than 3 kinds of cancer',
 'MCQ300b': 'Close relative had asthma?',
 'MCQ300c': 'Close relative had diabetes?',
 'MCQ300a': 'Close relative had heart attack?',
 'MCQ366a': 'Doctor told you to control/lose weight',
 'MCQ366b': 'Doctor told you to exercise',
 'MCQ366c': 'Doctor told you to reduce salt in diet',
 'MCQ366d': 'Doctor told you to reduce fat/calories',
 'MCQ371a': 'Are you now controlling or losing weight',
 'MCQ371b': 'Are you now increasing exercise',
 'MCQ371c': 'Are you now reducing salt in diet',
 'MCQ371d': 'Are you now reducing fat in diet',
 'OSQ230': 'Any metal objects inside your body?'}

bio_d = {'LBXSATSI': 'Alanine Aminotransferase (ALT) (IU/L)',
 'LBDSATLC': 'ALT Comment Code',
 'LBXSAL': 'Albumin, refrigerated serum (g/dL)',
 'LBDSALSI': 'Albumin, refrigerated serum (g/L)',
 'LBXSAPSI': 'Alkaline Phosphatase (ALP) (IU/L)',
 'LBXSASSI': 'Aspartate Aminotransferase (AST) (IU/L)',
 'LBXSC3SI': 'Bicarbonate (mmol/L)',
 'LBXSBU': 'Blood Urea Nitrogen (mg/dL)',
 'LBDSBUSI': 'Blood Urea Nitrogen (mmol/L)',
 'LBXSCLSI': 'Chloride (mmol/L)',
 'LBXSCK': 'Creatine Phosphokinase (CPK) (IU/L)',
 'LBXSCR': 'Creatinine, refrigerated serum (mg/dL)',
 'LBDSCRSI': 'Creatinine, refrigerated serum (umol/L)',
 'LBXSGB': 'Globulin (g/dL)',
 'LBDSGBSI': 'Globulin (g/L)',
 'LBXSGL': 'Glucose, refrigerated serum (mg/dL)',
 'LBDSGLSI': 'Glucose, refrigerated serum (mmol/L)',
 'LBXSGTSI': 'Gamma Glutamyl Transferase (GGT) (IU/L)',
 'LBDSGTLC': 'GGT Comment Code',
 'LBXSIR': 'Iron, refrigerated serum (ug/dL)',
 'LBDSIRSI': 'Iron, refrigerated serum (umol/L)',
 'LBXSLDSI': 'Lactate Dehydrogenase (LDH) (IU/L)',
 'LBXSOSSI': 'Osmolality (mmol/Kg)',
 'LBXSPH': 'Phosphorus (mg/dL)',
 'LBDSPHSI': 'Phosphorus (mmol/L)',
 'LBXSKSI': 'Potassium (mmol/L)',
 'LBXSNASI': 'Sodium (mmol/L)',
 'LBXSTB': 'Total Bilirubin (mg/dL)',
 'LBDSTBSI': 'Total Bilirubin (umol/L)',
 'LBDSTBLC': 'Total Bilirubin Comment Code',
 'LBXSCA': 'Total Calcium (mg/dL)',
 'LBDSCASI': 'Total Calcium (mmol/L)',
 'LBXSCH': 'Cholesterol, refrigerated serum (mg/dL)',
 'LBDSCHSI': 'Cholesterol, refrigerated serum (mmol/L)',
 'LBXSTP': 'Total Protein (g/dL)',
 'LBDSTPSI': 'Total Protein (g/L)',
 'LBXSTR': 'Triglycerides, refrig serum (mg/dL)',
 'LBDSTRSI': 'Triglycerides, refrig serum (mmol/L)',
 'LBXSUA': 'Uric acid (mg/dL)',
 'LBDSUASI': 'Uric acid (umol/L)'}

data_url = 'https://raw.githubusercontent.com/ZhouyaoXie/age-vis/main/data/data_n.csv'

col_d = {'mcq010': 'Ever been told you have asthma',
 'mcq025': 'Age when first had asthma',
 'mcq035': 'Still have asthma',
 'mcq040': 'Had asthma attack in past year',
 'mcq050': 'Emergency care visit for asthma/past yr',
 'agq030': 'Did SP have episode of hay fever/past yr',
 'mcq053': 'Taking treatment for anemia/past 3 mos',
 'mcq080': 'Doctor ever said you were overweight',
 'mcq092': 'Ever receive blood transfusion',
 'mcd093': 'Year receive blood transfusion',
 'mcq145': 'CHECK ITEM',
 'mcq149': 'Menstrual periods started yet?',
 'mcq151': 'Age in years at first menstrual period',
 'rhd018': 'Estimated age in months at menarche',
 'mcq160a': 'Doctor ever said you had arthritis',
 'mcq195': 'Which type of arthritis was it?',
 'mcq160b': 'Ever told had congestive heart failure',
 'mcd180b': 'Age when told you had heart failure',
 'mcq160c': 'Ever told you had coronary heart disease',
 'mcd180c': 'Age when told had coronary heart disease',
 'mcq160d': 'Ever told you had angina/angina pectoris',
 'mcd180d': 'Age when told you had angina pectoris',
 'mcq160e': 'Ever told you had heart attack',
 'mcd180e': 'Age when told you had heart attack',
 'mcq160f': 'Ever told you had a stroke',
 'mcd180f': 'Age when told you had a stroke',
 'mcq160m': 'Ever told you had thyroid problem',
 'mcq170m': 'Do you still have thyroid problem',
 'mcd180m': 'Age when told you had thyroid problem',
 'mcq160p': 'Ever told you had COPD, emphysema, ChB',
 'mcq160l': 'Ever told you had any liver condition',
 'mcq170l': 'Do you still have a liver condition',
 'mcd180l': 'Age when told you had a liver condition',
 'mcq500': 'Ever told you had any liver condition',
 'mcq510a': 'Liver condition: Fatty liver',
 'mcq510b': 'Liver condition: Liver fibrosis',
 'mcq510c': 'Liver condition: Liver cirrhosis',
 'mcq510d': 'Liver condition: Viral hepatitis',
 'mcq510e': 'Liver condition: Autoimmune hepatitis',
 'mcq510f': 'Liver condition: Other liver disease',
 'mcq515': 'CHECK ITEM',
 'mcq520': 'Abdominal pain during past 12 months?',
 'mcq530': 'Where was the most uncomfortable pain',
 'mcq540': 'Ever seen a DR about this pain',
 'mcq550': 'Has DR ever said you have gallstones',
 'mcq560': 'Ever had gallbladder surgery?',
 'mcq570': 'Age when 1st had gallbladder surgery?',
 'mcq220': 'Ever told you had cancer or malignancy',
 'mcq230a': '1st cancerwhat kind was it?',
 'mcq230b': '2nd cancerwhat kind was it?',
 'mcq230c': '3rd cancerwhat kind was it?',
 'mcq230d': 'More than 3 kinds of cancer',
 'mcq300b': 'Close relative had asthma?',
 'mcq300c': 'Close relative had diabetes?',
 'mcq300a': 'Close relative had heart attack?',
 'mcq366a': 'Doctor told you to control/lose weight',
 'mcq366b': 'Doctor told you to exercise',
 'mcq366c': 'Doctor told you to reduce salt in diet',
 'mcq366d': 'Doctor told you to reduce fat/calories',
 'mcq371a': 'Are you now controlling or losing weight',
 'mcq371b': 'Are you now increasing exercise',
 'mcq371c': 'Are you now reducing salt in diet',
 'mcq371d': 'Are you now reducing fat in diet',
 'osq230': 'Any metal objects inside your body?',
 'seqn': 'Respondent Sequence Number',
 'lbxsatsi': 'Alanine Aminotransferase (ALT) (IU/L)',
 'lbdsatlc': 'ALT Comment Code',
 'lbxsal': 'Albumin, refrigerated serum (g/dL)',
 'lbdsalsi': 'Albumin, refrigerated serum (g/L)',
 'lbxsapsi': 'Alkaline Phosphatase (ALP) (IU/L)',
 'lbxsassi': 'Aspartate Aminotransferase (AST) (IU/L)',
 'lbxsc3si': 'Bicarbonate (mmol/L)',
 'lbxsbu': 'Blood Urea Nitrogen (mg/dL)',
 'lbdsbusi': 'Blood Urea Nitrogen (mmol/L)',
 'lbxsclsi': 'Chloride (mmol/L)',
 'lbxsck': 'Creatine Phosphokinase (CPK) (IU/L)',
 'lbxscr': 'Creatinine, refrigerated serum (mg/dL)',
 'lbdscrsi': 'Creatinine, refrigerated serum (umol/L)',
 'lbxsgb': 'Globulin (g/dL)',
 'lbdsgbsi': 'Globulin (g/L)',
 'lbxsgl': 'Glucose, refrigerated serum (mg/dL)',
 'lbdsglsi': 'Glucose, refrigerated serum (mmol/L)',
 'lbxsgtsi': 'Gamma Glutamyl Transferase (GGT) (IU/L)',
 'lbdsgtlc': 'GGT Comment Code',
 'lbxsir': 'Iron, refrigerated serum (ug/dL)',
 'lbdsirsi': 'Iron, refrigerated serum (umol/L)',
 'lbxsldsi': 'Lactate Dehydrogenase (LDH) (IU/L)',
 'lbxsossi': 'Osmolality (mmol/Kg)',
 'lbxsph': 'Phosphorus (mg/dL)',
 'lbdsphsi': 'Phosphorus (mmol/L)',
 'lbxsksi': 'Potassium (mmol/L)',
 'lbxsnasi': 'Sodium (mmol/L)',
 'lbxstb': 'Total Bilirubin (mg/dL)',
 'lbdstbsi': 'Total Bilirubin (umol/L)',
 'lbdstblc': 'Total Bilirubin Comment Code',
 'lbxsca': 'Total Calcium (mg/dL)',
 'lbdscasi': 'Total Calcium (mmol/L)',
 'lbxsch': 'Cholesterol, refrigerated serum (mg/dL)',
 'lbdschsi': 'Cholesterol, refrigerated serum (mmol/L)',
 'lbxstp': 'Total Protein (g/dL)',
 'lbdstpsi': 'Total Protein (g/L)',
 'lbxstr': 'Triglycerides, refrig serum (mg/dL)',
 'lbdstrsi': 'Triglycerides, refrig serum (mmol/L)',
 'lbxsua': 'Uric acid (mg/dL)',
 'lbdsuasi': 'Uric acid (umol/L)',
 'wtsafprp': 'Fasting Subsample Weight',
 'lbxtr': 'Triglyceride (mg/dL)',
 'lbdtrsi': 'Triglyceride (mmol/L)',
 'lbdldl': 'LDL-Cholesterol, Friedewald (mg/dL)',
 'lbdldlsi': 'LDL-Cholesterol, Friedewald (mmol/L)',
 'lbdldlm': 'LDL-Cholesterol, Martin-Hopkins (mg/dL)',
 'lbdldmsi': 'LDL-Cholesterol, Martin-Hopkins (mmol/L)',
 'lbdldln': 'LDL-Cholesterol, NIH equation 2 (mg/dL)',
 'lbdldnsi': 'LDL-Cholesterol, NIH equation 2 (mmol/L) ',
 'lbxwbcsi': 'White blood cell count (1000 cells/uL)',
 'lbxlypct': 'Lymphocyte percent (%)',
 'lbxmopct': 'Monocyte percent (%)',
 'lbxnepct': 'Segmented neutrophils percent (%)',
 'lbxeopct': 'Eosinophils percent (%)',
 'lbxbapct': 'Basophils percent (%)',
 'lbdlymno': 'Lymphocyte number (1000 cells/uL)',
 'lbdmono': 'Monocyte number (1000 cells/uL)',
 'lbdneno': 'Segmented neutrophils num (1000 cell/uL)',
 'lbdeono': 'Eosinophils number (1000 cells/uL)',
 'lbdbano': 'Basophils number (1000 cells/uL)',
 'lbxrbcsi': 'Red blood cell count (million cells/uL)',
 'lbxhgb': 'Hemoglobin (g/dL)',
 'lbxhct': 'Hematocrit (%)',
 'lbxmcvsi': 'Mean cell volume (fL)',
 'lbxmc': 'Mean Cell Hgb Conc. (g/dL)',
 'lbxmchsi': 'Mean cell hemoglobin (pg)',
 'lbxrdw': 'Red cell distribution width (%)',
 'lbxpltsi': 'Platelet count (1000 cells/uL)',
 'lbxmpsi': 'Mean platelet volume (fL)',
 'lbxnrbc': 'Nucleated red blood cells ',
 'lbdhdd': 'Direct HDL-Cholesterol (mg/dL)',
 'lbdhddsi': 'Direct HDL-Cholesterol (mmol/L) ',
 'lbxhscrp': 'HS C-Reactive Protein (mg/L)',
 'lbdhrplc': 'HS C-Reactive Protein Comment Code '}

bio_d.update(dis_d)
bio_d.update(demo_d)
col_d = {}
for k, v in bio_d.items():
    col_d[k.lower()] = v

@st.cache
def load_data(data_url):
    dd_age = pd.read_csv(data_url)
    return dd_age


def train_model(imp_feat, param):
    # path_prefix = "../05839/NHANES/2017-2020"
    # dd_age = pd.read_sas(os.path.join(path_prefix, "P_BIOPRO.XPT"), format = "XPORT")
    # dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_MCQ.XPT"), format = "XPORT"), how = "outer")
    # dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_TRIGLY.XPT"), format = "XPORT"), how = "outer")
    # dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_HSCRP.XPT"), format = "XPORT"), how = "outer")
    # dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_HDL.XPT"), format = "XPORT"), how = "outer")
    # dd_age = dd_age.merge(pd.read_sas(os.path.join(path_prefix, "P_CBC.XPT"), format = "XPORT"), how = "outer")

    # dd_age = data_n.copy()
    # dd_age= dd_age.drop(columns=["SEQN"])
    print('start loading')
    t1 = time.time()
    dd_age = load_data(data_url)
    t2 = time.time()
    print(t2 - t1)
    age = dd_age[["SEQN","RIDAGEYR"]]
    dd_age = dd_age.drop(columns=["RIDAGEYR", "SDDSRVYR", "RIDAGEYR", "RIDAGEMN", "DMDYRUSZ" ,"MCQ025", "MCD093", "MCQ151" ])
    dd_age = dd_age.merge(age, how= "outer")
    dd_age= dd_age.drop(columns=["SEQN"])

    if "RIDAGEYR" in imp_feat:
    	imp_feat.remove("RIDAGEYR")
    imp_feat = list(set(dd_age.columns).intersection(set(imp_feat)))

    # dd_age = dd_age.dropna().fillna(dd_age.mean())
    dd_age = dd_age.fillna(dd_age.mean())
    x = np.array(dd_age.loc[:, imp_feat])
    y= np.array(dd_age.loc[:,"RIDAGEYR"])

    t3 = time.time()
    print(t3 - t2)
    params = param
    t_clock = ensemble.GradientBoostingRegressor(**params)

    x_train, x_test, y_train, y_test  = train_test_split(x,y, test_size = 0.3, random_state =3454)

    t_clock.fit(x_train,y_train)

    t4 = time.time()
    print(t4 - t3)

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
    mae = np.mean(abs(y_test - t_clock.predict(x_test)))
    print("MAE", np.mean(abs(y_test - t_clock.predict(x_test))))

    t5 = time.time()
    print(t5 - t4)

    # feature_importance = t_clock.feature_importances_
    # sorted_idx = np.argsort(feature_importance)
    # pos = np.arange(sorted_idx.shape[0]) + 2
    # fig = plt.figure(figsize=(10, 10))
    # plt.subplot(1, 2, 1)
    # plt.barh(pos, feature_importance[sorted_idx], align="center")
    # plt.yticks(pos, np.array(dd_age.loc[:, imp_feat].columns)[sorted_idx])
    # plt.title("Feature Importances")

    # print(np.array(dd_age.loc[:, imp_feat].columns)[sorted_idx])
    return t_clock, mse, r2, mae, dd_age, imp_feat

def plot_fea(t_clock = None, n_featuers = None, dd_age = None, imp_feat = None):
    if not t_clock: return
    feature_importance = t_clock.feature_importances_
    sorted_idx = np.argsort(feature_importance)[-n_featuers:]
    pos = np.arange(sorted_idx.shape[0]) + 2
    fig = plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.barh(pos, feature_importance[sorted_idx], align="center")
    # print(len(dd_age.columns), len(col_d.keys()))
    col_dd = {}
    for col in dd_age.columns:
        if col.lower() in col_d: col_dd[col] = col_d[col.lower()]
    # dd_age = dd_age.rename(columns = col_dd)
    plt.yticks(pos, np.array(dd_age.loc[:, imp_feat].rename(columns = col_dd).columns)[sorted_idx])
    plt.title("Feature Importances")
    return fig

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
        n_featuers = col1.slider("Number of top features to display", 
            min_value = 2, max_value = 40, value = 30)

        col2.markdown("Select features to include in training:")
        select = []
        demo = col2.checkbox("Demographics features", value = True)
        if demo: select.extend(demographics_lst)
        dis = col2.checkbox("Diseases features", value = True)
        if dis: select.extend(disease_lst)
        bio = col2.checkbox("Biochemistry features", value = True)
        if bio: select.extend(biochem_lst)
        # demo_features = col2.multiselect("Demographics features:", 
        #   options = demo_lst, default = demo_lst)
        # di_features = col2.multiselect("Diseases features:", options = disease_lst, default = disease_lst)
        # bio_features = col2.multiselect("Biochemistry features:", options = biochem_lst, default = biochem_lst)
        # selected_features = demo_features + di_features + bio_features

        submitted = st.form_submit_button(label = "Train Model!")
        # t_clock, n_featuers, dd_age, imp_feat = None, None, None, None
        # mse, mae, r2, tt = None, None, None, None
        if submitted:
            params = {
            "n_estimators": num_trees,
            "max_depth": depth,
            "min_samples_split": min_splits,
            "learning_rate":lr,
            "loss": "ls",
            }

            model_training_state = st.markdown("Model training... This might take a few minutes...")
            start = time.time()
            # fig = Figure()
            t_clock, mse, r2, mae, dd_age, imp_feat = train_model(select, params)
            end = time.time()
            tt = str(int(end-start))
            model_training_state.markdown(' ')

            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label = 'MSE', value = np.round(mse, 2) if mse else None)
            col2.metric(label = 'MAE', value = np.round(mae, 2) if mae else None)
            col3.metric(label = 'R-Squared', value = np.round(r2, 2) if r2 else None)
            col4.metric(label = 'Training Time', value = tt + 's' if tt else None)
            fig = plot_fea(t_clock, n_featuers, dd_age, imp_feat)
            st.pyplot(fig)

