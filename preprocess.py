import pandas as pd 
import numpy as np

athlete = pd.read_csv("athlete_events.csv")
regions = pd.read_csv("noc_regions.csv")

def preprocess():
    #Extracting info for summer olympics
    athlete_summer = athlete[athlete["Season"] == "Summer"]    
    #Merging DataFrames
    athlete_summer = athlete_summer.merge(regions , on='NOC' , how="left")
    #Dropping Duplicates
    athlete_summer.drop_duplicates(inplace= True)

    return athlete_summer


def medal_tally(athlete_summer):
    
    athlete_summer = pd.concat([athlete_summer,pd.get_dummies(athlete_summer["Medal"])],axis = 1)
    medal_tally = athlete_summer.drop_duplicates(subset = ["Sex" , "NOC" , "Games" , "Year" , "Sport" ,"City" ,"Event" , "Medal"] )
    medal_tally = medal_tally.groupby(athlete_summer["region"]).sum()[["Gold" , "Silver" ,"Bronze"]].sort_values("Gold" , ascending =False).reset_index()
    medal_tally["Total"] = medal_tally["Gold"]+medal_tally["Silver"]+medal_tally["Bronze"]

    medal_tally["Gold"] = medal_tally["Gold"].astype("int")
    medal_tally["Silver"] = medal_tally["Silver"].astype("int")
    medal_tally["Bronze"] = medal_tally["Bronze"].astype("int")
    medal_tally["Total"] = medal_tally["Total"].astype("int")

    return medal_tally

def dropDown(athlete_summer):
    #For Year Drop-Down
    year = athlete_summer["Year"].unique().tolist()
    year.sort(reverse=True)
    year.insert(0,"Overall")

    #For Country Drop-Down
    country = np.unique(athlete_summer["region"].dropna()).tolist()
    country.sort()
    country.insert(0,"Overall")
    return year,country

def yearPerformance(athlete_summer , year ):
    athlete_summer = pd.concat([athlete_summer,pd.get_dummies(athlete_summer["Medal"])],axis = 1)
    df1 = athlete_summer.drop_duplicates(subset = ["Sex" , "NOC" , "Games" , "Year" , "Sport" ,"City" ,"Event" , "Medal"] )
    df1.drop(["Name" , "ID" ,"Age" ,"Team","notes","NOC","Sex" ,"Height" , "Weight" , "Season" , "Games" , "City" , "Medal" ] ,inplace= True ,axis = "columns")
    df1 = df1[df1["Year"] == year].groupby(df1["region"]).sum()[["Gold" , "Silver" , "Bronze"]].sort_values("Gold" , ascending =False).reset_index()
    df1["Total"] = df1["Gold"] + df1["Silver"] + df1["Bronze"]
    return df1

def countryPerformance(athlete_summer , country):
    athlete_summer = pd.concat([athlete_summer,pd.get_dummies(athlete_summer["Medal"])],axis = 1)
    df2 = athlete_summer.drop_duplicates(subset = ["Sex" , "NOC" , "Games" , "Year" , "Sport" ,"City" ,"Event" , "Medal"] )
    df2.drop(["Name" , "ID" ,"Age" ,"Team","notes","NOC","Sex" ,"Height" , "Weight" , "Season" , "Games" , "City" , "Medal" ] ,inplace= True ,axis = "columns")
    df2 = df2[df2["region"] == country ].groupby(df2["Year"]).sum()[["Gold" , "Silver" , "Bronze"]].sort_values("Year" , ascending =False).reset_index()
    df2["Total"] = df2["Gold"] + df2["Silver"] + df2["Bronze"]
    return df2

def specificPerformance(athlete_summer , country ,year):
    athlete_summer = pd.concat([athlete_summer,pd.get_dummies(athlete_summer["Medal"])],axis = 1)
    df3 = athlete_summer.drop_duplicates(subset = ["Sex" , "NOC" , "Games" , "Year" , "Sport" ,"City" ,"Event" , "Medal"] )
    df3.drop(["Name" , "ID" ,"Age" ,"Team","notes","NOC","Sex" ,"Height" , "Weight" , "Season" , "Games" , "City" , "Medal" ] ,inplace= True ,axis = "columns")
    df3 = df3[(df3["region"] == country) & (df3["Year"] == year )].groupby(df3["region"]).sum()[["Gold" , "Silver" , "Bronze"]].reset_index()
    df3["Total"] = df3["Gold"] + df3["Silver"] + df3["Bronze"]
    return df3

