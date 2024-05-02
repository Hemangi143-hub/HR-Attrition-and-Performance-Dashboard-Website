#Library for Data Visualization.
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Libray for Data Manipulation.
import pandas as pd
import numpy as np

# Library to perform Statistical Analysis.
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency

# Library to overcome Warnings.
import warnings
warnings.filterwarnings("ignore")

#  Functions for data visualization and analysis.
import functions

#Code for Visualization
st.set_page_config(layout="wide", page_icon=":bar_chart:", page_title='HR Attrition and Performance Dashboard')
st.image('HR1.png', width=150) 
st.title("HR Attrition and Performance")

functions.space()
st.write('<p style="font-size:130%">Import Dataset</p>', unsafe_allow_html=True)

#Selecting CSV or Exel File
file_format = st.radio("Select File Format: ", ('csv','excel'), key='file_format')
dataset = st.file_uploader(label='')

#Default dataset
use_defo = st.checkbox('Use Example Dataset')
if use_defo:
    dataset = 'raw_hr_data1.csv'

#sidebar
st.sidebar.header('Import Dataset to Use Available Features: 👉')

if dataset:
    all_visuals = ['Dataset', 'Exploratory Data Analysis', 'Statistical Analysis']
    #functions.sidebar_space(2)
    visuals = st.sidebar.multiselect("Choose which visualizations you want to see 👇", all_visuals)

    if 'Dataset' in visuals :
        if file_format == 'csv' or use_defo:
            df = pd.read_csv(dataset)
        else:
            df = pd.read_excel(dataset)

        st.header('_DataSet:_')
        n, m = df.shape
        st.write(f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)   
        st.dataframe(df)
        
    #Exploratory Data Analysis
    if 'Exploratory Data Analysis' in visuals:
        all_visual=['Rate wise Employee Attrition','Gender wise Employee Attrition','Age wise Employee Attrition',
                    'Business Travel wise Employee Attrition','Department wise Employee Attrition','DailyRate wise Employee Attrition',
                    'Distance From Home wise Employee Attrition','Education wise Employee Attrition',
                    'Education Field wise Employee Attrition','Environment Satisfaction wise Employee Attrition',
                    'JobRoles wise Employee Attrition','Job Level wise Employee Attrition',
                    'Job Satisfaction wise Employee Attrition','Marital Status wise Employee Attrition',
                    'Monthly Income wise Employee Attrition','Monthly Rate wise Employee Attrition',
                    'Number of Companies Worked wise Employee Attrition','Over Time wise Employee Attrition',
                    'Percentage Salary Hike wise Employee Attrition','Performance Rating wise Employee Attrition',
                    'Relationship Satisfaction wise Employee Attrition','Work Life Balance wise Employee Attrition',
                    'Total Working Years wise Employee Attrition','Years at Company wise Employee Attrition',
                    'Years In Current Role wise Employee Attrition','Years Since Last Promotion wise Employee Attrition',
                    'Years with Current Manager wise Employee Attrition']
        visual = st.sidebar.multiselect("Choose which features you want to explore on data 👇", all_visual)

        # Visualize the Employee Attrition in Counts
        st.header("_Exploratory Data Analysis:_")
        if 'Rate wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Attrition")
            if "Attrition" in df.columns:
                # Visualization to show Employee Attrition in Counts.
                plt.figure(figsize=(17, 6))
                plt.subplot(1, 2, 1)
                attrition_rate = df["Attrition"].value_counts()
                sns.barplot(x=attrition_rate.index, y=attrition_rate.values, palette=["#11f9f9", "#ffff00"])
                plt.title("Employee Attrition Counts", fontweight="black", size=20, pad=20)
                for i, v in enumerate(attrition_rate.values):
                    plt.text(i, v, v, ha="center", fontweight='black', fontsize=18)
                
                # Visualization to show Employee Attrition in Percentage.
                plt.subplot(1, 2, 2)
                plt.pie(attrition_rate, labels=["No", "Yes"], autopct="%.2f%%", textprops={"fontweight": "black", 
                        "size": 15},colors=["#11f9f9", "#ffff00"], explode=[0, 0.1], startangle=90)
                center_circle = plt.Circle((0, 0), 0.3, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)
                plt.title("Employee Attrition Rate", fontweight="black", size=20, pad=10)
                # Display the plots using Streamlit
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'Attrition' columns.")
        
        # Visualize the Employee Attrition in Percentage
        if 'Gender wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Gender")            
            if "Attrition" in df.columns and "Gender" in df.columns:
                # Visualization to show Total Employees by Gender.
                plt.figure(figsize=(14, 6))
                plt.subplot(1, 2, 1)
                gender_distribution = df["Gender"].value_counts()
                plt.title("Employees Distribution by Gender", fontweight="black", size=20)
                plt.pie(gender_distribution, autopct="%.0f%%", labels=gender_distribution.index,
                        textprops=({"fontweight": "black", "size": 20}), explode=[0, 0.1], startangle=90,
                        colors=["#ffb563", "#FFC0CB"])

                # Visualization to show Employee Attrition by Gender.
                plt.subplot(1, 2, 2)
                new_df = df[df["Attrition"] == "Yes"]
                value_1 = df["Gender"].value_counts()
                value_2 = new_df["Gender"].value_counts()
                attrition_rate = np.floor((value_2 / value_1) * 100).values
                sns.barplot(x=value_2.index, y=value_2.values, palette=["#D4A1E7", "#E7A1A1"])
                plt.title("Employee Attrition Rate by Gender", fontweight="black", size=20, pad=20)
                for index, value in enumerate(value_2):
                    plt.text(index, value, str(value) + " (" + str(int(attrition_rate[index])) + "% )", ha="center", va="bottom",
                        size=15, fontweight="black")
                plt.tight_layout()
                # Display the plots using Streamlit
                st.pyplot(plt)
            else: 
                st.error("The Uploaded Dataset Doesn't contain 'Gender' columns.")

        #visualization to show Employee Distribution by Age.
        if 'Age wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Age")
            if "Attrition" in df.columns and "Age" in df.columns:
                plt.figure(figsize=(13.5, 6))
                plt.subplot(1, 2, 1)
                sns.histplot(x="Age", hue="Attrition", data=df, kde=True, palette=["#cb007d", "#71f50b86"])
                plt.title("Employee Distribution by Age", fontweight="black", size=20, pad=10)

                # Visualization to show Employee Distribution by Age & Attrition.
                plt.subplot(1, 2, 2)
                sns.boxplot(x="Attrition", y="Age", data=df, palette=["#D4A1E7", "#cb01fd86"])
                plt.title("Employee Distribution by Age & Attrition", fontweight="black", size=20, pad=10)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'Age' columns.")

        if 'Business Travel wise Employee Attrition' in visual:
            st.subheader("Employees Distribution by Business Travel")
            if "Attrition" in df.columns and "BusinessTravel" in df.columns:                
                #Attrition rate by Business Travel 
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["BusinessTravel"].value_counts()
                plt.title("Attrition Rate by Business Travel", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct = "%.1f%%", pctdistance = 0.75, startangle = 90, colors = ['#0b0bf599', '#264fe386','#d0dcf6'],
                        textprops={"fontweight":"black", "size":15})
                center_circle = plt.Circle((0,0),0.4,fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)
                
                #Attrition by Business Travel
                plt.subplot(1, 2, 2)
                new_df = df[df["Attrition"] == "Yes"]
                value_2 = new_df["BusinessTravel"].value_counts()
                attrition_rate = np.floor((value_2 / value_1) * 100).values
                sns.barplot(x=value_2.index, y=value_2.values, palette=["#11264e", "#176aa5", "#279aec"])
                plt.title("Attrition Rate by Business Travel", fontweight="black", size=20, pad=20)
                for index, value in enumerate(value_2):
                    plt.text(index, value, str(value) + " (" + str(int(attrition_rate[index])) + "% )", ha="center", va="bottom",
                        size=10, fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'BusinessTravel' columns.")
        
        #Visualization to show Total Employees by Department.
        if 'Department wise Employee Attrition' in visual:
            if "Attrition" in df.columns and "Department" in df.columns:
                # Visualization to show Total Employees by Department.
                st.subheader("Employees Distribution by Department")
                plt.figure(figsize=(14, 6))
                plt.subplot(1, 2, 1)
                value_1 = df["Department"].value_counts()
                sns.barplot(x=value_1.index, y=value_1.values, palette=["#f67b4a", "#ea9d7c", "#FFC0CB"])
                plt.title("Employees by Department", fontweight="black", size=20, pad=20)
                for index, value in enumerate(value_1.values):
                    plt.text(index, value, str(value), ha="center", va="bottom", fontweight="black", size=15)

                # Visualization to show Employee Attrition Rate by Department.
                plt.subplot(1, 2, 2)
                new_df = df[df["Attrition"] == "Yes"]
                value_2 = new_df["Department"].value_counts()
                attrition_rate = np.floor((value_2 / value_1) * 100).values
                sns.barplot(x=value_2.index, y=value_2.values, palette=["#660b30", "#dc2d73", "#f070a3"])
                plt.title("Attrition Rate by Department", fontweight="black", size=20, pad=20)
                for index, value in enumerate(value_2):
                    plt.text(index, value, str(value) + " (" + str(attrition_rate[index]) + "% )", ha="center", 
                            va="bottom", size=13, fontweight="black")
                plt.tight_layout()
                # Display the plots using Streamlit
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'Department' columns.")

        if 'DailyRate wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Daily Rate")
            if "DailyRate" in df.columns:
                df["DailyRate"].describe().to_frame().T
                # Define the bin edges for the groups
                bin_edges = [0, 500, 1000, 1500]
                # Define the labels for the groups
                bin_labels = ['Low DailyRate', 'Average DailyRate', 'High DailyRate']
                # Cut the DailyRate column into groups
                df['DailyRateGroup'] = pd.cut(df['DailyRate'], bins=bin_edges, labels=bin_labels)
                ##Visualization to show Total Employees by DailyRateGroup.
                plt.figure(figsize=(13,6))
                plt.subplot(1,2,1)
                value_1 = df["DailyRateGroup"].value_counts()
                plt.pie(value_1.values, labels=value_1.index,autopct="%.2f%%",textprops={"fontweight":"black","size":15},explode=[0.1,0.1,0.1],colors= ['#FF8000', '#FF9933', '#FFB366'])
                plt.title("Employees by DailyRateGroup",fontweight="black",pad=15,size=18)
                
                #Visualization to show Attrition Rate by DailyRateGroup.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["DailyRateGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(),y= value_2.values,palette=["#11264e","#6faea4","#FEE08B"])
                plt.title("Employee Attrition Rate by DailyRateGroup",fontweight="black",pad=15,size=18)
                for index,value in enumerate(value_2.values):
                    plt.text(index,value, str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",fontweight="black",size=15)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'DailyRateGroup' columns.")
                
        if 'Distance From Home wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Distance From Home")
            if "DistanceFromHome" in df.columns:
                st.write("Total Unique Values in Attribute is =>",df["DistanceFromHome"].nunique())
                df["DistanceFromHome"].describe().to_frame().T
                # Define the bin edges for the groups
                bin_edges = [0,2,5,10,30]
                # Define the labels for the groups
                bin_labels = ['0-2 kms', '3-5 kms', '6-10 kms',"10+ kms"]

                # Cuttinf the DistaanceFromHome column into groups
                df['DistanceGroup'] = pd.cut(df['DistanceFromHome'], bins=bin_edges, labels=bin_labels)
                ##Visualization to show Total Employees by DistnaceFromHome.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["DistanceGroup"].value_counts()
                sns.barplot(x=value_1.index.tolist(), y=value_1.values,palette = ["#FFA07A", "#D4A1E7", "#FFC0CB","#87CEFA"])
                plt.title("Employees by Distance From Home",fontweight="black",pad=15,size=18)
                for index, value in enumerate(value_1.values):
                    plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15)
                
                #Visualization to show Attrition Rate by DistanceFromHome.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["DistanceGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(),y= value_2.values,palette=["#fe2146","#d47bf5","#fc7b90","#D4A1E7"])
                plt.title("Attrition Rate by DistanceFromHome",fontweight="black",pad=15,size=18)
                for index,value in enumerate(value_2.values):
                    plt.text(index,value, str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",fontweight="black",size=15)

                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'DistanceGroup' columns.")
                
        if 'Education wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Education")
            #Visualization to show Total Employees by Education.
            if "Education" in df.columns:
                df["Education"] = df["Education"].replace({1:"Below College",2:"College",3:"Bachelor",4:"Master",5:"Doctor"})
                plt.figure(figsize=(13.5,6))
                plt.subplot(1,2,1)
                value_1 = df["Education"].value_counts()
                sns.barplot(x=value_1.index, y=value_1.values, order=value_1.index, palette = ["#03304C", "#0369a9", "#2997db","#7dcdff","#a8dcfd"])
                plt.title("Employees Distribution by Education", fontweight="black", size=20,pad=15)
                for index,value in enumerate(value_1.values):
                    plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15)
                    
                #Visualization to show Employee Attrition by Education.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"] == "Yes"]
                value_2 = new_df["Education"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
                plt.title("Employee Attrition by Education",fontweight="black",size=18,pad=15)
                for index,value in enumerate(value_2.values):
                    plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",
                    fontweight="black",size=13)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'Education' columns.")
                
        if 'Education Field wise Employee Attrition' in visual:
            st.subheader("Employee Attrition By Education Field")
            #Visualization to show Total Employees by Education Field.
            if 'EducationField' in df.columns:
                plt.figure(figsize=(13.5,8))
                plt.subplot(1,2,1)
                value_1 = df["EducationField"].value_counts()
                sns.barplot(x=value_1.index, y=value_1.values,order=value_1.index,palette = ["#FFA07A", "#D4A1E7", "#FFC0CB","#87CEFA","#c979e6","#fd692e"])
                plt.title("Employees by Education Field",fontweight="black",size=20,pad=15)
                for index,value in enumerate(value_1.values):
                    plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15) 
                    plt.xticks(rotation=90)

                #Visualization to show Employee Attrition by Education Field.
                plt.subplot(1,2,2)
                
                value_2 = new_df["EducationField"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#760b4d","#ee199c","#ad3d82","#c5579b","#fe70c8","#fda9dd"])
                plt.title("Employee Attrition by Education Field",fontweight="black",size=18,pad=15)
                for index,value in enumerate(value_2.values):
                    plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",
                        fontweight="black",size=13)
                plt.xticks(rotation=90)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'EducationField' columns.")
                
        if 'Environment Satisfaction wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Environment Satisfaction")
            if 'EnvironmentSatisfaction' in df.columns:
                #Visualization to show Total Employees by EnvironmentSatisfaction.
                df["EnvironmentSatisfaction"] = df["EnvironmentSatisfaction"].replace({1:"Low",2:"Medium",3:"High",4:"Very High"})
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["EnvironmentSatisfaction"].value_counts()
                plt.title("Employees by EnvironmentSatisfaction", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90, colors=['#F70000','#E84040','#E96060','#E88181'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by EnvironmentSatisfaction.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["EnvironmentSatisfaction"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
                plt.title("Attrition Rate by Environment Satisfaction",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                    size=10,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'EnvironmentSatisfaction' columns.")
                
        if 'JobRoles wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by JobRole")
            if 'JobRole' in df.columns:
                ##Visualization to show Total Employees by JobRole.
                plt.figure(figsize=(13,8))
                plt.subplot(1,2,1)
                value_1 = df["JobRole"].value_counts()
                sns.barplot(x=value_1.index.tolist(), y=value_1.values,palette = ["#023e4d","#02719c", "#0aabeb", "#32c4fe","#3488a9","#61bce0","#9ad9f3","#6690a2","#3baecb"])
                plt.title("Employees by Job Role",fontweight="black",pad=15,size=18)
                plt.xticks(rotation=90)
                for index, value in enumerate(value_1.values):
                    plt.text(index,value,value,ha="center",va="bottom",fontweight="black",size=15)
                    
                #Visualization to show Attrition Rate by JobRole.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["JobRole"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#3ff7f7","#32b2bb", "#b3f1f6", "#84c2fe","#07a0ab","#61bce0","#19dcdc","#02737b","#05d9e8"])
                plt.title("Employee Attrition Rate by JobRole",fontweight="black",pad=15,size=18)
                plt.xticks(rotation=90)
                for index,value in enumerate(value_2.values):
                    plt.text(index,value, str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                    fontweight="black",size=10)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'JobRole' columns.")
        
        if 'Job Level wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Job Level")
            if 'JobLevel' in df.columns:
                #Visualization to show Total Employees by Job Level.
                df["JobLevel"] = df["JobLevel"].replace({1:"Entry Level",2:"Junior Level",3:"Mid Level",4:"Senior Level",5:"Executive Level"})
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["JobLevel"].value_counts()
                plt.title("Employees by Job Level", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.8,startangle=90,colors=['#FF6D8C', '#FF8C94', '#FFAC9B', '#FFCBA4',"#FFD8B1"],textprops={"fontweight":"black","size":13})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by JobLevel.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["JobLevel"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#f77ac3","#d47bf5","#fc7b90","#D4A1E7","#e70087"])
                plt.title("Attrition Rate by Job Level",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                    size=10,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'JobLevel' columns.")
                
        if 'Job Satisfaction wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Job Satisfaction")
            if 'JobSatisfaction' in df.columns:
                #Visualization to show Total Employees by Job Satisfaction.
                df["JobSatisfaction"] = df["JobSatisfaction"].replace({1:"Low",2:"Medium",3:"High",4:"Very High"})
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["JobSatisfaction"].value_counts()
                plt.title("Employees by Job Satisfaction", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.8,startangle=90,
                    colors=['#FFB300', '#FFC300', '#FFD700', '#FFFF00'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by Job Satisfaction.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["JobSatisfaction"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index,y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
                plt.title("Attrition Rate by Job Satisfaction",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",
                        size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'JobSatisfaction' columns.")
            
        if 'Marital Status wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Marital Status")
            if 'MaritalStatus' in df.columns:
                #Visualization to show Total Employees by MaritalStatus.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["MaritalStatus"].value_counts()
                plt.title("Employees by MaritalStatus", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,colors=['#E84040', '#E96060', '#E88181', '#E7A1A1'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by MaritalStatus.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["MaritalStatus"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index, y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
                plt.title("Attrition Rate by MaritalStatus", fontweight="black", size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(attrition_rate[index])+"% )",ha="center",va="bottom",size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'MaritalStatus' columns.")
                
        if 'Monthly Income wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Monthly Income")
            if 'MonthlyIncome' in df.columns:
                #Visualization to show Employee Distribution by MonthlyIncome.
                plt.figure(figsize=(13,6))
                plt.subplot(1,2,1)
                sns.histplot(x="MonthlyIncome", hue="Attrition", kde=True ,data=df,palette=["#11264e","#6faea4"])
                plt.title("Employee Attrition by Monthly Income",fontweight="black",size=20,pad=15)

                #Visualization to show Employee Attrition by Monthly Income.
                plt.subplot(1,2,2)
                sns.boxplot(x="Attrition",y="MonthlyIncome",data=df,palette=["#D4A1E7","#6faea4"])
                plt.title("Employee Attrition by Monthly Income",fontweight="black",size=20,pad=15)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'MonthlyIncome' columns.")
        
        if 'Monthly Rate wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Monthly Rate")
            if 'MonthlyRate' in df.columns:
                plt.figure(figsize=(13,6))
                plt.subplot(1,2,1)
                sns.histplot(x="MonthlyRate", hue="Attrition", data=df,kde=True, palette=["#11264e","#6eaefa"])
                plt.title("Employee Attrition by Monthly Rate",fontweight="black",size=20,pad=15)

                plt.subplot(1,2,2)
                sns.boxplot(x="Attrition",y="MonthlyRate",data=df,palette=["#1d7874","#AC1F29"])
                plt.title("Employee Attrition by Monthly Rate",fontweight="black",size=20,pad=15)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'MonthlyRate' columns.")
                
        if 'Number of Companies Worked wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Number of Companies Worked")
            if 'NumCompaniesWorked' in df.columns:
                df["NumCompaniesWorked"].describe().to_frame().T
                # Define the bin edges for the groups
                bin_edges = [0, 1, 3, 5, 10]
                # Define the labels for the groups
                bin_labels = ['0-1 Companies', '2-3 companies', '4-5 companies', "5+ companies"]
                # Cut the DailyRate column into groups
                df["NumCompaniesWorkedGroup"] = pd.cut(df['NumCompaniesWorked'], bins=bin_edges, labels=bin_labels)
                
                #Visualization to show Total Employees by NumCompaniesWorked.
                plt.figure(figsize=(13,6))
                plt.subplot(1,2,1)
                value_1 = df["NumCompaniesWorkedGroup"].value_counts()
                plt.title("Employees by Companies Worked", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                    colors=['#FF6D8C', '#FF8C94', '#FFAC9B', '#FFCBA4'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by NumCompaniesWorked.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["NumCompaniesWorkedGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
                plt.title("Attrition Rate by Companies Worked",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",size=15,fontweight="black")
                plt.xticks(size=12)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'NumCompaniesWorkedGroup' columns.")
        
        if 'Over Time wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Over Time")
            if 'OverTime' in df.columns:
                #Visualization to show Total Employees by OverTime.
                plt.figure(figsize=(15,6))
                plt.subplot(1,2,1)
                value_1 = df["OverTime"].value_counts()
                plt.title("Employees by OverTime", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                    colors=["#ffb563","#FFC0CB"],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by OverTime.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["OverTime"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#D4A1E7","#E7A1A1"])
                plt.title("Attrition Rate by OverTime",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                        size=15,fontweight="black")
                plt.xticks(size=13)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'OverTime' columns.")
        
        if 'Percentage Salary Hike wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Percentage Salary Hike")
            if 'PercentSalaryHike' in df.columns:
                #Visualization to show Employee Distribution by Percentage Salary Hike.
                plt.figure(figsize=(16,6))
                sns.countplot(x="PercentSalaryHike", hue="Attrition", data=df, palette=["#1d7874","#AC1F29"])
                plt.title("Employee Attrition By PercentSalaryHike",fontweight="black",size=20,pad=15)
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'PercentSalaryHike' columns.")
            
        if 'Performance Rating wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Performance Rating")
            if 'PerformanceRating' in df.columns:
                df["PerformanceRating"] = df["PerformanceRating"].replace({1:"Low",2:"Good",3:"Excellent",4:"Outstanding"})
                #Visualization to show Total Employees by PerformanceRating.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["PerformanceRating"].value_counts()
                plt.title("Employees by PerformanceRating", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                    colors=["#b86607","#ff8902","#ffb563","#fad6ac"],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by PerformanceRating.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["PerformanceRating"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(),y= value_2.values,palette=["#D4A1E7","#E7A1A1"])
                plt.title("Attrition Rate by PerformanceRating",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",
                            va="bottom",size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'PerformanceRating' columns.")
        
        if 'Relationship Satisfaction wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Relationship Satisfaction")
            if 'RelationshipSatisfaction' in df.columns:
                df["RelationshipSatisfaction"] = df["RelationshipSatisfaction"].replace({1:"Low",2:"Medium",3:"High",4:"Very High"})
                #Visualization to show Total Employees by RelationshipSatisfaction.
                plt.figure(figsize=(13,6))
                plt.subplot(1,2,1)
                value_1 = df["RelationshipSatisfaction"].value_counts()
                plt.title("Employees by RelationshipSatisfaction", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                    colors=['#6495ED', '#87CEEB', '#00BFFF', '#1E90FF'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by RelationshipSatisfaction.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["RelationshipSatisfaction"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index, y=value_2.values,order=value_2.index,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])
                plt.title("Attrition Rate by RelationshipSatisfaction",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'RelationshipSatisfaction' columns.")
                
        if 'Work Life Balance wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Work Life Balance")
            if 'WorkLifeBalance' in df.columns:
                df["WorkLifeBalance"] = df["WorkLifeBalance"].replace({1:"Bad",2:"Good",3:"Better",4:"Best"})
                ##Visualization to show Total Employees by WorkLifeBalance.
                plt.figure(figsize=(14.5,6))
                plt.subplot(1,2,1)
                value_1 = df["WorkLifeBalance"].value_counts()
                plt.title("Employees by WorkLifeBalance", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                    colors= ['#FF8000', '#FF9933', '#FFB366', '#FFCC99'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by WorkLifeBalance.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["WorkLifeBalance"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index, y=value_2.values,order=value_2.index,palette=["#bd15f5","#d15ef7","#de8ef9","#e5baf3"])
                plt.title("Employee Attrition Rate by WorkLifeBalance",fontweight="black",pad=15,size=18)
                for index,value in enumerate(value_2.values):
                    plt.text(index,value, str(value)+" ("+str(attrition_rate[index])+"%)",ha="center",va="bottom",fontweight="black",size=15)
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'WorkLifeBalance' columns.")
                
        if 'Total Working Years wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Total Working Year")
            if 'TotalWorkingYears' in df.columns:
                # Define the bin edges for the groups
                bin_edges = [0, 5, 10, 20, 50]
                # Define the labels for the groups
                bin_labels = ['0-5 years', '5-10 years', '10-20 years', "20+ years"]
                # Cut the DailyRate column into groups
                df["TotalWorkingYearsGroup"] = pd.cut(df['TotalWorkingYears'], bins=bin_edges, labels=bin_labels)
                
                #Visualization to show Total Employees by TotalWorkingYearsGroup.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["TotalWorkingYearsGroup"].value_counts()
                plt.title("Employees by TotalWorkingYears", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                    colors=['#E84040', '#E96060', '#E88181', '#E7A1A1'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by TotalWorkingYearsGroup.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["TotalWorkingYearsGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#0a0767","#0f09ae","#352fd2","#6c68ef"])
                plt.title("Attrition Rate by TotalWorkingYears",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",
                        size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'TotalWorkingYearsGroup' columns.")
        
        if 'Years at Company wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Years At Comany")
            if 'YearsAtCompany' in df.columns:
                # Define the bin edges for the groups
                bin_edges = [0, 1, 5, 10, 20]
                # Define the labels for the groups
                bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]
                # Cut the DailyRate column into groups
                df["YearsAtCompanyGroup"] = pd.cut(df['YearsAtCompany'], bins=bin_edges, labels=bin_labels)
                
                #Visualization to show Total Employees by YearsAtCompanyGroup.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["YearsAtCompanyGroup"].value_counts()
                plt.title("Employees by YearsAtCompany", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,colors=['#FFB300', '#FFC300', '#FFD700', '#FFFF00'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by YearsAtCompanyGroup.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["YearsAtCompanyGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#68dbef","#6faea4","#1c7cfa","#138397"])
                plt.title("Attrition Rate by YearsAtCompany",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'YearAtCompany' columns.")
                
        if 'Years In Current Role wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Year In Current Role")
            if 'YearsInCurrentRole' in df.columns:
                # Define the bin edges for the groups
                bin_edges = [0, 1, 5, 10, 20]
                # Define the labels for the groups
                bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]
                # Cut the DailyRate column into groups
                df["YearsInCurrentRoleGroup"] = pd.cut(df['YearsInCurrentRole'], bins=bin_edges, labels=bin_labels)
                
                #Visualization to show Total Employees by YearsInCurrentRoleGroup.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["YearsInCurrentRoleGroup"].value_counts()
                plt.title("Employees by YearsInCurrentRole", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#6495ED', '#87CEEB', '#00BFFF', '#1E90FF'],textprops={"fontweight":"black","size":15,"color":"black"})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by YearsInCurrentRoleGroup.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["YearsInCurrentRoleGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette= ["#041f42","#1f5dae","#1171ed","#63a1f1"])
                plt.title("Attrition Rate by YearsInCurrentRole",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'YearsInCurrentRole' columns.")
                
        if 'Years Since Last Promotion wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Years Since Last Promotion")
            if 'YearsSinceLastPromotion' in df.columns:
                # Define the bin edges for the groups
                bin_edges = [0, 1, 5, 10, 20]
                # Define the labels for the groups
                bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]
                # Cut the DailyRate column into groups
                df["YearsSinceLastPromotionGroup"] = pd.cut(df['YearsSinceLastPromotion'], bins=bin_edges, labels=bin_labels)
                
                #Visualization to show Total Employees by YearsSinceLastPromotionGroup.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["YearsSinceLastPromotionGroup"].value_counts()
                plt.title("Employees by YearsSinceLastPromotion", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors=['#FF6D8C', '#FF8C94', '#FFAC9B', '#FFCBA4'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by YearsSinceLastPromotionGroup.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["YearsSinceLastPromotionGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#11264e","#6faea4","#FEE08B","#D4A1E7","#E7A1A1"])

                plt.title("Attrition Rate by YearsSinceLastPromotion",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'YearsSinceLastPromotionGroup' columns.")
        
        if 'Years with Current Manager wise Employee Attrition' in visual:
            st.subheader("Employee Distribution by Years With Current Manager")
            if 'YearsWithCurrManager' in df.columns:
                # Define the bin edges for the groups
                bin_edges = [0, 1, 5, 10, 20]
                # Define the labels for the groups
                bin_labels = ['0-1 years', '2-5 years', '5-10 years', "10+ years"]
                # Cut the DailyRate column into groups
                df["YearsWithCurrManagerGroup"] = pd.cut(df['YearsWithCurrManager'], bins=bin_edges, labels=bin_labels)        
                
                #Visualization to show Total Employees by YearsWithCurrManagerGroup.
                plt.figure(figsize=(14,6))
                plt.subplot(1,2,1)
                value_1 = df["YearsWithCurrManagerGroup"].value_counts()
                plt.title("Employees by YearsWithCurrManager", fontweight="black", size=20, pad=20)
                plt.pie(value_1.values, labels=value_1.index, autopct="%.1f%%",pctdistance=0.75,startangle=90,
                colors= ['#FF8000', '#FF9933', '#FFB366', '#FFCC99'],textprops={"fontweight":"black","size":15})
                center_circle = plt.Circle((0, 0), 0.4, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(center_circle)

                #Visualization to show Attrition Rate by YearsWithCurrManagerGroup.
                plt.subplot(1,2,2)
                new_df = df[df["Attrition"]=="Yes"]
                value_2 = new_df["YearsWithCurrManagerGroup"].value_counts()
                attrition_rate = np.floor((value_2/value_1)*100).values
                sns.barplot(x=value_2.index.tolist(), y=value_2.values,palette=["#260ab0","#389fbc","#38bc7a","#3887bc"])
                plt.title("Attrition Rate by YearsWithCurrManager",fontweight="black",size=20,pad=20)
                for index,value in enumerate(value_2):
                    plt.text(index,value,str(value)+" ("+str(int(attrition_rate[index]))+"%)",ha="center",va="bottom",size=15,fontweight="black")
                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.error("The Uploaded Dataset Doesn't contain 'YearsWithCurrManagerGroup' columns.")
    
    
    # Statistical Analysis - Feature Importance
    if 'Statistical Analysis' in visuals:
        all_features = ['Visualizing the F_Score of ANOVA Test of Each Numerical features',
                        'Comparing F_Score and P_value of ANOVA Test',
                        'Visualizing the Chi-Square Statistic Values of Each Categorical Features',
                        'Compairing Chi2_Statistic and P_value of Chi_Square Test']
        features = st.sidebar.multiselect("Choose which features you want to explore on data 👇",all_features)
        
        
        st.header("_Statistical Analysis:_")
        if 'Visualizing the F_Score of ANOVA Test of Each Numerical features' in features:
        
            num_cols = df.select_dtypes(np.number).columns
            new_df = df.copy()
            new_df["Attrition"] = new_df["Attrition"].replace({"No":0,"Yes":1})
            f_scores = {}
            p_values = {}

            for column in num_cols:
                f_score, p_value = stats.f_oneway(new_df[column],new_df["Attrition"])
    
                f_scores[column] = f_score
                p_values[column] = p_value
            
            plt.figure(figsize=(15,6))
            keys = list(f_scores.keys())
            values = list(f_scores.values())

            sns.barplot(x=keys, y=values)
            plt.title("Anova-Test F_scores Comparison",fontweight="black",size=20,pad=15)
            plt.xticks(rotation=90)

            for index,value in enumerate(values):
                plt.text(index,value,int(value), ha="center", va="bottom",fontweight="black",size=15)
            #plt.tight_layout()
            st.pyplot(plt)
        
        if 'Comparing F_Score and P_value of ANOVA Test' in features:
            test_df = pd.DataFrame({"Features":keys,"F_Score":values})
            test_df["P_value"] = [format(p, '.20f') for p in list(p_values.values())]
            st.write(test_df)
        
        #Performing Chi-Square Test to Analyze the Categorical Feature Importance in Employee Attrition    
        cat_cols = df.select_dtypes(include="object").columns.tolist()
        cat_cols.remove("Attrition")
        chi2_statistic = {}
        p_values = {}

        # Perform chi-square test for each column
        for col in cat_cols:
            contingency_table = pd.crosstab(df[col], df['Attrition'])
            chi2, p_value, _, _ = chi2_contingency(contingency_table)
            chi2_statistic[col] = chi2
            p_values[col] = p_value
            
        if  'Visualizing the Chi-Square Statistic Values of Each Categorical Features' in features:
            columns = list(chi2_statistic.keys())
            values = list(chi2_statistic.values())

            plt.figure(figsize=(16,6))
            sns.barplot(x=columns, y=values)
            plt.xticks(rotation=90)
            plt.title("Chi2 Statistic Value of each Categorical Columns",fontweight="black",size=20,pad=15)
            for index,value in enumerate(values):
                plt.text(index,value,round(value,2),ha="center",va="bottom",fontweight="black",size=15)
            st.pyplot(plt)
        
        if 'Compairing Chi2_Statistic and P_value of Chi_Square Test' in features:
            test_df = pd.DataFrame({"Features":columns,"Chi_2 Statistic":values})
            test_df["P_value"] =  [format(p, '.20f') for p in list(p_values.values())]
            st.write(test_df)
        
        