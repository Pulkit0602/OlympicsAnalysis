import streamlit as st
import pandas as pd
import preprocess
import numpy as np
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff
import matplotlib.pyplot as plt


df_preprocess = preprocess.preprocess()

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally" , "Overall Analysis" , "Country-wise Analysis" , "Athlete wise Analysis")
)

#st.dataframe(df_preprocess)

if user_menu == "Medal Tally" :
    st.sidebar.header("Medal Tally")
    year,country = preprocess.dropDown(df_preprocess)
    selectedYear = st.sidebar.selectbox("Select Year" , year)
    selectedcountry = st.sidebar.selectbox("Select country" , country)
    #st.header(selectedYear)
    #st.header(selectedcountry)
    if selectedYear == "Overall" and selectedcountry == "Overall":
        st.title("Overall Tally")
        st.table(preprocess.medal_tally(df_preprocess))        

    elif selectedYear == "Overall" and  selectedcountry != "Overall":
        st.title(selectedcountry +" Overall Performance")
        df_country = preprocess.countryPerformance(df_preprocess , selectedcountry) 
        st.table(df_country)

    elif selectedYear != "Overall" and  selectedcountry == "Overall":
        st.title("Medal Tally In " + str(selectedYear) + " Olympics")
        df_year = preprocess.yearPerformance(df_preprocess , selectedYear) 
        st.table(df_year)
    
    elif selectedYear != "Overall" and selectedcountry != "Overall":
        st.title(selectedcountry +" Performance In " +  str(selectedYear) + " Olympics")
        df_specific = preprocess.specificPerformance(df_preprocess , country = selectedcountry , year = selectedYear) 
        st.table(df_specific)


if user_menu == "Overall Analysis" :
    st.sidebar.header("Overall-Analysis-Menu")
    Overall_Analysis_menu = st.sidebar.radio(
    "Select an Option",
    ("Top Statistics" , "Graphs" , "Heat-Map" , "Top-Athelets")
    )
    
    if Overall_Analysis_menu == "Top Statistics":
        editions = df_preprocess["Year"].unique().shape[0]-1
        Cities = df_preprocess["City"].unique().shape[0]
        Sports = df_preprocess["Sport"].unique().shape[0]
        Events = df_preprocess["Event"].unique().shape[0]
        Athletes = df_preprocess["Name"].unique().shape[0]
        Nations = df_preprocess["region"].unique().shape[0]

        st.title("Top Statistics")

        col1,col2,col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)

        with col2:
            st.header("Hosts")
            st.title(Cities)

        with col3:
            st.header("Sports")
            st.title(Sports)

        col1,col2,col3 = st.columns(3)
        with col1:
            st.header("Events")
            st.title(Events)

        with col2:
            st.header("Athletes")
            st.title(Athletes)

        with col3:
            st.header("Nations")
            st.title(Nations)

    if Overall_Analysis_menu == "Graphs":
        st.title("Participating Nation Over Years")
        data_Over_Time = preprocess.data_over_time(df_preprocess , "region")
        fig = px.line(data_Over_Time , x = "Year" , y = "region")
        st.plotly_chart(fig)

        st.title("Events Over Years")
        data_Over_Time = preprocess.data_over_time(df_preprocess , "Event")
        fig = px.line(data_Over_Time , x = "Year" , y = "Event")
        st.plotly_chart(fig)

        st.title("Athelete Over Years")
        data_Over_Time = preprocess.data_over_time(df_preprocess , "Name")
        fig = px.line(data_Over_Time , x = "Year" , y = "Name")
        st.plotly_chart(fig)

        st.title("Sports Over Years")
        data_Over_Time = preprocess.data_over_time(df_preprocess , "Sport")
        fig = px.line(data_Over_Time , x = "Year" , y = "Sport")
        st.plotly_chart(fig)
    
    if Overall_Analysis_menu == "Heat-Map":

        st.title("No. of Events over time(Every Sport)")
        fig,ax = plt.subplots(figsize = (20,20))
        heat_map_events = df_preprocess.drop_duplicates(subset = ["Year" , "Sport" , "Event"] )
        heat_map_events = heat_map_events.pivot_table(index = "Sport" , columns = "Year" , values="Event" , aggfunc="count").fillna(0).astype(int)
        ax = sns.heatmap(heat_map_events,annot=True)
        st.pyplot(fig)

    if Overall_Analysis_menu == "Top-Athelets":

        st.title("Most Successful Athlete")
        sport = df_preprocess["Sport"].unique().tolist()
        sport.sort()
        sport.insert(0,"Overall")
        sport = st.sidebar.selectbox("Select Sport" , sport)    
        most_succesful = preprocess.most_succesful(df_preprocess , sport)
        st.table(most_succesful)
        

if user_menu == "Country-wise Analysis" :
    st.sidebar.title("Country-wise Analysis")   
    country = np.unique(df_preprocess["region"].dropna()).tolist()
    country.sort()    
    selectedcountry = st.sidebar.selectbox("Select country" , country )
    st.title(selectedcountry + " Medal Tally Over Years") 

    Country_wise  = preprocess.country_medal(df_preprocess , selectedcountry)
    fig = px.line(Country_wise , x = Country_wise.index , y = "Medals")
    st.plotly_chart(fig)

    st.title(selectedcountry + " Excel Sports")
    fig,ax = plt.subplots(figsize = (20,20))
    heat_map = preprocess.heat_map_country(df_preprocess ,selectedcountry)
    sns.heatmap(heat_map,annot=True)
    st.pyplot(fig)

    st.title( selectedcountry  + " Most Successful Athlete")    
    succesful_country = preprocess.succesful_country(df_preprocess , selectedcountry)
    st.table(succesful_country)

if user_menu == "Athlete wise Analysis" :
    #Age-Medal-Realtionship
    st.title("Distrubution of Age")
    df7 = df_preprocess.copy()
    df7 = df7.drop_duplicates(subset = ["region" ,"Name"] )  
    x1 = df7["Age"].dropna()
    x2 = df7[df7["Medal"] == "Gold"]["Age"].dropna()
    x3 = df7[df7["Medal"] == "Silver"]["Age"].dropna()
    x4 = df7[df7["Medal"] == "Bronze"]["Age"].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4],["Overall Age","Gold-Medalist","Silver-Medalist","Bronze-Medalist"] , show_rug=False ,show_hist=False )
    fig.update_layout(autosize = False , width = 1000 , height = 600)
    st.plotly_chart(fig)

    #Height - weigth Relation
    st.title("Height Weight Relationship")
    sport = df_preprocess["Sport"].unique().tolist()
    sport.sort()
    sport.insert(0,"Overall")
    sport = st.sidebar.selectbox("Select Sport" , sport)
    df9 = preprocess.height_weight(df_preprocess , sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=df9["Weight"], y=df9["Height"],hue = df9["Medal"] , style = df9["Sex"], s =70)
    st.pyplot(fig)

    st.title("Female-Male-Competitors")
    df_gender = preprocess.M_F_participation(df_preprocess)
    fig = px.line(df_gender , x = "Year" , y =["Male" , "Female"] )
    st.plotly_chart(fig)

    st.title("Female-Male-Medals")
    df_gender = preprocess.M_F_medals(df_preprocess)
    fig = px.line(df_gender , x = "Year" , y =["Male" , "Female"] )
    st.plotly_chart(fig)