def data_over_time(athlete_summer ,data):
        #graph that how no of nations inc with each year in olympics (Line Graph)
    # X=Olympic Year # Y= No of sports
    oly_data = athlete_summer.drop_duplicates(subset = ["Year" , data] )
    data_Over_Time = oly_data.groupby(athlete_summer["Year"]).count()[data].reset_index()
    data_Over_Time = data_Over_Time.rename(columns = {'region':data}) 

    return data_Over_Time 

def most_succesful(df3 , sport):
    
    df3 = df3.dropna(subset = "Medal")
    
    if sport != "Overall":
        df_succesful = df3[df3["Sport"] == sport][["Name","region"]].value_counts().reset_index().head(10)
        df_succesful  = df_succesful .rename(columns = {'index':'Athlete' ,0:"Medals"}) 
    else:
        print("Hey")
        df_succesful = df3[["Name","Sport","region"]].value_counts().reset_index().head(10)
        df_succesful  = df_succesful .rename(columns = {0:"Medals"})

    return df_succesful

def country_medal(df5 , country):
    df5= pd.concat([df5,pd.get_dummies(df5["Medal"])],axis = 1)
    df5 = df5.drop_duplicates(subset = ["Sex" , "NOC" , "Games" , "Year" , "Sport" ,"City" ,"Event" , "Medal"])        
    df5 = df5[df5["region"] == country].groupby(df5["Year"]).sum()[["Gold" , "Silver" , "Bronze"]]
    df5["Medals"] = df5["Gold"] + df5["Silver"] + df5["Bronze"]

    return df5

#Heat Map of country
def heat_map_country(df6 , country):

    df6 = pd.concat([df6,pd.get_dummies(df6["Medal"])],axis = 1)    
    df6.drop_duplicates(subset = ["Year" , "Sport" , "Event" , "region","Medal"] ,inplace =True )
    df6 = df6.dropna(subset=["Medal"])
    df6["Medals"] = df6["Gold"] + df6["Silver"] + df6["Bronze"]
    df6 = df6[df6["region"] == country]     
    df6 = df6.pivot_table(index = "Sport" , columns = "Year" , values="Medals" , aggfunc="count").fillna(0).astype(int)

    return df6  

#3.Most Successful Athlete
def succesful_country(df6 , country):
    
    df6 = df6.drop_duplicates(subset = ["Year" , "Sport" , "Event" , "region" ,"Name"] )    
    df6 = df6.dropna(subset=["Medal"])
    df6 = df6[df6["region"] == country][["Name" , "Sport"]].value_counts().head(10).reset_index()     
    df6 = df6.rename(columns = {0:"Medals"})
    
    return df6

def height_weight(df,sport):
    #Height - weigth Relation
    df8 = df.copy()
    if sport != "Overall":
        df9 = df8[df8["Sport"] == sport]
    else:
         df9 = df8.copy()         
    return df9

def M_F_participation(df10):
    df10.drop_duplicates(subset = ["Year" , "region" ,"Name"] , inplace = True)
    df_male = df10[df10["Sex"] == "M"].groupby(df10["Year"]).count()["Name"].reset_index()
    df_female = df10[df10["Sex"] == "F"].groupby(df10["Year"]).count()["Name"].reset_index()
    df_gender = df_male.merge(df_female , on="Year")
    df_gender  = df_gender .rename(columns = {"Name_x":"Male" , "Name_y":"Female"})    
    
    return df_gender

def M_F_medals(df10):
    df10.drop_duplicates(subset = ["Year" , "region" ,"Name"] , inplace = True)
    df10.dropna(subset=["Medal"] , inplace = True)
    df_male = df10[df10["Sex"] == "M"].groupby(df10["Year"]).count()["Name"].reset_index()
    df_female = df10[df10["Sex"] == "F"].groupby(df10["Year"]).count()["Name"].reset_index()
    df_gender = df_male.merge(df_female , on="Year")
    df_gender  = df_gender .rename(columns = {"Name_x":"Male" , "Name_y":"Female"})    
    
    return df_gender