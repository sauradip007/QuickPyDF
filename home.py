
import time
import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib as mpl
from sklearn.metrics import confusion_matrix

x = np.linspace(0, 10, 100)

st.set_page_config(
    page_title="MRM Doc Generator"

)
st.title("MRM Doc Generator")
st.sidebar.success("Select a page above.")



# st.title("File Uploader")
st.markdown('---')

dataframe= st.file_uploader("Upload file in .csv/.tsv format",type=["csv","tsv"])
validation = st.file_uploader("Upload validation file in .csv/.tsv format",type=["csv","tsv"])
# if not none we display whatevcer is going into the file uploader

side_num = st.sidebar.write("Select your visualisation type")
opt_num = st.sidebar.radio("Select Any Graph", options=['Scatterplot','Linechart', 'Barchart', 'Histogram'])

# Extract categorical columns (if any)->form inoput->django db connection
opt_cat = st.sidebar.radio("Select Any Graph", options=['kde','Heatmap', 'Classification-Report', 'Confusion Matrix'])

if dataframe is not None:
    st.checkbox("Use container width", value=False, key="use_container_width")
    df = pd.read_csv(dataframe)
    st.dataframe(df.head(), use_container_width=st.session_state.use_container_width)
    st.header("Info about the dataset")
    st.markdown('---')
    st.dataframe(df.describe(), use_container_width=st.session_state.use_container_width)

st.set_option('deprecation.showPyplotGlobalUse', False)
# Scatter
if dataframe is not None and opt_num == 'Scatterplot':
    st.markdown("<h1 style= 'text-align:center';> Scatter </h1>",
                unsafe_allow_html=True)

    # multioption list showing a list of numeric cols
    col1,col2 = st.columns(2)
    num_list = df.select_dtypes(include=np.number).columns.tolist()
    multione_select= col1.selectbox("Choose first numeric column",options=num_list)
    multitwo_select = col2.selectbox("Choose second numeric column", options=num_list)
    sns.scatterplot(x=df[multione_select],y=df[multitwo_select])
    st.pyplot()
# Linechart
# st.set_option('deprecation.showPyplotGlobalUse', False)
if dataframe is not None and opt_num == 'Linechart':
    st.markdown("<h1 style= 'text-align:center';> Lineplot </h1>",
                unsafe_allow_html=True)

    # multioption list showing a list of numeric cols
    col1,col2 = st.columns(2)
    num_list = df.select_dtypes(include=np.number).columns.tolist()
    multione_select= col1.selectbox("Choose first numeric column",options=num_list)
    multitwo_select = col2.selectbox("Choose second numeric column", options=num_list)
    sns.lineplot(x=df[multione_select],y=df[multitwo_select])
    st.pyplot()
# Bar graph
if dataframe is not None and opt_num == 'Barchart':
    st.markdown("<h1 style= 'text-align:center';> Barplot </h1>",
                unsafe_allow_html=True)

    # multioption list showing a list of numeric cols
    col1,col2 = st.columns(2)
    num_list = df.select_dtypes(include=np.number).columns.tolist()
    multione_select= col1.selectbox("Choose first numeric column",options=num_list)
    multitwo_select = col2.selectbox("Choose second numeric column", options=num_list)
    fig, ax = plt.subplots()
    sns.barplot(x=df[multione_select],y=df[multitwo_select],data=df,linewidth=4,ax=ax)
    st.pyplot(fig)
# Histogram
if dataframe is not None and opt_num == 'Histogram':
    st.markdown("<h1 style= 'text-align:center';> Histplot </h1>",
                unsafe_allow_html=True)

    # multioption list showing a list of numeric cols
    # col1,col2 = st.columns(2)
    num_list = df.select_dtypes(include=np.number).columns.tolist()
    multione_select= st.selectbox("Choose numeric column",options=num_list)
    # multitwo_select = col2.selectbox("Choose second numeric column", options=num_list)
    sns.histplot(x=df[multione_select])
    st.pyplot()

# Confusion Matrix
if dataframe is not None and opt_cat == 'Confusion Matrix':
    st.markdown("<h1 style= 'text-align:center';> Confusion Matrix </h1>",
                unsafe_allow_html=True)

    cat_list = ['model_output','model_target']
   
    
    # if dt of model output and prediction dont do anything else use lambda
    if df['model_output'].dtype != df['model_target'].dtype:
        def proba(x):
            if x < 0.5:
                return 0
            else:
                return 1
        df['model_output'] = df['model_output'].apply(lambda x: proba(x))
    
    cf_matrix = confusion_matrix(df['model_output'], df['model_target'])
    sns.heatmap(cf_matrix/np.sum(cf_matrix), annot=True,fmt='.2%', cmap='Blues')

    st.pyplot()



if dataframe is not None and opt_cat == 'Heatmap':
    st.markdown("<h1 style= 'text-align:center';> Heatmap </h1>",
                unsafe_allow_html=True)

    cat_list = ['model_output','model_target']
   
    
    # if dt of model output and prediction dont do anything else use lambda
    if df['model_output'].dtype != df['model_target'].dtype:
        def proba(x):
            if x < 0.5:
                return 0
            else:
                return 1
        df['model_output'] = df['model_output'].apply(lambda x: proba(x))
    

    mpl.rcParams.update(mpl.rcParamsDefault)
    # cf_matrix = confusion_matrix(df['model_output'], df['model_target'])
    heatmap = sns.heatmap(data=df.iloc[:,-2:])
    plt.show()
    st.pyplot(heatmap.figure)
# Heatmap




